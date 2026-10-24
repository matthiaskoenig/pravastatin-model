"""Simulation experiment of the study Niemi2006."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
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

#: the MRP2 (ABCC2) mRNA is 95 % higher in livers with c.1446CG (Niemi2006);
#: the carriers have a 67 % lower AUC, which the model does not reproduce with
#: the activity of MRP2 (a limitation of the model)
F_MRP2_1446CG = 1.95


class Niemi2006(PravastatinSimulationExperiment):
    """Simulation experiment of Niemi2006.

    The 41 healthy volunteers of Niemi2004 after a single oral dose of 40 mg
    pravastatin sodium (the same measurements), grouped by SLCO1B1 *17 (n=3,
    the HC17 group of Niemi2004), the ABCC2 (MRP2) c.1446C>G variant
    (heterozygous, n=3, no *17) and neither (n=35). The *17 carriers are
    simulated with the activity of OATP1B1 of a 521T/C genotype, the c.1446CG
    carriers with the higher activity of MRP2 of `F_MRP2_1446CG`.
    """

    dset_ids: ClassVar[list[str]] = [
        "Fig1_no_SLCO1B1_17_c1446CC",
        "Fig1_SLCO1B1_17",
        "Fig1_c1446CG",
    ]
    #: the simulation of a dataset
    dset_tasks: ClassVar[dict[str, str]] = {
        "Fig1_no_SLCO1B1_17_c1446CC": "task_pra_40",
        "Fig1_SLCO1B1_17": "task_pra_40_slco1b1_17",
        "Fig1_c1446CG": "task_pra_40_abcc2_1446CG",
    }
    #: the genotype of the metadata: pkpdsim has no member of ABCC2, the
    #: c.1446CG carriers have no *17 (`NR` for the SLCO1B1 genotype); the
    #: reference group contains the 521C carriers of the other haplotypes
    genotypes: ClassVar[dict[str, Genotype]] = {
        "Fig1_no_SLCO1B1_17_c1446CC": Genotype.SLCO1B1_WILD_TYPE,
        "Fig1_SLCO1B1_17": Genotype.SLCO1B1_POLYMORPHISM,
        "Fig1_c1446CG": Genotype.NR,
    }
    labels_dset: ClassVar[dict[str, str]] = {
        "Fig1_no_SLCO1B1_17_c1446CC": "no *17, ABCC2 1446CC",
        "Fig1_SLCO1B1_17": "SLCO1B1 *17",
        "Fig1_c1446CG": "ABCC2 1446CG",
    }
    colors: ClassVar[dict[str, str]] = {
        "Fig1_no_SLCO1B1_17_c1446CC": "black",
        "Fig1_SLCO1B1_17": "tab:red",
        "Fig1_c1446CG": "tab:green",
    }
    markers: ClassVar[dict[str, str]] = {
        "Fig1_no_SLCO1B1_17_c1446CC": "o",
        "Fig1_SLCO1B1_17": "s",
        "Fig1_c1446CG": "^",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.pra)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        changes = {
            "pra_40": {},
            "pra_40_slco1b1_17": {
                "LI__f_OATP1B1": Q(self.slco1b1_map["*1a/*17"], "dimensionless"),
            },
            "pra_40_abcc2_1446CG": {
                "LI__f_MRP2": Q(F_MRP2_1446CG, "dimensionless"),
            },
        }
        return {
            sim_key: Simulation(
                start=0,
                end=13 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # pravastatin sodium
                    "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                    **sim_changes,
                },
            )
            for sim_key, sim_changes in changes.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for dset_id in self.dset_ids:
            mappings[self.to_sid(f"fm_pra40_{dset_id}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(dset_id),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=self.dset_tasks[dset_id], xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.HEALTHY,
                    coadministration=Coadministration.NONE,
                    genotype=self.genotypes[dset_id],
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            name=f"{self.__class__.__name__} (40 mg, tablet)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_pra, unit="µM")

        for dset_id in self.dset_ids:
            plots[0].add_data(
                task=self.dset_tasks[dset_id],
                xid="time",
                yid="[Cve_pra]",
                label=f"Sim {self.labels_dset[dset_id]}",
                color=self.colors[dset_id],
            )
            plots[0].add_data(
                dataset=self.to_sid(dset_id),
                xid="time",
                yid="mean",
                yid_sd="mean_sd",
                count="count",
                label=self.labels_dset[dset_id],
                color=self.colors[dset_id],
                marker=self.markers[dset_id],
                linestyle="",
            )

        return self.figures_by_sid(fig)
