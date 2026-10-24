"""Simulation experiment of the study Neuvonen1998."""

from typing import ClassVar, NamedTuple, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
    DataType,
    Dosing,
    Fasting,
    Genotype,
    Health,
    PKPDData,
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
    F_NO_INTERACTION,
    PravastatinSimulationExperiment,
)


class Arm(NamedTuple):
    """An arm of the crossover."""

    #: label of the serum data of pravastatin (Fig3)
    label_data: str
    #: activity of OATP1B1 (`LI__f_OATP1B1`)
    f_oatp1b1: float
    coadministration: Coadministration
    label: str
    color: str


class Neuvonen1998(PravastatinSimulationExperiment):
    """Simulation experiment of Neuvonen1998.

    Study II of two parallel crossover studies (study I is simvastatin): 10
    healthy volunteers (7 men, 3 women, 52-86 kg) took itraconazole 200 mg or
    placebo once daily for 4 days (4 weeks between the phases); on day 4 they
    took a single 40 mg tablet of pravastatin sodium (Pravachol) with 150 ml
    water 2 h after itraconazole, fasted from 2 h before the dose, a meal 4 h
    after it. Serum by GC-MS (limit of quantification 0.5 ng/ml) to 24 h
    (Fig3, mean and SEM); the means of zero at 12 and 24 h are below the limit
    of quantification and are not used. The total HMG-CoA reductase
    inhibitors of Fig3 (radioenzymatic assay, pravastatin and its active
    metabolites in ng equivalents of pravastatin sodium) are not an
    observable of the model.

    Itraconazole inhibits CYP3A4 and P-glycoprotein; pravastatin is not
    metabolized by CYP3A4, and the AUC ratio of 1.71 (Cmax 1.80) was not
    significant and driven by two subjects. The arm is simulated without an
    interaction (`F_NO_INTERACTION`).
    """

    arms: ClassVar[dict[str, Arm]] = {
        "placebo": Arm(
            label_data="PRA_pravastatin",
            f_oatp1b1=1.0,
            coadministration=Coadministration.NONE,
            label="40 mg (placebo)",
            color="black",
        ),
        "itr": Arm(
            label_data="PRA+ITR_pravastatin",
            f_oatp1b1=F_NO_INTERACTION,
            coadministration=Coadministration.ITRACONAZOLE,
            label="40 mg + itraconazole 200 mg",
            color="tab:purple",
        ),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig3")
        # below the limit of quantification: the means of zero after the dose
        df = df[(df.time == 0) | (df["mean"] > 0)]
        for key, arm in self.arms.items():
            dset = DataSet.from_df(df[df.label == arm.label_data], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig3_{key}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            f"pra40_{key}": Simulation(
                start=0,
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # 40 mg pravastatin sodium, fasted
                    "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "LI__f_OATP1B1": Q(arm.f_oatp1b1, "dimensionless"),
                },
            )
            for key, arm in self.arms.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        return {
            f"fm_pra40po_Fig3_{key}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig3_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_pra40_{key}", xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.HEALTHY,
                    coadministration=arm.coadministration,
                    genotype=Genotype.NR,
                    data=PKPDData.PK,
                    data_type=DataType.MEAN,
                ),
            )
            for key, arm in self.arms.items()
        }

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig3",
            num_cols=2,
            name=f"{self.__class__.__name__} (healthy, fasted, itraconazole)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", max=12), legend=True
        )
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-3)

        for plot in plots:
            for key, arm in self.arms.items():
                plot.add_data(
                    task=f"task_pra40_{key}",
                    xid="time",
                    yid="[Cve_pra]",
                    label=f"Sim {arm.label}",
                    color=arm.color,
                    # the arms are the same simulation (no interaction)
                    linestyle="-" if key == "placebo" else "--",
                )
                plot.add_data(
                    dataset=f"Fig3_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=arm.label,
                    color=arm.color,
                    marker="o",
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Neuvonen1998, output_dir=Neuvonen1998.__name__)
