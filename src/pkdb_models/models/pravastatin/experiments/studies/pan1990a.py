"""Simulation experiment of the study Pan1990a."""

from typing import override

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


class Pan1990a(PravastatinSimulationExperiment):
    """Simulation experiment of Pan1990a.

    Randomized two-way crossover in 20 healthy men (76.4 kg): 40 mg pravastatin
    sodium (two 20 mg tablets) once daily for 7 days in the morning after an
    overnight fast (and a fast of at least 1 hr after the dose), and 40 mg
    lovastatin for 7 days, with a washout of 7 days. Serum after the last dose
    of pravastatin (day 7, Fig2).
    """

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig2"]:
            df = self.load_dataframe(fig_id)
            # intact pravastatin (GC/MS); the active and total HMG-CoA reductase
            # inhibitors (bioassay) and the metabolites are not in the model
            df_pra40 = df[
                (df.intervention == "PRA_40_D7") & (df.label == "pravastatin")
            ]
            dset = DataSet.from_df(df_pra40, self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"{fig_id}_PRA_40"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        # once daily dosing of pravastatin for 7 days, the last day is 25 hr
        time_repeats = 7
        time_delta = 24 * 60  # [min]
        dose = Q(40, "mg") * self.Mr.pra / self.Mr.pra_na  # pravastatin sodium
        end = (time_repeats - 1) * time_delta + 25 * 60
        return {
            "pra_40": Simulation(
                start=0,
                end=end,
                # every 3 min, the change times are on the grid
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_pra": dose,
                },
                changes=[
                    self.add_doses(
                        [k * time_delta for k in range(1, time_repeats)],
                        {"PODOSE_pra": dose},
                    ),
                ],
                time_shift=-(time_repeats - 1) * time_delta,
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        return {
            "fm_pra40po_pra": FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset="Fig2_PRA_40",
                    xid="time",
                    yid="mean",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_pra_40", xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.MULTIPLE,
                    fasting=Fasting.FASTED,
                    health=Health.HEALTHY,
                    coadministration=Coadministration.NONE,
                    genotype=Genotype.NR,
                ),
            ),
        }

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig2_control_multiple_dose",
            name=f"{self.__class__.__name__} (40 mg once daily, day 7)",
        )
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="day", min=-6.5), legend=True
        )
        plots[0].set_yaxis(self.label_pra, unit="µM")

        plots[0].add_data(
            task="task_pra_40",
            xid="time",
            yid="[Cve_pra]",
            label="Sim 40 mg",
            color="black",
        )
        plots[0].add_data(
            dataset="Fig2_PRA_40",
            xid="time",
            yid="mean",
            count="count",
            label="40 mg (day 7)",
            color="black",
            marker="s",
            linestyle="",
        )

        return self.figures_by_sid(fig)
