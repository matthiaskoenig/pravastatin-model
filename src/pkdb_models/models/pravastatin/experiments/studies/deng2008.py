"""Simulation experiment of the study Deng2008."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
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

from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
)


class Deng2008(PravastatinSimulationExperiment):
    """Simulation experiment of Deng2008.

    Randomized crossover of pravastatin and pitavastatin in 11 healthy Korean
    men selected by their SLCO1B1 genotype (*1a/*1a n=6, *15/*15 n=5): a single
    oral dose of 40 mg pravastatin (sodium, Mevalotin tablet) with 240 ml
    water after an overnight fast, food 4 hr after the dose; plasma by LC-MS/MS
    (LLOQ 1 ng/ml). Only pravastatin is simulated. *15/*15 (c.388A>G and
    c.521T>C homozygous) is simulated with the OATP1B1 activity of 521C/C
    (`slco1b1_map`).

    The data of 0 to 6 hr are Fig 2a (linear axis), the terminal phase (12 and
    24 hr) is digitized from the semilog Fig 2c, whose caption swaps the
    symbols of the genotypes (the legend of the panel is right).
    """

    #: the SLCO1B1 genotype of the data label
    variants: ClassVar[dict[str, str]] = {
        "1a1a_pra": "*1a/*1a",
        "1515_pra": "*15/*15",
    }

    #: the genotype of the vocabulary of the data label
    genotypes: ClassVar[dict[str, Genotype]] = {
        "1a1a_pra": Genotype.SLCO1B1_WILD_TYPE,
        "1515_pra": Genotype.SLCO1B1_521CC,
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig2")
        for label in self.variants:
            dset = DataSet.from_df(df[df.label == label], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig2_{label}"] = dset

        return dsets

    @staticmethod
    def task_suffix(label: str) -> str:
        """Suffix of the simulation of a data label: `1a1a` or `1515`."""
        return label.removesuffix("_pra")

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            f"pra_40_{self.task_suffix(label)}": Simulation(
                start=0,
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "LI__f_OATP1B1": Q(self.slco1b1_map[variant], "dimensionless"),
                },
            )
            for label, variant in self.variants.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        return {
            f"fm_pra40po_Fig2_{label}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig2_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=f"task_pra_40_{self.task_suffix(label)}",
                    xid="time",
                    yid="[Cve_pra]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.HEALTHY,
                    genotype=self.genotypes[label],
                ),
            )
            for label in self.variants
        }

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        for fig_key, labels in {
            "control": ["1a1a_pra"],
            "variants": list(self.variants),
        }.items():
            sid = f"Fig2_{fig_key}"
            fig = Figure(experiment=self, sid=sid, num_rows=1, num_cols=2)
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )
            plots[0].set_yaxis(self.label_pra, unit="µM")
            plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-4)
            for plot in plots:
                for label in labels:
                    variant = self.variants[label]
                    color = self.slco1b1_colors[variant]
                    plot.add_data(
                        task=f"task_pra_40_{self.task_suffix(label)}",
                        xid="time",
                        yid="[Cve_pra]",
                        label=f"Sim: {variant} (PRA 40mg)",
                        linestyle="-",
                        color=color,
                    )
                    plot.add_data(
                        dataset=f"Fig2_{label}",
                        xid="time",
                        yid="mean",
                        yid_sd="mean_sd",
                        count="count",
                        label=f"Deng2008: SLCO1B1 {variant}",
                        color=color,
                        marker="s",
                    )
            figures[sid] = fig

        return figures
