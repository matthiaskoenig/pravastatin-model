"""Simulation experiment of the study Pan1990."""

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


class Pan1990(PravastatinSimulationExperiment):
    """Simulation experiment of Pan1990.

    33 men with primary hypercholesterolemia, randomized to 5, 10 or 20 mg
    pravastatin sodium twice daily (n=11 per dose) for 4 weeks, taken before
    the morning and the evening meal, then the same dose with cholestyramine
    24 g/day for 4 more weeks. Fig1 is the serum after the morning dose at the
    steady state of week 4 (the 56th dose). The single dose (week 0) and the
    arm with cholestyramine (week 8, which binds pravastatin in the gut, a
    process the model does not have) are only in Table 2.
    """

    doses: ClassVar[list[int]] = [5, 10, 20]
    colors: ClassVar[dict[int, str]] = {
        5: "tab:blue",
        10: "tab:orange",
        20: "tab:red",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1"]:
            df = self.load_dataframe(fig_id)
            for label, df_label in df.groupby("intervention"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.pra)
                dsets[f"{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        # twice daily dosing for 4 weeks: 56 doses, the first one at the start
        # and the last one, the profiled morning dose of week 4, at time 0
        time_repeats = 4 * 7 * 2
        time_delta = 12 * 60  # [min]
        end = (time_repeats - 1) * time_delta + 13 * 60
        for dose in self.doses:
            dose_na = Q(dose, "mg") * self.Mr.pra / self.Mr.pra_na
            simulations[f"pra_{dose}"] = Simulation(
                start=0,
                end=end,
                # every 3 min, the change times are on the grid
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_pra": dose_na,
                },
                changes=[
                    self.add_doses(
                        [k * time_delta for k in range(1, time_repeats)],
                        {"PODOSE_pra": dose_na},
                    ),
                ],
                time_shift=-(time_repeats - 1) * time_delta,
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for dose in self.doses:
            mappings[f"fm_pra{dose}po_pra"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig1_PRA{dose}_twice",
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self, task=f"task_pra_{dose}", xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.MULTIPLE,
                    # before the morning meal
                    fasting=Fasting.FASTED,
                    health=Health.PRIMARY_HYPERCHOLESTEROLEMIA,
                    coadministration=Coadministration.NONE,
                    genotype=Genotype.NR,
                ),
            )

        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig1_control_multiple_dose",
            name=f"{self.__class__.__name__} (twice daily, week 4)",
            # the legend inside would cover the peaks of the data
            settings={"legend_position": "outside"},
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="day", min=-2, max=0.8), legend=True
        )
        plots[0].set_yaxis(self.label_pra, unit="µM")

        for dose in self.doses:
            plots[0].add_data(
                task=f"task_pra_{dose}",
                xid="time",
                yid="[Cve_pra]",
                label=f"Sim {dose} mg",
                color=self.colors[dose],
            )
            plots[0].add_data(
                dataset=f"Fig1_PRA{dose}_twice",
                xid="time",
                yid="mean",
                count="count",
                label=f"{dose} mg",
                color=self.colors[dose],
                marker="s",
                linestyle="",
            )

        return self.figures_by_sid(fig)
