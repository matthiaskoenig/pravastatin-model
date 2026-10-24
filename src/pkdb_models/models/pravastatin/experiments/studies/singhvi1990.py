"""Simulation experiment of the study Singhvi1990."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
    DataType,
    Dosing,
    Fasting,
    Genotype,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.pravastatin import MODEL
from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
)


class Singhvi1990(PravastatinSimulationExperiment):
    """Simulation experiment of Singhvi1990.

    8 healthy Caucasian men (74 kg) received 9.9 mg [14C]-pravastatin sodium
    intravenously over 2 min and 19.2 mg as an oral solution in a randomized
    crossover (fasting not reported). Plasma pravastatin (Fig2, mean and SD)
    to 3 h; urine and feces over 4 days. Of the dose, 47 % (iv) and 8 % (po)
    were excreted as unchanged pravastatin in the urine within 48 h; the
    excreta of 96 h are total radioactivity, pravastatin and its metabolites
    (urine 60 % and 20 %, feces 34 % and 71 %), which the model does not
    have. The amounts are of pravastatin sodium.
    """

    #: the routes: dataset suffix, key of the fit mappings, route, form
    interventions: ClassVar[dict[str, tuple[str, Route, ApplicationForm]]] = {
        "iv_10": ("10iv", Route.IV, ApplicationForm.NR),
        "po_20": ("20po", Route.PO, ApplicationForm.SOLUTION),
    }
    labels_intervention: ClassVar[dict[str, str]] = {
        "iv_10": "9.9 mg iv",
        "po_20": "19.2 mg po (solution)",
    }
    colors: ClassVar[dict[str, str]] = {
        "iv_10": "tab:blue",
        "po_20": "black",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig2")
        for label, df_label in df.groupby("label"):
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig2_{label}"] = dset

        # the amounts [mg] are of pravastatin sodium (fractions of the dose)
        df = self.load_dataframe("FigA")
        df = df[df.measurement_type == "cumulative amount"]
        for label, df_label in df.groupby("label"):
            dset = DataSet.from_df(df_label, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra_na)
            dsets[f"FigA_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "pra_iv_10": Simulation(
                start=0,
                end=97 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # 9.9 mg pravastatin sodium over 2 min
                    "IVDOSE_pra": Q(9.9, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "ti_pra": Q(60, "s"),
                },
            ),
            "pra_po_20": Simulation(
                start=0,
                end=97 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # 19.2 mg pravastatin sodium, an oral solution without the
                    # dissolution of a tablet
                    "PODOSE_pra": Q(19.2, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "GU__Ka_dis_pra": Q(20, "1/hr"),
                },
            ),
        }

    def _metadata(self, intervention: str, tissue: Tissue) -> PKPDMappingMetaData:
        _, route, application_form = self.interventions[intervention]
        return PKPDMappingMetaData(
            tissue=tissue,
            route=route,
            application_form=application_form,
            dosing=Dosing.SINGLE,
            fasting=Fasting.NR,
            health=Health.HEALTHY,
            genotype=Genotype.NR,
            data_type=DataType.MEAN,
        )

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for intervention, (key, _, _) in self.interventions.items():
            task = f"task_pra_{intervention}"
            # plasma
            mappings[f"fm_pra{key}_pra"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig2_PRA_{intervention}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task=task, xid="time", yid="[Cve_pra]"),
                metadata=self._metadata(intervention, Tissue.PLASMA),
            )
            # unchanged pravastatin in the urine (0-48 h)
            mappings[f"fm_pra{key}_pra_urine"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"FigA_PRA_urine_{intervention}",
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(self, task=task, xid="time", yid="Aurine_pra"),
                metadata=self._metadata(intervention, Tissue.URINE),
            )
            # total radioactivity in the urine and the feces (0-96 h), not
            # the unchanged pravastatin of the model
            for tissue in ["urine", "feces"]:
                mappings[f"fm_pra{key}_total14c_{tissue}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=f"FigA_PRA14C_{tissue}_{intervention}",
                        xid="time",
                        yid="mean",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=task, xid="time", yid=f"A{tissue}_pra"
                    ),
                    metadata=self._metadata(
                        intervention,
                        Tissue.URINE if tissue == "urine" else Tissue.FECES,
                    ),
                )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig2",
            num_rows=2,
            num_cols=2,
            name=f"{self.__class__.__name__} (healthy)",
            # one legend per row right of the panels: a legend inside covered
            # the urine data
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_xaxis(self.label_time, unit="hr", min=0, max=3.5)
        plots[0].set_yaxis(self.label_pra, unit="µM", scale="log", min=5e-3)
        # linear: the oral peak and the iv tail (the iv peak in the log panel)
        plots[1].set_xaxis(self.label_time, unit="hr", min=0, max=3.5)
        plots[1].set_yaxis(self.label_pra, unit="µM", min=0, max=0.3)
        plots[2].set_yaxis(self.label_pra_urine, unit="µmole")
        plots[3].set_yaxis(self.label_pra_feces, unit="µmole")

        for intervention in self.interventions:
            task = f"task_pra_{intervention}"
            label = self.labels_intervention[intervention]
            color = self.colors[intervention]
            for plot, yid in [
                (plots[0], "[Cve_pra]"),
                (plots[1], "[Cve_pra]"),
                (plots[2], "Aurine_pra"),
                (plots[3], "Afeces_pra"),
            ]:
                plot.add_data(
                    task=task, xid="time", yid=yid, label=f"Sim {label}", color=color
                )
            for plot in plots[:2]:
                plot.add_data(
                    dataset=f"Fig2_PRA_{intervention}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=label,
                    color=color,
                )
            plots[2].add_data(
                dataset=f"FigA_PRA_urine_{intervention}",
                xid="time",
                yid="mean",
                count="count",
                label=f"{label} (unchanged)",
                color=color,
                linestyle="",
            )
            for plot, tissue in [(plots[2], "urine"), (plots[3], "feces")]:
                plot.add_data(
                    dataset=f"FigA_PRA14C_{tissue}_{intervention}",
                    xid="time",
                    yid="mean",
                    count="count",
                    label=f"{label} (total 14C)",
                    color=color,
                    marker="^",
                    linestyle="",
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Singhvi1990, output_dir=Singhvi1990.__name__)
