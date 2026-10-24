"""Simulation experiment of the study Keskitalo2009."""

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


class Keskitalo2009(PravastatinSimulationExperiment):
    """Simulation experiment of Keskitalo2009.

    32 healthy subjects grouped by the ABCG2 (BCRP) c.421C>A genotype (C/C
    n=23, C/A n=4, A/A n=5) took single oral doses of 40 mg of fluvastatin, of
    pravastatin (tablet of pravastatin sodium, Pravachol) and of simvastatin in
    three phases of a fixed order, at least one week apart, with 150 ml water
    after an overnight fast; a warm meal 4 h after the dose. Plasma by LC-MS/MS
    to 12 h (Fig1, mean and SEM).

    The ABCG2 genotype had no effect on pravastatin (AUC of A/A 12 % lower than
    C/C, not significant); the model has no BCRP and simulates every genotype
    as the reference. The SLCO1B1 c.521T>C genotype is not balanced between the
    groups: all four C/A subjects, four of the five A/A subjects and 7 of the 23
    C/C subjects are 521TC (521CC was excluded), so the small C/A and A/A groups
    are population validation, not training data.
    """

    #: the ABCG2 genotypes of Fig1 (key of the dataset: label of the data,
    #: genotype)
    genotypes: ClassVar[dict[str, tuple[str, Genotype]]] = {
        "CC": ("pravastatin_c.421C/C", Genotype.ABCG2_421CC),
        "CA": ("pravastatin_c.421C/A", Genotype.ABCG2_421CA),
        "AA": ("pravastatin_c.421A/A", Genotype.ABCG2_421AA),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for key, (label, _) in self.genotypes.items():
            df_pra40 = df[(df.intervention == "PRA_40mg") & (df.label == label)]
            dset = DataSet.from_df(df_pra40, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig1_{key}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "pra_40": Simulation(
                start=0,
                end=13.5 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # 40 mg pravastatin sodium, fasted
                    "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, (_, genotype) in self.genotypes.items():
            mappings[f"fm_pra40po_Fig1_{key}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_pra_40", xid="time", yid="[Cve_pra]"
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
            name=f"{self.__class__.__name__} (healthy, fasted, ABCG2 c.421C>A)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-3)

        for plot in plots:
            plot.add_data(
                task="task_pra_40",
                xid="time",
                yid="[Cve_pra]",
                label="Sim 40 mg",
                color="black",
            )
            for key in self.genotypes:
                genotype = f"421{key[0]}/{key[1]}"
                plot.add_data(
                    dataset=f"Fig1_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"ABCG2 {genotype}",
                    color=self.abcg2_colors[genotype],
                    marker="s",
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Keskitalo2009, output_dir=Keskitalo2009.__name__)
