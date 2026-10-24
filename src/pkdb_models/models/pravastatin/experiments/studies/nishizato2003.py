"""Simulation experiment of the study Nishizato2003."""

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


class Nishizato2003(PravastatinSimulationExperiment):
    """Simulation experiment of Nishizato2003.

    Single oral dose of 10 mg pravastatin sodium (Mevalotin tablet) with 150 ml
    water after an overnight fast in 23 healthy Japanese men (52.4-97.8 kg) of
    seven OATP1B1 (SLCO1B1) genotypes; serum to 24 hr (Fig1: *1b/*1b n=4,
    *1b/*15 n=9, *15/*15 n=1, without SD). The urinary amounts of Tab6b are not
    measured values of the paper: the curation calculated them from the renal
    clearance, the AUC and an assumed body weight of 75.1 kg
    (`Ae = CLr * BW * AUC`, 20 % of the dose for *1a/*1a, 43 % for *15/*15).
    The allele *16 (Asn130Asp, Asn151Ser) has no 521C and a normal total
    clearance (*1b/*16 2.55 l/kg/hr, *1b/*1b 2.39), it is simulated with the
    activity of the wildtype allele.
    """

    #: the activity of OATP1B1 of a genotype of the study
    genotypes: ClassVar[dict[str, str]] = {
        "slco1b1_1a_1a": "*1a/*1a",
        "slco1b1_1a_1b": "*1a/*1b",
        "slco1b1_1b_1b": "*1b/*1b",
        "slco1b1_1b_15": "*1b/*15",
        "slco1b1_15_15": "*15/*15",
        # *16 without 521C: the activity of *1a/*1b
        "slco1b1_1b_16": "*1a/*1b",
    }
    labels_group: ClassVar[dict[str, str]] = {
        "slco1b1_1a_1a": "*1a/*1a",
        "slco1b1_1a_1b": "*1a/*1b",
        "slco1b1_1b_1b": "*1b/*1b",
        "slco1b1_1b_15": "*1b/*15",
        "slco1b1_15_15": "*15/*15",
        "slco1b1_1b_16": "*1b/*16",
    }
    colors: ClassVar[dict[str, str]] = {
        "slco1b1_1a_1a": "black",
        "slco1b1_1a_1b": "tab:blue",
        "slco1b1_1b_1b": "blue",
        "slco1b1_1b_15": "tab:orange",
        "slco1b1_15_15": "red",
        "slco1b1_1b_16": "tab:cyan",
    }
    #: the groups of the serum data (Fig1) and of the urinary amounts (Tab6b);
    #: the group with an unidentified genotype is not simulated
    groups_serum: ClassVar[list[str]] = [
        "slco1b1_1b_1b",
        "slco1b1_1b_15",
        "slco1b1_15_15",
    ]
    groups_urine: ClassVar[list[str]] = [
        "slco1b1_1a_1a",
        "slco1b1_1a_1b",
        "slco1b1_1b_1b",
        "slco1b1_1b_15",
        "slco1b1_15_15",
        "slco1b1_1b_16",
    ]

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1", "Tab6b"]:
            df = self.load_dataframe(fig_id)
            if fig_id == "Fig1":
                for label, df_label in df.groupby("label"):
                    label = str(label)
                    dset = DataSet.from_df(df_label, self.ureg)
                    dset.unit_conversion("mean", 1 / self.Mr.pra)
                    dsets[self.to_sid(f"{fig_id}_{label}")] = dset
            elif fig_id == "Tab6b":
                for group, df_group in df.groupby("group"):
                    group = str(group)
                    df_group_cum_amount = df_group[
                        df_group["measurement_type"] == "cumulative amount"
                    ]
                    dset = DataSet.from_df(df_group_cum_amount, self.ureg)
                    # µg to µmole
                    dset.unit_conversion("mean", 1 / self.Mr.pra)
                    dsets[self.to_sid(f"{fig_id}_{group}")] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            self.to_sid(f"pra_10_{group}"): Simulation(
                start=0,
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # pravastatin sodium
                    "PODOSE_pra": Q(10, "mg") * self.Mr.pra / self.Mr.pra_na,
                    "LI__f_OATP1B1": Q(self.slco1b1_map[genotype], "dimensionless"),
                },
            )
            for group, genotype in self.genotypes.items()
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for fig_id, groups in [
            ("Fig1", self.groups_serum),
            ("Tab6b", self.groups_urine),
        ]:
            serum = fig_id == "Fig1"
            for group in groups:
                dset_id = f"{fig_id}_{group}"
                mappings[self.to_sid(f"fm_pra10po_{dset_id}")] = FitMapping(
                    self,
                    reference=FitData(
                        self,
                        dataset=self.to_sid(dset_id),
                        xid="time",
                        yid="mean",
                        # the serum data has no SD, the SD of the urinary
                        # amounts is that of the renal clearance
                        yid_sd=None if serum else "mean_sd",
                        count="count",
                    ),
                    observable=FitData(
                        self,
                        task=self.to_sid(f"task_pra_10_{group}"),
                        xid="time",
                        yid="[Cve_pra]" if serum else "Aurine_pra",
                    ),
                    metadata=PKPDMappingMetaData(
                        tissue=Tissue.SERUM if serum else Tissue.URINE,
                        route=Route.PO,
                        application_form=ApplicationForm.TABLET,
                        dosing=Dosing.SINGLE,
                        fasting=Fasting.FASTED,
                        health=Health.HEALTHY,
                        coadministration=Coadministration.NONE,
                        genotype=Genotype.SLCO1B1_WILD_TYPE
                        if group == "slco1b1_1a_1a"
                        else Genotype.SLCO1B1_POLYMORPHISM,
                    ),
                )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1",
            name=f"{self.__class__.__name__} (10 mg, tablet)",
            num_rows=1,
            num_cols=2,
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra_urine, unit="µmole")

        for k, (fig_id, groups, yid) in enumerate(
            [
                ("Fig1", self.groups_serum, "[Cve_pra]"),
                ("Tab6b", self.groups_urine, "Aurine_pra"),
            ]
        ):
            for group in groups:
                label = self.labels_group[group]
                plots[k].add_data(
                    task=self.to_sid(f"task_pra_10_{group}"),
                    xid="time",
                    yid=yid,
                    label=f"Sim {label}",
                    color=self.colors[group],
                )
                plots[k].add_data(
                    dataset=self.to_sid(f"{fig_id}_{group}"),
                    xid="time",
                    yid="mean",
                    yid_sd=None if fig_id == "Fig1" else "mean_sd",
                    count="count",
                    label=label,
                    color=self.colors[group],
                    marker="s",
                    linestyle="",
                )

        return self.figures_by_sid(fig)
