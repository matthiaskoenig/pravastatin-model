"""Simulation experiment of the study Gustavson2005."""

from typing import ClassVar, NamedTuple, override

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


class Profile(NamedTuple):
    """A profile of the study: the day of the dose and the coadministration."""

    day: int
    coadministration: Coadministration
    label: str
    color: str


class Gustavson2005(PravastatinSimulationExperiment):
    """Simulation experiment of Gustavson2005.

    Open-label sequential multiple-dose study in 24 healthy white adults
    (17 M / 7 F, 75.8 kg): one 40 mg pravastatin (sodium) tablet once daily
    in the morning on days 1 to 15, about 30 min after the start of a
    standardized breakfast (`GU__fed` 1), fenofibrate 160 mg once daily added
    on days 6 to 15. Plasma by LC-MS/MS (LLOQ 0.1 ng/ml) over 24 hr on days 5,
    6 and 15; one subject withdrew on day 13 (n=23 on day 15).

    Fenofibrate raised the AUC by 25 % (day 6) and 31 % (day 15), which the
    authors call modest; it has no established transporter mechanism and is
    simulated as the control (`F_NO_INTERACTION` of the base experiment). The
    data of SQ 31906 (3alpha-hydroxy-iso-pravastatin, Fig 2) is not simulated,
    the model has no isomer.
    """

    #: the profiles by the label of the data
    profiles: ClassVar[dict[str, Profile]] = {
        "pra40_d5": Profile(5, Coadministration.NONE, "day 5", "black"),
        "pra40_fen160_d1": Profile(
            6, Coadministration.FENOFIBRATE, "day 6, fenofibrate", "tab:blue"
        ),
        "pra40_fen160_d10": Profile(
            15, Coadministration.FENOFIBRATE, "day 15, fenofibrate", "tab:red"
        ),
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig1")
        for label in self.profiles:
            dset = DataSet.from_df(df[df.label == label], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Fig1_{label}"] = dset

        return dsets

    @staticmethod
    def task_key(day: int) -> str:
        """Key of the simulation of the profile of a day."""
        return f"pra_40_d{day}"

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        dose = Q(40, "mg") * self.Mr.pra / self.Mr.pra_na
        time_delta = 24 * 60  # [min]
        for profile in self.profiles.values():
            # once daily doses with breakfast until the day of the profile,
            # which is 25 hr long and starts at time 0
            end = (profile.day - 1) * time_delta + 25 * 60
            simulations[self.task_key(profile.day)] = Simulation(
                start=0,
                end=end,
                # every 3 min, the change times are on the grid
                preinit_changes={
                    **self.default_changes(),
                    "GU__fed": Q(1, "dimensionless"),
                    "PODOSE_pra": dose,
                },
                changes=[
                    self.add_doses(
                        [k * time_delta for k in range(1, profile.day)],
                        {"PODOSE_pra": dose},
                    ),
                ],
                time_shift=-(profile.day - 1) * time_delta,
            )

        return simulations

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
                    task=f"task_{self.task_key(profile.day)}",
                    xid="time",
                    yid="[Cve_pra]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.MULTIPLE,
                    fasting=Fasting.FED,
                    health=Health.HEALTHY,
                    coadministration=profile.coadministration,
                    genotype=Genotype.NR,
                ),
            )
            for label, profile in self.profiles.items()
        }

    @override
    def figures(self) -> dict[str, Figure]:
        figures = {}
        for sid, labels, xaxis in [
            (
                "Fig1_control_multiple_dose",
                ["pra40_d5"],
                Axis(self.label_time, unit="day", min=-4.5),
            ),
            (
                "Fig1_fenofibrate",
                list(self.profiles),
                Axis(self.label_time, unit="hr", min=0, max=25),
            ),
        ]:
            fig = Figure(experiment=self, sid=sid, num_rows=1, num_cols=1)
            plots = fig.create_plots(xaxis=xaxis, legend=True)
            plots[0].set_yaxis(self.label_pra, unit="µM", max=0.09)
            for label in labels:
                profile = self.profiles[label]
                plots[0].add_data(
                    task=f"task_{self.task_key(profile.day)}",
                    xid="time",
                    yid="[Cve_pra]",
                    label=f"Sim: {profile.label} (PRA 40mg, fed)",
                    linestyle="-",
                    color=profile.color,
                )
                plots[0].add_data(
                    dataset=f"Fig1_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=f"Gustavson2005: {profile.label}",
                    color=profile.color,
                )
            figures[sid] = fig

        return figures
