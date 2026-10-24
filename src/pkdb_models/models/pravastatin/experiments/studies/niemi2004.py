"""Simulation experiment of the study Niemi2004."""

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


class Niemi2004(PravastatinSimulationExperiment):
    """Simulation experiment of Niemi2004.

    Single oral dose of 40 mg pravastatin sodium (Pravachol tablet) with water
    after a fast of at least 1 hr in 41 healthy Finnish volunteers (24 women,
    17 men, 64.8 kg). The four panels of Fig1 group the same 41 subjects by the
    SLCO1B1 (OATP1B1) variants: (a) -11187G>A, (b) c.521T>C, (c) the haplotype
    *15B, (d) the haplotype *17 (mean and SEM). The *15B and *17 haplotypes
    carry 521C, the -11187A promoter variant is part of *17, so the carriers of
    a variant are simulated with the activity of OATP1B1 of a 521T/C genotype
    and the non-carriers of a haplotype with the wildtype (they include carriers
    of 521C of the other haplotypes). Niemi2006 regroups the same subjects.
    """

    #: the groups of Fig1 by panel
    panels: ClassVar[dict[str, list[str]]] = {
        "a": ["11187GG", "11187GA"],
        "b": ["521TT", "521TC", "521CC"],
        "c": ["NC15B", "HC15B"],
        "d": ["NC17", "HC17"],
    }
    #: the SLCO1B1 genotype which gives the activity of OATP1B1 of a group
    group_genotypes: ClassVar[dict[str, str]] = {
        "11187GG": "521T/T",
        "11187GA": "521T/C",
        "521TT": "521T/T",
        "521TC": "521T/C",
        "521CC": "521C/C",
        "NC15B": "521T/T",
        "HC15B": "521T/C",
        "NC17": "521T/T",
        "HC17": "521T/C",
    }
    #: the genotype of the metadata of a group: the reference groups of a panel
    #: are the wildtype of the variant of the panel
    group_metadata_genotypes: ClassVar[dict[str, Genotype]] = {
        "11187GG": Genotype.SLCO1B1_WILD_TYPE,
        "11187GA": Genotype.SLCO1B1_POLYMORPHISM,
        "521TT": Genotype.SLCO1B1_521TT,
        "521TC": Genotype.SLCO1B1_521TC,
        "521CC": Genotype.SLCO1B1_521CC,
        "NC15B": Genotype.SLCO1B1_WILD_TYPE,
        "HC15B": Genotype.SLCO1B1_POLYMORPHISM,
        "NC17": Genotype.SLCO1B1_WILD_TYPE,
        "HC17": Genotype.SLCO1B1_POLYMORPHISM,
    }
    labels_group: ClassVar[dict[str, str]] = {
        "11187GG": "-11187GG",
        "11187GA": "-11187GA",
        "521TT": "521TT",
        "521TC": "521TC",
        "521CC": "521CC",
        "NC15B": "non-carriers *15B",
        "HC15B": "heterozygous *15B",
        "NC17": "non-carriers *17",
        "HC17": "heterozygous *17",
    }
    markers: ClassVar[dict[str, str]] = {
        "521T/T": "o",
        "521T/C": "s",
        "521C/C": "^",
    }

    @staticmethod
    def task_suffix(genotype: str) -> str:
        """Suffix of the simulation of a genotype, `521T/C` is `521TC`."""
        return genotype.replace("/", "")

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id, study="Niemi2004")
            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.pra)
                dsets[self.to_sid(f"{fig_id}_{label}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        for genotype in sorted(set(self.group_genotypes.values())):
            simulations[self.to_sid(f"pra_40_{self.task_suffix(genotype)}")] = (
                Simulation(
                    start=0,
                    end=13 * 60,
                    preinit_changes={
                        **self.default_changes(),
                        # pravastatin sodium
                        "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                        "LI__f_OATP1B1": Q(self.slco1b1_map[genotype], "dimensionless"),
                    },
                )
            )

        return simulations

    def task_id(self, group: str) -> str:
        """Task of the simulation of a group of Fig1."""
        genotype = self.group_genotypes[group]
        return self.to_sid(f"task_pra_40_{self.task_suffix(genotype)}")

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for group in self.group_genotypes:
            mappings[self.to_sid(f"fm_pra40po_{group}")] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=self.to_sid(f"Fig1_{group}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task=self.task_id(group), xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.HEALTHY,
                    coadministration=Coadministration.NONE,
                    genotype=self.group_metadata_genotypes[group],
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            name=f"{self.__class__.__name__} (40 mg, tablet)",
            num_rows=2,
            num_cols=2,
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        for k, (panel, groups) in enumerate(self.panels.items()):
            plot = plots[k]
            plot.title = f"({panel})"
            plot.set_yaxis(self.label_pra, unit="µM")
            # one simulation per activity of OATP1B1 of the panel
            for genotype in dict.fromkeys(self.group_genotypes[g] for g in groups):
                plot.add_data(
                    task=self.to_sid(f"task_pra_40_{self.task_suffix(genotype)}"),
                    xid="time",
                    yid="[Cve_pra]",
                    label=f"Sim {genotype}",
                    color=self.slco1b1_colors[genotype],
                )
            for group in groups:
                genotype = self.group_genotypes[group]
                plot.add_data(
                    dataset=self.to_sid(f"Fig1_{group}"),
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=self.labels_group[group],
                    color=self.slco1b1_colors[genotype],
                    marker=self.markers[genotype],
                    linestyle="",
                )

        return self.figures_by_sid(fig)
