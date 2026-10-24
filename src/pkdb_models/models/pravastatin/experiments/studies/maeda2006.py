"""Simulation experiment of the study Maeda2006."""

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


class Maeda2006(PravastatinSimulationExperiment):
    """Simulation experiment of Maeda2006.

    23 healthy Japanese men (20-35 yr, 50-80 kg) grouped by the SLCO1B1
    (OATP1B1) haplotype (*1a/*1a n=5, *1b/*1b n=7, *1a/*15 n=6, *1b/*15 n=5)
    took a single 10 mg tablet of pravastatin sodium (Mevalotin) after an
    overnight fast (valsartan and temocapril in other phases). Plasma to 24 h
    (Fig1AB, mean and SD).

    Every haplotype is simulated with its OATP1B1 activity (`slco1b1_map`).
    The ranking of this cohort contradicts the European cohorts (Niemi2004,
    Mwinyi2004): *1b/*15 has the lowest AUC (0.52 of *1a/*1a), *1a/*15 the
    same as *1a/*1a (0.95) and *1b/*1b 0.65, while the activities of the
    alleles predict an increased AUC for the *15 carriers. The variant curves
    are validation of a limitation of the model, not training data.
    """

    #: the SLCO1B1 haplotypes of Fig1AB (key of the dataset: genotype of the
    #: activity map, genotype of the metadata)
    genotypes: ClassVar[dict[str, tuple[str, Genotype]]] = {
        "1a1a": ("*1a/*1a", Genotype.SLCO1B1_WILD_TYPE),
        "1b1b": ("*1b/*1b", Genotype.SLCO1B1_POLYMORPHISM),
        "1a15": ("*1a/*15", Genotype.SLCO1B1_521TC),
        "1b15": ("*1b/*15", Genotype.SLCO1B1_521TC),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1AB")
        # the means of zero after the dose (24 h) are below the limit of
        # quantification, not measurements
        df = df[(df.time == 0) | (df["mean"] > 0)]
        for key in self.genotypes:
            dset = DataSet.from_df(df[df.label == f"Fig1AB_{key}"], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig1AB_{key}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            f"pra10_{key}": Simulation(
                start=0,
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # 10 mg pravastatin sodium, fasted
                    "PODOSE_pra": Q(10, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "LI__f_OATP1B1": Q(self.slco1b1_map[variant], "dimensionless"),
                },
            )
            for key, (variant, _) in self.genotypes.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, (_, genotype) in self.genotypes.items():
            mappings[f"fm_pra10po_Fig1AB_{key}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1AB_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_pra10_{key}", xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
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
            num_cols=2,
            name=f"{self.__class__.__name__} (healthy, fasted, SLCO1B1)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_xaxis(self.label_time, unit="hr", max=14)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-4)

        for plot in plots:
            for key, (variant, _) in self.genotypes.items():
                color = self.slco1b1_colors[variant]
                plot.add_data(
                    task=f"task_pra10_{key}",
                    xid="time",
                    yid="[Cve_pra]",
                    label=f"Sim {variant}",
                    color=color,
                )
                plot.add_data(
                    dataset=f"Fig1AB_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"SLCO1B1 {variant}",
                    color=color,
                    marker="s",
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Maeda2006, output_dir=Maeda2006.__name__)
