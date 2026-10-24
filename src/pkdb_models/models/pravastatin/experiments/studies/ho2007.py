"""Simulation experiment of the study Ho2007."""

from typing import ClassVar, NamedTuple, override

from pkpdsim.metadata import (
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


class Group(NamedTuple):
    """A group of the study: a SLCO1B1 c.521T>C genotype or an ethnicity."""

    #: the SLCO1B1 genotype of the simulation (`slco1b1_map`)
    variant: str
    genotype: Genotype
    label: str
    marker: str


class Ho2007(PravastatinSimulationExperiment):
    """Simulation experiment of Ho2007.

    A single oral dose of 40 mg pravastatin (sodium) with water after an
    overnight fast in 107 healthy adults (69 European-Americans, 38
    African-Americans); plasma by HPLC-UV (LOD 5 ng/ml for the first 73
    subjects, 1 ng/ml later). The SLCO1B1 c.521T>C genotypes (T/T n=88: *1a/*1a,
    *1a/*1b, *1b/*1b; T/C n=17: *1a/*5, *1a/*15, *1b/*15; C/C n=2: *15/*15)
    are simulated with the OATP1B1 activities of `slco1b1_map`. The groups by
    ethnicity are the same subjects again (simulated as 521T/T).

    The majority of the concentrations at 6, 8 and 12 hr were below the
    detection limits (the paper reports AUC0-5), the data from 6 hr on is left
    out.
    """

    #: the groups by the label of the data
    groups: ClassVar[dict[str, Group]] = {
        "TT": Group("521T/T", Genotype.SLCO1B1_521TT, "SLCO1B1 c.521T/T", "o"),
        "TC": Group("521T/C", Genotype.SLCO1B1_521TC, "SLCO1B1 c.521T/C", "s"),
        "CC": Group("521C/C", Genotype.SLCO1B1_521CC, "SLCO1B1 c.521C/C", "^"),
        "EuropeanAmericans": Group("521T/T", Genotype.NR, "European-Americans", "s"),
        "AfricanAmericans": Group("521T/T", Genotype.NR, "African-Americans", "^"),
    }

    #: the concentrations from this time on are mostly below the LOD [hr]
    t_lod: ClassVar[float] = 6.0

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        df = df[df.time < self.t_lod]
        for label in self.groups:
            dset = DataSet.from_df(df[df.label == label], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig1_{label}"] = dset

        return dsets

    @staticmethod
    def task_key(variant: str) -> str:
        """Key of the simulation of a SLCO1B1 c.521 genotype."""
        return f"pra_40_{variant.replace('/', '')}"

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            self.task_key(variant): Simulation(
                start=0,
                end=13 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "LI__f_OATP1B1": Q(self.slco1b1_map[variant], "dimensionless"),
                },
            )
            for variant in ["521T/T", "521T/C", "521C/C"]
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        return {
            f"fm_pra40po_Fig1_{label}": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self,
                    task=f"task_{self.task_key(group.variant)}",
                    xid="time",
                    yid="[Cve_pra]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.HEALTHY,
                    genotype=group.genotype,
                ),
            )
            for label, group in self.groups.items()
        }

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        for fig_key, labels in {
            "control": ["TT", "EuropeanAmericans", "AfricanAmericans"],
            "variants": ["TT", "TC", "CC"],
        }.items():
            sid = f"Fig1_{fig_key}"
            fig = Figure(experiment=self, sid=sid, num_rows=1, num_cols=1)
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )
            plots[0].set_yaxis(self.label_pra, unit="µM", min=-0.025, max=0.3)

            variants = dict.fromkeys(self.groups[label].variant for label in labels)
            for variant in variants:
                plots[0].add_data(
                    task=f"task_{self.task_key(variant)}",
                    xid="time",
                    yid="[Cve_pra]",
                    label=f"Sim: SLCO1B1 c.{variant} (PRA 40mg)",
                    linestyle="-",
                    color=self.slco1b1_colors[variant],
                )
            for label in labels:
                group = self.groups[label]
                plots[0].add_data(
                    dataset=f"Fig1_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    marker=group.marker,
                    label=f"Ho2007: {group.label}",
                    color=self.slco1b1_colors[group.variant]
                    if fig_key == "variants"
                    else "black",
                )
            figures[sid] = fig

        return figures
