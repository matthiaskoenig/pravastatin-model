"""Simulation experiment of the study Kyrklund2003a."""

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
    F_OAT3_GEMFIBROZIL,
    F_OATP1B1_GEMFIBROZIL,
    PravastatinSimulationExperiment,
)


class Arm(NamedTuple):
    """An arm of the crossover."""

    #: label of the plasma data (Fig1)
    label_plasma: str
    #: intervention of the urinary data (Table II)
    intervention: str
    #: activity of OATP1B1 (`LI__f_OATP1B1`)
    f_oatp1b1: float
    #: activity of the renal secretion by OAT3 (`KI__f_OAT3`)
    f_oat3: float
    coadministration: Coadministration
    label: str
    color: str


class Kyrklund2003a(PravastatinSimulationExperiment):
    """Simulation experiment of Kyrklund2003a.

    10 healthy volunteers (5 men, 5 women, 60-85 kg) took gemfibrozil 600 mg or
    placebo twice daily for 3 days in a randomized crossover (washout 2
    weeks); on day 3 they took a single 40 mg tablet of pravastatin sodium
    (Pravachol) with 150 ml water after an overnight fast. Plasma by LC-MS/MS
    to 24 h (Fig1, mean and SEM, digitized to 12 h), urine 0-12 and 12-24 h
    (Ae(0-24) of Table II, mean and SD).

    Gemfibrozil (and its glucuronide) inhibits the hepatic uptake by OATP1B1
    and the tubular secretion by OAT3: the AUC rose 2.02 fold, Cmax 1.81 fold,
    the renal clearance fell to 0.57 (25.0 to 14.3 l/h), the half-life and
    Ae(0-24) did not change. The arm is simulated with the activities
    `F_OATP1B1_GEMFIBROZIL` and `F_OAT3_GEMFIBROZIL` of the base experiment,
    which are not fitted.
    """

    arms: ClassVar[dict[str, Arm]] = {
        "placebo": Arm(
            label_plasma="pra_40",
            intervention="PRA40",
            f_oatp1b1=1.0,
            f_oat3=1.0,
            coadministration=Coadministration.NONE,
            label="40 mg (placebo)",
            color="black",
        ),
        "gem": Arm(
            label_plasma="gem_600",
            intervention="PRA40, GEM600",
            f_oatp1b1=F_OATP1B1_GEMFIBROZIL,
            f_oat3=F_OAT3_GEMFIBROZIL,
            coadministration=Coadministration.GEMFIBROZIL,
            label="40 mg + gemfibrozil 600 mg b.i.d.",
            color="tab:red",
        ),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        df_tab2 = self.load_dataframe("Tab2")
        for key, arm in self.arms.items():
            dset = DataSet.from_df(df[df.label == arm.label_plasma], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig1_{key}"] = dset

            # Ae(0-24)
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
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # 40 mg pravastatin sodium, fasted
                    "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "LI__f_OATP1B1": Q(arm.f_oatp1b1, "dimensionless"),
                    "KI__f_OAT3": Q(arm.f_oat3, "dimensionless"),
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
            name=f"{self.__class__.__name__} (healthy, fasted, gemfibrozil)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_xaxis(self.label_time, unit="hr", max=13)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_xaxis(self.label_time, unit="hr", max=13)
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
                    label=f"{arm.label}, Ae(0-24)" if urine else arm.label,
                    color=arm.color,
                    marker="s" if key == "placebo" else "o",
                    linestyle="" if urine else "--",
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Kyrklund2003a, output_dir=Kyrklund2003a.__name__)
