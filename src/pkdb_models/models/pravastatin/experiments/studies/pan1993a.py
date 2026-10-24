"""Simulation experiment of the study Pan1993a."""

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


class Pan1993a(PravastatinSimulationExperiment):
    """Simulation experiment of Pan1993a.

    Single oral dose of 20 mg pravastatin sodium (two 10 mg tablets) after an
    overnight fast in 70 healthy subjects of five groups: young men (n=10),
    elderly men (n=15, 65-75 yr), young women with a tubal ligation (TL, n=14
    in the pharmacokinetics), young women on combination oral contraceptives
    (OC, n=13) and elderly women (n=12). Serum at 0.33 to 48 hr (Fig1). The
    oral contraceptives have no effect (the conclusion of the study), the
    elderly have a higher AUC (+27 % men, +43 % women), which the model does not
    describe (no age).
    """

    #: the groups of the data
    groups: ClassVar[list[str]] = [
        "young_men",
        "elderly_men",
        "women_tl",
        "women_oc",
        "elderly_women",
    ]
    labels_group: ClassVar[dict[str, str]] = {
        "young_men": "young men",
        "elderly_men": "elderly men",
        "women_tl": "young women (TL)",
        "women_oc": "young women (OC)",
        "elderly_women": "elderly women",
    }
    colors: ClassVar[dict[str, str]] = {
        "young_men": "black",
        "elderly_men": "tab:blue",
        "women_tl": "tab:red",
        "women_oc": "tab:orange",
        "elderly_women": "tab:purple",
    }
    markers: ClassVar[dict[str, str]] = {
        "young_men": "^",
        "elderly_men": "s",
        "women_tl": "<",
        "women_oc": "o",
        "elderly_women": "v",
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
                dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "pra_20_po": Simulation(
                start=0,
                end=49 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # pravastatin sodium
                    "PODOSE_pra": Q(20, "mg") * self.Mr.pra / self.Mr.pra_na,
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for group in self.groups:
            mappings[f"fm_pra20po_{group}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_{group}",
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_pra_20_po", xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.HEALTHY,
                    coadministration=Coadministration.ORAL_CONTRACEPTIVES
                    if group == "women_oc"
                    else Coadministration.NONE,
                    genotype=Genotype.NR,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1_control",
            name=f"{self.__class__.__name__} (20 mg, tablet)",
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_pra, unit="µM")

        plots[0].add_data(
            task="task_pra_20_po",
            xid="time",
            yid="[Cve_pra]",
            label="Sim 20 mg",
            color="black",
        )
        for group in self.groups:
            plots[0].add_data(
                dataset=f"Fig1_{group}",
                xid="time",
                yid="mean",
                count="count",
                label=self.labels_group[group],
                color=self.colors[group],
                marker=self.markers[group],
                linestyle="",
            )

        return self.figures_by_sid(fig)
