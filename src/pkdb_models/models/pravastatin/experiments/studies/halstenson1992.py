"""Simulation experiment of the study Halstenson1992."""

from typing import ClassVar, NamedTuple, override

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


class Group(NamedTuple):
    """A group of the study by its creatinine clearance."""

    #: the label of the data
    data_label: str
    #: the class of the renal function (`renal_map`, `renal_colors`)
    impairment: str
    #: the measured creatinine clearance [ml/min/1.73 m2] (Table I)
    crcl: float


class Halstenson1992(PravastatinSimulationExperiment):
    """Simulation experiment of Halstenson1992.

    A single oral dose of 20 mg pravastatin (sodium) in 16 subjects in four
    groups of four by their 24 hr creatinine clearance (Table I: 101.0, 69.5,
    32.5 and 19.5 ml/min/1.73 m2), fasted from 10 hr before until 4 hr after
    the dose; serum and urine by GC/MS. The renal function of a group is its
    measured creatinine clearance relative to the GFR of 101 ml/min of the
    model (`KI__f_renal_function` = CrCl / 101), the colors are those of its
    class. The urinary excretion of 0 to 24 hr is the fraction of the dose of
    Table II (fe 12.3, 8.2, 4.1 and 0.8 %) as an amount of pravastatin sodium.
    """

    #: the groups by the label of the data
    groups: ClassVar[dict[str, Group]] = {
        "pra_gr1": Group("Halstenson1992: group I", "Normal renal function", 101.0),
        "pra_gr2": Group("Halstenson1992: group II", "Mild renal impairment", 69.5),
        "pra_gr3": Group(
            "Halstenson1992: group III", "Moderate renal impairment", 32.5
        ),
        "pra_gr4": Group("Halstenson1992: group IV", "Severe renal impairment", 19.5),
    }

    #: the creatinine clearance of the healthy GFR of the model [ml/min]
    crcl_healthy: ClassVar[float] = 101.0

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for label in self.groups:
            dset = DataSet.from_df(df[df.label == label], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig1_{label}"] = dset

        # the amount in the urine is the fraction of the dose of pravastatin
        # sodium (mg of the salt)
        df = self.load_dataframe("Tab2B")
        for label in self.groups:
            dset = DataSet.from_df(df[df.label == f"{label}_urine"], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra_na)
            dsets[f"Tab2B_{label}_urine"] = dset

        return dsets

    @staticmethod
    def task_key(label: str) -> str:
        """Key of the simulation of a group."""
        return f"pra_20_{label.removeprefix('pra_')}"

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            self.task_key(label): Simulation(
                start=0,
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_pra": Q(20, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "KI__f_renal_function": Q(
                        group.crcl / self.crcl_healthy, "dimensionless"
                    ),
                },
            )
            for label, group in self.groups.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        def metadata(label: str, tissue: Tissue) -> PKPDMappingMetaData:
            return PKPDMappingMetaData(
                tissue=tissue,
                route=Route.PO,
                application_form=ApplicationForm.TABLET,
                dosing=Dosing.SINGLE,
                fasting=Fasting.FASTED,
                health=Health.HEALTHY
                if label == "pra_gr1"
                else Health.RENAL_IMPAIRMENT,
                genotype=Genotype.NR,
            )

        mappings = {}
        for label in self.groups:
            task = f"task_{self.task_key(label)}"
            mappings[f"fm_pra20po_Fig1_{label}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_{label}",
                    xid="time",
                    yid="mean",
                    # the serum of group IV has no SD
                    yid_sd=None if label == "pra_gr4" else "mean_sd",
                    count="count",
                ),
                observable=FitData(self, task=task, xid="time", yid="[Cve_pra]"),
                metadata=metadata(label, Tissue.SERUM),
            )
            mappings[f"fm_pra20po_Tab2B_{label}_urine"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Tab2B_{label}_urine",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(self, task=task, xid="time", yid="Aurine_pra"),
                metadata=metadata(label, Tissue.URINE),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Fig1_Tab2"
        figures = {}
        for fig_type in ["variants", "control"]:
            sid = f"{name}_{fig_type}"
            fig = Figure(experiment=self, sid=sid, num_rows=1, num_cols=3)
            plots = fig.create_plots(
                xaxis=Axis(self.label_time, unit="hr"), legend=True
            )
            plots[0].set_yaxis(self.label_pra, unit="µM")
            plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-4)
            plots[2].set_yaxis(self.label_pra_urine, unit="µmole")

            for label, group in self.groups.items():
                if fig_type == "control" and label != "pra_gr1":
                    continue
                task = f"task_{self.task_key(label)}"
                color = self.renal_colors[group.impairment]
                sim_label = f"Sim: CrCl {group.crcl} ml/min (PRA 20mg)"
                for plot in plots[:2]:
                    plot.add_data(
                        task=task,
                        xid="time",
                        yid="[Cve_pra]",
                        label=sim_label,
                        linestyle="-",
                        color=color,
                    )
                    plot.add_data(
                        dataset=f"Fig1_{label}",
                        xid="time",
                        yid="mean",
                        yid_sd=None if label == "pra_gr4" else "mean_sd",
                        count="count",
                        label=group.data_label,
                        color=color,
                    )
                plots[2].add_data(
                    task=task,
                    xid="time",
                    yid="Aurine_pra",
                    label=sim_label,
                    linestyle="-",
                    color=color,
                )
                plots[2].add_data(
                    dataset=f"Tab2B_{label}_urine",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=group.data_label,
                    color=color,
                    linestyle="",
                )

            figures[sid] = fig

        return figures
