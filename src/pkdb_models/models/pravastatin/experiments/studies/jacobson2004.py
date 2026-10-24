"""Simulation experiment of the study Jacobson2004."""

from typing import ClassVar, NamedTuple, override

from pkpdsim.metadata import (
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
    F_NO_INTERACTION,
    F_OATP1B1_CLARITHROMYCIN,
    PravastatinSimulationExperiment,
)


class Profile(NamedTuple):
    """A profile of pravastatin of a trial of the study."""

    #: the figure and the label of the data
    fig_id: str
    data_label: str
    #: the days of the doses of pravastatin, the profile is of the last
    dose_days: tuple[int, ...]
    #: the doses were taken after breakfast (`GU__fed` 1)
    fed: bool
    #: the coadministered drug of the vocabulary, None for mibefradil (no
    #: member of the vocabulary, the profile is shown but not mapped)
    coadministration: Coadministration | None
    #: the label and the color of the figures
    label: str
    color: str
    #: the activity of OATP1B1 (`LI__f_OATP1B1`), the inhibition by the
    #: coadministered drug
    f_oatp1b1: float = F_NO_INTERACTION


#: once daily doses on days 1 to 7 and 10 to 17 (trials 2 and 4)
DAYS_1_7_10_17 = (*range(1, 8), *range(10, 18))


class Jacobson2004(PravastatinSimulationExperiment):
    """Simulation experiment of Jacobson2004.

    Four trials of 40 mg pravastatin (sodium) with CYP3A4 inhibitors in healthy
    adults, serum by LC-MS/MS (trial 3 by a radioenzymatic assay):

    1. verapamil (n=15 men): pravastatin on the mornings of days 1 and 5,
       verapamil 120 mg on day 2 and 480 mg extended-release on the evenings
       of days 2 to 4; profiles on day 1 (alone) and day 5 (Fig 1A, AUC
       ratio 1.31, not significant)
    2. mibefradil (n=15): pravastatin once daily in the morning on days 1 to 7
       and 10 to 17, mibefradil 100 mg on days 10 to 19; profiles on days 7
       and 17 (Fig 2A, AUC ratio 1.20, not significant)
    3. itraconazole (n=16 of 60): pravastatin with itraconazole 200 mg once
       daily for 30 days; profiles on day 1 ("alone", Fig 3 and Table 3) and
       day 30 of the active HMG-CoA reductase inhibitors before hydrolysis by
       a radioenzymatic assay, which is not the pravastatin of the model
    4. clarithromycin (n=15): pravastatin once daily after breakfast on days 1
       to 7 and 10 to 17, clarithromycin 500 mg twice daily on days 10 to 18;
       profiles on days 7 and 17 (Fig 4A, AUC ratio 2.10)

    Verapamil and itraconazole are simulated as the control (`F_NO_INTERACTION`
    of the base experiment: pravastatin is not metabolized by CYP3A4),
    clarithromycin inhibits OATP1B1 (`F_OATP1B1_CLARITHROMYCIN`, from day 1 of
    the simulation: the profile of day 17 depends only on the last days).
    Mibefradil is no member of the vocabulary of the coadministrations, its
    profile is shown but not mapped. Food is reported only for trial 4.
    """

    #: the profiles by the key of their dataset
    profiles: ClassVar[dict[str, Profile]] = {
        "Fig1_PRA1": Profile(
            "Fig1",
            "PRA1_pravastatin",
            (1,),
            False,
            Coadministration.NONE,
            "trial 1, day 1",
            "black",
        ),
        "Fig1_PRA1_VER": Profile(
            "Fig1",
            "PRA1,VER_pravastatin",
            (1, 5),
            False,
            Coadministration.VERAPAMIL,
            "trial 1, day 5, verapamil",
            "tab:red",
        ),
        "Fig2_PRA2": Profile(
            "Fig2",
            "PRA2_pravastatin",
            tuple(range(1, 8)),
            False,
            Coadministration.NONE,
            "trial 2, day 7",
            "black",
        ),
        "Fig2_PRA2_MIB": Profile(
            "Fig2",
            "PRA2,MIB_pravastatin",
            DAYS_1_7_10_17,
            False,
            None,
            "trial 2, day 17, mibefradil",
            "tab:red",
        ),
        "Fig3_PRA3": Profile(
            "Fig3",
            "PRA3_pravastatin",
            (1,),
            False,
            Coadministration.NONE,
            "trial 3, day 1",
            "black",
        ),
        "Fig3_PRA3_ITR": Profile(
            "Fig3",
            "ITR,PRA3_pravastatin",
            tuple(range(1, 31)),
            False,
            Coadministration.ITRACONAZOLE,
            "trial 3, day 30, itraconazole",
            "tab:red",
        ),
        "Fig4_PRA4": Profile(
            "Fig4",
            "CLA_PRA_PRA2",
            tuple(range(1, 8)),
            True,
            Coadministration.NONE,
            "trial 4, day 7",
            "black",
        ),
        "Fig4_PRA4_CLA": Profile(
            "Fig4",
            "CLA_PRA_PRA2,CLA",
            DAYS_1_7_10_17,
            True,
            Coadministration.CLARITHROMYCIN,
            "trial 4, day 17, clarithromycin",
            "tab:red",
            F_OATP1B1_CLARITHROMYCIN,
        ),
    }

    #: the keys of the mappings of the profiles; the mibefradil arm is not
    #: mapped
    mapping_keys: ClassVar[dict[str, str]] = {
        "Fig1_PRA1": "fm_pra40po_pra_PRA1",
        "Fig1_PRA1_VER": "fm_pra40po_pra_PRA1_VER",
        "Fig2_PRA2": "fm_pra40po_pra_PRA2",
        "Fig3_PRA3": "fm_pra40po_pra_PRA3",
        "Fig3_PRA3_ITR": "fm_pra40po_pra_PRA3_ITR",
        "Fig4_PRA4": "fm_pra40po_pra_PRA4",
        "Fig4_PRA4_CLA": "fm_pra40po_pra_PRA4_CLA",
    }

    #: the trials of the figures by the figure of the data
    trials: ClassVar[dict[str, str]] = {
        "Fig1": "Trial 1: verapamil",
        "Fig2": "Trial 2: mibefradil",
        "Fig3": "Trial 3: itraconazole, radioenzymatic",
        "Fig4": "Trial 4: clarithromycin (fed)",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        dfs = {fig_id: self.load_dataframe(fig_id) for fig_id in self.trials}
        for key, profile in self.profiles.items():
            df = dfs[profile.fig_id]
            dset = DataSet.from_df(df[df.label == profile.data_label], self.ureg)
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[key] = dset

        return dsets

    @staticmethod
    def task_key(key: str) -> str:
        """Key of the simulation of a profile."""
        return f"pra_40_{key.split('_', 1)[1]}"

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        dose = Q(40, "mg") * self.Mr.pra / self.Mr.pra_na
        time_delta = 24 * 60  # [min]
        for key, profile in self.profiles.items():
            # the profile is 25 hr after the dose of its day at time 0
            day_last = profile.dose_days[-1]
            end = (day_last - 1) * time_delta + 25 * 60
            times = [(day - 1) * time_delta for day in profile.dose_days[1:]]
            changes = [self.add_doses(times, {"PODOSE_pra": dose})] if times else []
            simulations[self.task_key(key)] = Simulation(
                start=0,
                end=end,
                # every 5 min, the change times are on the grid
                preinit_changes={
                    **self.default_changes(),
                    "GU__fed": Q(1 if profile.fed else 0, "dimensionless"),
                    "LI__f_OATP1B1": Q(profile.f_oatp1b1, "dimensionless"),
                    "PODOSE_pra": dose,
                },
                changes=changes,
                time_shift=-(day_last - 1) * time_delta,
            )

        return simulations

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, mapping_key in self.mapping_keys.items():
            profile = self.profiles[key]
            if profile.coadministration is None:
                continue
            mappings[mapping_key] = FitMapping(
                self,
                reference=FitData(
                    self, dataset=key, xid="time", yid="mean", count="count"
                ),
                observable=FitData(
                    self,
                    task=f"task_{self.task_key(key)}",
                    xid="time",
                    yid="[Cve_pra]",
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.SERUM,
                    route=Route.PO,
                    dosing=Dosing.SINGLE
                    if len(profile.dose_days) == 1
                    else Dosing.MULTIPLE,
                    fasting=Fasting.FED if profile.fed else Fasting.NR,
                    health=Health.HEALTHY,
                    coadministration=profile.coadministration,
                    genotype=Genotype.NR,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        sid = "Fig1_2_3_4"
        fig = Figure(experiment=self, sid=sid, num_rows=2, num_cols=2)
        plots = fig.create_plots(
            xaxis=Axis(self.label_time, unit="hr", min=0, max=25), legend=True
        )
        for kp, (fig_id, title) in enumerate(self.trials.items()):
            plots[kp].set_title(title)
            plots[kp].set_yaxis(self.label_pra, unit="µM", max=0.25)
            for key, profile in self.profiles.items():
                if profile.fig_id != fig_id:
                    continue
                plots[kp].add_data(
                    task=f"task_{self.task_key(key)}",
                    xid="time",
                    yid="[Cve_pra]",
                    label=f"Sim: {profile.label}",
                    linestyle="-",
                    color=profile.color,
                )
                plots[kp].add_data(
                    dataset=key,
                    xid="time",
                    yid="mean",
                    count="count",
                    label=f"Jacobson2004: {profile.label}",
                    color=profile.color,
                )

        return {sid: fig}
