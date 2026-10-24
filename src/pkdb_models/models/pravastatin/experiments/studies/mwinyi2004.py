"""Simulation experiment of the study Mwinyi2004."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
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
    PravastatinSimulationExperiment,
)


class Mwinyi2004(PravastatinSimulationExperiment):
    """Simulation experiment of Mwinyi2004.

    30 healthy white men grouped by the SLCO1B1 (OATP-C) haplotype (*1a/*1a
    n=10; *1a/*1b n=8 and *1b/*1b n=2; *1a/*5 n=10) took a single 40 mg dose
    of pravastatin sodium (Bristol-Myers Squibb) with 200 ml water after an
    overnight fast. Plasma by HPLC to 24 h (Fig1, mean and SEM), urine 0-12 h
    (Ae(0-12) of Table II, mean and SD).

    Every group is simulated with its OATP1B1 activity (`slco1b1_map`); the
    group of *1a/*1b and *1b/*1b with the activity of `(*1a+1b)/*1b`.
    """

    #: the SLCO1B1 haplotypes (key of the dataset: genotype of the activity
    #: map, label, genotype of the metadata)
    genotypes: ClassVar[dict[str, tuple[str, str, Genotype]]] = {
        "1a1a": ("*1a/*1a", "*1a/*1a", Genotype.SLCO1B1_WILD_TYPE),
        "1a1b_1b1b": (
            "(*1a+1b)/*1b",
            "*1a/*1b and *1b/*1b",
            Genotype.SLCO1B1_POLYMORPHISM,
        ),
        "1a5": ("*1a/*5", "*1a/*5", Genotype.SLCO1B1_521TC),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        df_urine = self.load_dataframe("Fig2_Ae_Mean")
        df_urine = df_urine[df_urine.measurement_type == "cumulative amount"]
        for key in self.genotypes:
            for dset_id, df_dset in [
                (f"Fig1_{key}", df[df.label == f"Fig1_{key}"]),
                (
                    f"Fig2_{key}_urine",
                    df_urine[df_urine.label == f"Fig2_{key}_urine"],
                ),
            ]:
                dset = DataSet.from_df(df_dset, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.pra)
                dsets[dset_id] = dset

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
                    "LI__f_OATP1B1": Q(self.slco1b1_map[variant], "dimensionless"),
                },
            )
            for key, (variant, _, _) in self.genotypes.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, (_, _, genotype) in self.genotypes.items():
            for dset_id, yid, tissue in [
                (f"Fig1_{key}", "[Cve_pra]", Tissue.PLASMA),
                (f"Fig2_{key}_urine", "Aurine_pra", Tissue.URINE),
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
                        genotype=genotype,
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
            name=f"{self.__class__.__name__} (healthy, fasted, SLCO1B1)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_xaxis(self.label_time, unit="hr", max=12)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-4)
        plots[2].set_yaxis(self.label_pra_urine, unit="µmole")

        for key, (variant, label, _) in self.genotypes.items():
            color = self.slco1b1_colors[variant]
            for k, plot in enumerate(plots):
                urine = k == 2
                plot.add_data(
                    task=f"task_pra40_{key}",
                    xid="time",
                    yid="Aurine_pra" if urine else "[Cve_pra]",
                    label=f"Sim {label}",
                    color=color,
                )
                plot.add_data(
                    dataset=f"Fig2_{key}_urine" if urine else f"Fig1_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"SLCO1B1 {label}, Ae(0-12)" if urine else f"SLCO1B1 {label}",
                    color=color,
                    marker="s",
                    linestyle="" if urine else "--",
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Mwinyi2004, output_dir=Mwinyi2004.__name__)
