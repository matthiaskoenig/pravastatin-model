"""Sensitivity analysis of the pravastatin model.

The outputs are the pharmacokinetic parameters of pravastatin in venous plasma
after a single oral dose of 40 mg pravastatin sodium (the non-compartmental
analysis of `pkpdutils`) and the fraction of the dose excreted unchanged in the
urine. The parameters are the parameters of the model with bounds of +-15 %
around their value. The analyses are run as a script, the local analysis by
default:

    python -m pkdb_models.models.pravastatin.sensitivity.sensitivity_analysis
    python -m pkdb_models.models.pravastatin.sensitivity.sensitivity_analysis local sampling

The analyses run on `pkpdsim.sensitivity.SensitivityRunner`, which writes the
table of the parameters into `results/sensitivity` of the model and the tables
and figures of an analysis into `results/sensitivity/<analysis>`.
An analysis does not vary a parameter which one of its groups sets
(`pkpdsim.sensitivity.free_parameters`): `sampling`, over the groups, leaves out
`KI__f_renal_function` and `f_cirrhosis`. The environment variable
`PKPDSIM_SENSITIVITY_N` replaces the numbers of samples of the global analyses
for a quick run, see `pkpdsim.sensitivity.sample_size`.

The model without pravastatin is stationary, so the simulation of a group
starts with the dose. The dose is followed for `END_HR` hours, long enough for
the slow distribution into the deep tissue (`kdeep_pra`).
"""

from collections.abc import Mapping

import numpy as np
from pkpdsim.sensitivity import (
    FastAnalysis,
    LocalAnalysis,
    ParameterType,
    SamplingAnalysis,
    SensitivityGroup,
    SensitivityOutput,
    SensitivityParameter,
    SensitivityRunner,
    SobolAnalysis,
    parameters_from_sbml,
    set_bounds,
    set_relative_bounds,
)
from pkpdutils import NCAOptions
from sbmlsim import Q
from sbmlsim.simulation import PK, Formula, Simulation

from pkdb_models.models.pravastatin import MODEL, MODEL_PATH
from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
)
from pkdb_models.models.pravastatin.fitting.parameters import (
    parameters_pk as fit_parameters,
)

#: oral dose of pravastatin sodium of the analysis [mg], given as the dose of
#: pravastatin of the model (`PODOSE_pra`)
DOSE_PRA_NA = 40
#: the hours after the dose
END_HR = 48
#: the limit of quantification of the non-compartmental analysis [mM], about
#: 1e-4 of the maximal plasma concentration after 40 mg (1e-4 mM), so that the
#: noise of the integrator is not the terminal phase
LLOQ = 1e-8
#: fraction of the bounds of a parameter relative to its value
BOUNDS_FRACTION = 0.15

#: outputs of the non-compartmental analysis of pravastatin -> unit of the output
PK_OUTPUTS: dict[str, str] = {
    "auc_inf_obs": "mM*min",
    "cmax": "mM",
    "tmax": "min",
    "thalf": "min",
    "vz_f": "l",
    "cl_f": "ml/min",
}
#: the outputs whose unit has the amount of the dose: the dose is a mass
#: (`PODOSE_pra` in mg), so they are divided by the molecular weight (its value
#: at the start, a value per simulation like the parameter of the analysis)
PK_PER_DOSE_MASS: frozenset[str] = frozenset({"vz_f", "cl_f"})

#: the outputs with their ids and names
OUTPUTS: list[SensitivityOutput] = [
    SensitivityOutput("pra_auc_inf_obs", "pravastatin AUC∞"),
    SensitivityOutput("pra_cmax", "pravastatin Cmax"),
    SensitivityOutput("pra_tmax", "pravastatin tmax"),
    SensitivityOutput("pra_thalf", "pravastatin Half-life"),
    SensitivityOutput("pra_vz_f", "pravastatin Vz/F"),
    SensitivityOutput("pra_cl_f", "pravastatin CL/F"),
    SensitivityOutput("pra_fe_urine", "pravastatin fraction urine"),
]


def _pk_observables(sid: str, outputs: Mapping[str, str]) -> list:
    """Get the non-compartmental analysis of a substance in plasma and its outputs.

    Besides the analysis, the fraction of the dose excreted unchanged in the
    urine until the end (`<sid>_fe_urine`, the cumulative amount at its
    maximum over the amount of the dose).
    """
    pk_id = f"pk_{sid}"
    return [
        PK(
            pk_id,
            f"[Cve_{sid}]",
            dose=f"PODOSE_{sid}",
            route="oral",
            options=NCAOptions(lloq=LLOQ),
            parameters=list(outputs),
        ),
        *(
            Formula(
                f"{sid}_{key}",
                f"{pk_id}.{key} / at(Mr_{sid}, 0)"
                if key in PK_PER_DOSE_MASS
                else f"{pk_id}.{key}",
                unit=unit,
            )
            for key, unit in outputs.items()
        ),
        Formula(
            f"{sid}_fe_urine",
            f"max(Aurine_{sid}) / (at(PODOSE_{sid}, 0) / at(Mr_{sid}, 0))",
            unit="dimensionless",
        ),
    ]


#: the observables of a simulation, the outputs with their units; the id of
#: the analysis (`pk_pra`) is no species of the model
OBSERVABLES = _pk_observables("pra", PK_OUTPUTS)

#: the output times [hr]: every 0.01 hr in the first 12 hr after the dose
#: (absorption and maximum, tmax about 1 hr), every 0.25 hr after it
TIMES_HR: tuple[float, ...] = tuple(
    np.unique(
        np.concatenate(
            [
                np.linspace(0, 12, 1201),
                np.linspace(12, END_HR, 4 * (END_HR - 12) + 1),
            ]
        )
    ).tolist()
)


def sensitivity_simulation(changes: Mapping[str, float]) -> Simulation:
    """Get the simulation of a group: a single oral dose of pravastatin at time 0."""
    mr = PravastatinSimulationExperiment.Mr
    return Simulation(
        start=0,
        end=END_HR,
        times=TIMES_HR,
        time_unit="hr",
        preinit_changes={
            **changes,
            "PODOSE_pra": Q(DOSE_PRA_NA, "mg") * mr.pra / mr.pra_na,
        },
    )


#: the groups the analyses are run for: the control, the stages of renal
#: impairment and of cirrhosis of the simulation experiments
SENSITIVITY_GROUPS: list[SensitivityGroup] = [
    SensitivityGroup("control", "Control", sensitivity_simulation({}), "dimgrey"),
    *(
        SensitivityGroup(
            uid,
            name,
            sensitivity_simulation(
                {
                    "KI__f_renal_function": PravastatinSimulationExperiment.renal_map[
                        name
                    ]
                }
            ),
            PravastatinSimulationExperiment.renal_colors[name],
        )
        for uid, name in [
            ("mildRI", "Mild renal impairment"),
            ("modRI", "Moderate renal impairment"),
            ("sevRI", "Severe renal impairment"),
        ]
    ),
    *(
        SensitivityGroup(
            uid,
            name,
            sensitivity_simulation(
                {"f_cirrhosis": PravastatinSimulationExperiment.cirrhosis_map[name]}
            ),
            PravastatinSimulationExperiment.cirrhosis_colors[name],
        )
        for uid, name in [
            ("mildCirrhosis", "Mild cirrhosis"),
            ("moderateCirrhosis", "Moderate cirrhosis"),
            ("severeCirrhosis", "Severe cirrhosis"),
        ]
    ),
]


def sensitivity_parameters() -> list[SensitivityParameter]:
    """Get the parameters of the analyses with their bounds and references."""
    parameters = parameters_from_sbml(
        MODEL_PATH,
        exclude_ids={
            # molecular weights
            "Mr_pra",
            # reference values
            "BW_ref",
            # unchangeable values
            "FQlu",
            "FVhv",
            "FVpo",
            # dosing parameters
            "PODOSE_pra",
            "IVDOSE_pra",
            "ti_pra",
            "GU__Ka_application_pra",
            # switches of food and of the activities of transporters, which
            # the experiments set
            "GU__fed",
            "KI__f_OAT3",
            "LI__f_OATP1B1",
            "LI__f_MRP2",
            "GU__f_OATP2B1",
            # the fast equilibrium of the biliary excretion
            "LI__PRAEX_k",
        },
        exclude_na=True,
        exclude_zero=True,
    )

    # the fitted parameters, their bounds are set relative to the value below
    set_bounds(
        parameters,
        [(fp.pid, np.nan, np.nan, ParameterType.FIT) for fp in fit_parameters],
    )
    # the scaling factors of the organ functions
    set_bounds(
        parameters,
        [
            (uid, 1 - BOUNDS_FRACTION, 1 + BOUNDS_FRACTION, ParameterType.SCALING)
            for uid in ["KI__f_renal_function"]
        ],
    )

    # the references of the values from the literature
    references = {
        "BW": r"\cite{Ogden2004, Jones2013, Thompson2009, Brown1997}",
        "FQgu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FQh": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FQki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVar": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVgi": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVki": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVli": r"\cite{Jones2013, Wynne1989, Thompson2009, Brown1997}",
        "FVlu": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "FVve": r"\cite{Jones2013, Thompson2009, Brown1997}",
        "COBW": r"\cite{Cattermole2017, Patel2021, Collis2001}",
        "KI__f_renal_function": r"\cite{Stevens2024}",
    }
    by_uid = {p.uid: p for p in parameters}
    for uid, reference in references.items():
        p = by_uid[uid]
        p.reference = reference
        if p.type == ParameterType.NA:
            p.type = ParameterType.DATA

    # every parameter without bounds varies around its value
    set_relative_bounds(parameters, BOUNDS_FRACTION)
    return parameters


#: the analyses of the script, with their groups and numbers of samples
SENSITIVITY = SensitivityRunner(
    model=MODEL,
    parameters=sensitivity_parameters,
    outputs=OUTPUTS,
    observables=OBSERVABLES,
    analyses={
        "local": LocalAnalysis(groups=SENSITIVITY_GROUPS[:1], delta=0.01),
        "sampling": SamplingAnalysis(groups=SENSITIVITY_GROUPS, n=1000),
        "fast": FastAnalysis(groups=SENSITIVITY_GROUPS[:1], n=1000),
        "sobol": SobolAnalysis(groups=SENSITIVITY_GROUPS[:1], n=4096),
    },
    default=("local",),
)


if __name__ == "__main__":
    SENSITIVITY.main()
