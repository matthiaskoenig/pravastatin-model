"""Simulation experiment of the study Wu2012."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
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
    F_OATP1B1_QUERCETIN,
    PravastatinSimulationExperiment,
)


class Wu2012(PravastatinSimulationExperiment):
    """Simulation experiment of Wu2012.

    16 healthy Chinese-Han men (60-80 kg) took quercetin 500 mg or placebo
    once daily for 14 days in a randomized crossover; on day 14 they took a
    single 40 mg tablet of pravastatin sodium (Mevalotin) after an overnight
    fast, 1 h after the last capsule, a meal 4 h later. Plasma by LC-MS/MS
    (limit of quantification 0.957 ng/ml) to 10 h (Fig4, mean and SD: the
    caption says SEM, but the bars are SD by the coefficient of variation of
    Cmax in Table 1).

    Quercetin inhibits the hepatic uptake of pravastatin by OATP1B1 (in vitro
    IC50 about 16 µM; AUC ratio 1.24, Cmax ratio 1.31), simulated with the
    activity `F_OATP1B1_QUERCETIN` of the base experiment, which is not
    fitted.
    """

    #: the arms of Fig4: the activity of OATP1B1 and the coadministration
    interventions: ClassVar[dict[str, tuple[float, Coadministration]]] = {
        "pra40": (1.0, Coadministration.NONE),
        "pra40_quercetin": (F_OATP1B1_QUERCETIN, Coadministration.QUERCETIN),
    }
    labels_arm: ClassVar[dict[str, str]] = {
        "pra40": "40 mg (placebo)",
        "pra40_quercetin": "40 mg + quercetin 500 mg",
    }
    colors: ClassVar[dict[str, str]] = {
        "pra40": "black",
        "pra40_quercetin": "tab:red",
    }
    markers: ClassVar[dict[str, str]] = {
        "pra40": "s",
        "pra40_quercetin": "o",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig4")
        for label in self.interventions:
            dset = DataSet.from_df(df[df.label == label], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig4_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            label: Simulation(
                start=0,
                end=11 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # 40 mg pravastatin sodium, fasted
                    "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "LI__f_OATP1B1": Q(f_oatp1b1, "dimensionless"),
                },
            )
            for label, (f_oatp1b1, _) in self.interventions.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for label, (_, coadministration) in self.interventions.items():
            mappings[f"fm_pra40po_Fig4_{label}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig4_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_{label}", xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.HEALTHY,
                    coadministration=coadministration,
                    genotype=Genotype.NR,
                    data_type=DataType.MEAN,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig4",
            num_cols=2,
            name=f"{self.__class__.__name__} (healthy, fasted)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-3)

        for plot in plots:
            for label in self.interventions:
                plot.add_data(
                    task=f"task_{label}",
                    xid="time",
                    yid="[Cve_pra]",
                    label=f"Sim {self.labels_arm[label]}",
                    color=self.colors[label],
                )
                plot.add_data(
                    dataset=f"Fig4_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=self.labels_arm[label],
                    color=self.colors[label],
                    marker=self.markers[label],
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Wu2012, output_dir=Wu2012.__name__)
