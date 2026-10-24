"""Simulation experiment of the study Sigurbjoernsson1998."""

from typing import ClassVar, NamedTuple, override

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


class Curve(NamedTuple):
    """An individual curve of the figures: dataset, dose [mg], label, marker."""

    dataset: str
    dose: int
    label: str
    marker: str


class Sigurbjoernsson1998(PravastatinSimulationExperiment):
    """Simulation experiment of Sigurbjoernsson1998.

    20 Caucasian subjects (46-81 years, 13 women, 7 men): 15 patients with
    primary moderate hypercholesterolaemia, who had taken pravastatin 20 mg
    once daily for 3 months, and 5 normal volunteers. 5 of the patients took
    single oral doses of 20 and 40 mg pravastatin sodium in the morning,
    breakfast 30 min after the dose; serum by HPLC-UV (detection limit
    2 ng/ml) to 4.5 h. The figures show individual elderly patients: subject 1
    after 20 and 40 mg (Fig3), subject 2 after 40 mg (Fig4, from 1.5 h). Fig5
    is the 40 mg curve of subject 1 (Fig3) again on a log axis and is not
    used.

    The chronic therapy is simulated as the single dose of the study day: the
    serum before the dose is below the detection limit (Fig3) and a dosing
    interval of 24 h with a half-life of about 2 h leaves no accumulation.
    """

    curves: ClassVar[list[Curve]] = [
        Curve("Fig3_pravastatin_20mg_po_elderly1", 20, "subject 1, 20 mg", "s"),
        Curve("Fig3_pravastatin_40mg_po_elderly1", 40, "subject 1, 40 mg", "^"),
        Curve("Fig4_pravastatin_40mg_po_elderly2", 40, "subject 2, 40 mg", "v"),
    ]
    #: the keys of the fit mappings by dataset
    mapping_keys: ClassVar[dict[str, str]] = {
        "Fig3_pravastatin_20mg_po_elderly1": "fm_pra20po_pra_elderly1",
        "Fig3_pravastatin_40mg_po_elderly1": "fm_pra40po_pra_elderly1",
        "Fig4_pravastatin_40mg_po_elderly2": "fm_pra40po_pra_elderly2",
    }
    colors: ClassVar[dict[int, str]] = {20: "tab:gray", 40: "black"}

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig3", "Fig4"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("value", 1 / self.Mr.pra)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            f"pra_{dose}": Simulation(
                start=0,
                end=5 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # pravastatin sodium, fasted (breakfast 30 min later)
                    "PODOSE_pra": Q(dose, "mg") * self.Mr.pra / self.Mr.pra_na,
                },
            )
            for dose in self.colors
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        return {
            self.mapping_keys[curve.dataset]: FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=curve.dataset,
                    xid="time",
                    yid="value",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_pra_{curve.dose}", xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.NR,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
                    genotype=Genotype.NR,
                    data_type=DataType.INDIVIDUAL,
                ),
            )
            for curve in self.curves
        }

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig3_Fig4",
            num_cols=2,
            name=f"{self.__class__.__name__} (hypercholesterolaemia, elderly)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=5e-3)

        for plot in plots:
            for dose, color in self.colors.items():
                plot.add_data(
                    task=f"task_pra_{dose}",
                    xid="time",
                    yid="[Cve_pra]",
                    label=f"Sim {dose} mg",
                    color=color,
                )
            for curve in self.curves:
                plot.add_data(
                    dataset=curve.dataset,
                    xid="time",
                    yid="value",
                    count="count",
                    label=curve.label,
                    color=self.colors[curve.dose],
                    marker=curve.marker,
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Sigurbjoernsson1998, output_dir=Sigurbjoernsson1998.__name__)
