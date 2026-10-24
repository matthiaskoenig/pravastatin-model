"""Simulation experiment of the study Becquemont1999."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    Dosing,
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


class Becquemont1999(PravastatinSimulationExperiment):
    """Simulation experiment of Becquemont1999.

    Open-label study of 16 days in 12 healthy volunteers (7 M / 5 F): 40 mg
    pravastatin (sodium) orally on day 1 alone, on day 8 with mibefradil
    100 mg/day (from day 3 to day 16) and once daily on days 11 to 16 with
    mibefradil; plasma profiles (LC-MS/MS, LOD 5 ng/ml) on days 1, 8 and 16.
    Food is not reported. Mibefradil had no significant effect (AUC ratio
    1.32 on day 8).

    The experiment simulates the single dose of day 1. The concentrations at
    12 and 24 hr are below the LOD (only one subject was detectable) and
    are left out. The mibefradil profiles (days 8 and 16) are shown with the
    simulation of the control but not mapped: mibefradil is no member of the
    vocabulary of the coadministrations, and pravastatin is not metabolized by
    CYP3A4 (no interaction is expected).
    """

    #: the labels of the data and their days of the profile
    days: ClassVar[dict[str, str]] = {"D1": "day 1", "D8": "day 8", "D16": "day 16"}

    #: the concentrations from this time on are below the LOD [hr]
    t_lod: ClassVar[float] = 12.0

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        df = df[df.time < self.t_lod]
        for label in self.days:
            dset = DataSet.from_df(df[df.label == label], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig1_PRA_40_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "pra_40": Simulation(
                start=0,
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        return {
            "fm_pra40po_pra": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig1_PRA_40_D1",
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
                    dosing=Dosing.SINGLE,
                    health=Health.HEALTHY,
                    genotype=Genotype.NR,
                ),
            ),
        }

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        colors = {"D1": "black", "D8": "tab:blue", "D16": "tab:red"}
        for fig_key, labels in {
            "control": ["D1"],
            "mibefradil": ["D1", "D8", "D16"],
        }.items():
            sid = f"Fig1_{fig_key}"
            fig = Figure(experiment=self, sid=sid, num_rows=1, num_cols=1)
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )
            plots[0].set_yaxis(self.label_pra, unit="µM")
            plots[0].add_data(
                task="task_pra_40",
                xid="time",
                yid="[Cve_pra]",
                label="Sim: control (PRA 40mg)",
                linestyle="-",
                color="black",
            )
            for label in labels:
                mibefradil = "" if label == "D1" else " with mibefradil"
                plots[0].add_data(
                    dataset=f"Fig1_PRA_40_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Becquemont1999: {self.days[label]}{mibefradil}",
                    color=colors[label],
                )
            figures[sid] = fig

        return figures
