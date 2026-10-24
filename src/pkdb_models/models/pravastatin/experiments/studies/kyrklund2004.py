"""Simulation experiment of the study Kyrklund2004."""

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
    F_OATP1B1_RIFAMPICIN,
    PravastatinSimulationExperiment,
)


class Arm(NamedTuple):
    """An arm of the crossover."""

    #: label of the plasma data (Fig1) and intervention of Table 2
    intervention: str
    #: activity of OATP1B1 (`LI__f_OATP1B1`)
    f_oatp1b1: float
    coadministration: Coadministration
    label: str
    color: str


class Kyrklund2004(PravastatinSimulationExperiment):
    """Simulation experiment of Kyrklund2004.

    10 healthy volunteers (19-25 yr, 52-103 kg) took rifampicin 600 mg or
    placebo once daily for 5 days in a randomized crossover (washout 4
    weeks); on day 6, 17 h after the last dose of rifampicin, they took a
    single 40 mg tablet of pravastatin sodium (Pravachol) with 150 ml water
    after an overnight fast, meals 3 and 7 h after the dose. Plasma by
    LC-MS/MS to 12 h (Fig1, mean and SEM), urine 0-12 h (Ae(0-12) of Table 2,
    mean and SD).

    Rifampicin, given 17 h before pravastatin, induces the hepatic uptake
    (OATP1B1) rather than inhibiting it: the AUC fell to 0.69, Cmax to 0.79,
    Ae(0-12) to 0.79, while the renal clearance (24.2 and 26.2 l/h) and the
    half-life did not change. The arm is simulated with the activity
    `F_OATP1B1_RIFAMPICIN` of the base experiment, which is not fitted.
    """

    arms: ClassVar[dict[str, Arm]] = {
        "placebo": Arm(
            intervention="pravastatin40mg_po",
            f_oatp1b1=1.0,
            coadministration=Coadministration.NONE,
            label="40 mg (placebo)",
            color="black",
        ),
        "rif": Arm(
            intervention="pravastatin40mg_po, rifampicin",
            f_oatp1b1=F_OATP1B1_RIFAMPICIN,
            coadministration=Coadministration.RIFAMPICIN,
            label="40 mg after rifampicin 600 mg daily",
            color="tab:blue",
        ),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        df_tab2 = self.load_dataframe("Tab2")
        for key, arm in self.arms.items():
            dset = DataSet.from_df(df[df.label == arm.intervention], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig1_{key}"] = dset

            # Ae(0-12)
            df_urine = df_tab2[
                (df_tab2.intervention == arm.intervention)
                & (df_tab2.measurement_type == "cumulative amount")
            ]
            dset = DataSet.from_df(df_urine, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Tab2_{key}_urine"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            f"pra40_{key}": Simulation(
                start=0,
                end=13 * 60,
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
        mappings = {}
        for key, arm in self.arms.items():
            for dset_id, yid, tissue in [
                (f"Fig1_{key}", "[Cve_pra]", Tissue.PLASMA),
                (f"Tab2_{key}_urine", "Aurine_pra", Tissue.URINE),
            ]:
                suffix = "_urine" if tissue == Tissue.URINE else ""
                mappings[f"fm_pra40po_{key}{suffix}"] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=dset_id,
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self, task=f"task_pra40_{key}", xid="time", yid=yid
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=tissue,
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
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            num_cols=3,
            name=f"{self.__class__.__name__} (healthy, fasted, rifampicin)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-3)
        plots[2].set_yaxis(self.label_pra_urine, unit="µmole")

        for key, arm in self.arms.items():
            for k, plot in enumerate(plots):
                urine = k == 2
                plot.add_data(
                    task=f"task_pra40_{key}",
                    xid="time",
                    yid="Aurine_pra" if urine else "[Cve_pra]",
                    label=f"Sim {arm.label}",
                    color=arm.color,
                )
                plot.add_data(
                    dataset=f"Tab2_{key}_urine" if urine else f"Fig1_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"{arm.label}, Ae(0-12)" if urine else arm.label,
                    color=arm.color,
                    marker="s" if key == "placebo" else "o",
                    linestyle="" if urine else "--",
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Kyrklund2004, output_dir=Kyrklund2004.__name__)
