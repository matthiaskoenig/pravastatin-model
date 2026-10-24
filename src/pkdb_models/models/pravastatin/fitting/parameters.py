"""The fit parameters of the pravastatin model.

The pharmacokinetics are fitted on the plasma concentrations and the urinary
excretion of pravastatin after intravenous (Singhvi1990) and oral doses. The
intravenous data and the urine separate the hepatic uptake (`LI__PRAIM_Vmax`),
the renal clearance (`KI__PRAEX_f`) and the fraction absorbed
(`GU__F_pra_abs`); the dissolution and the absorption rate shape the oral
curves, the tissue distribution (`Kp_pra`) the intravenous curve. The bounds
contain the
literature values (total clearance 1.0 l/min, renal clearance 0.43-0.46 l/min,
Vss 0.46 l/kg, fraction absorbed 0.34, bioavailability 0.17-0.18; Singhvi1990,
Halstenson1992). Fixed, not fitted: the Km of the hepatic uptake (10 µM, far
above the plasma concentrations), the biliary excretion `LI__PRAEX_k` (only the
timing of the enterohepatic circulation), the exchange flow of the tissue
`ftissue_pra` (fast, 20 l/min), the slow distribution into the deep tissue
(`Kpdeep_pra`, `kdeep_pra`: the beta phase of Singhvi1990, which the cost of
the fits does not identify), the unbound fraction (0.5), the
healthy GFR (101 ml/min), the activities of the SLCO1B1 alleles, the factors
of the interactions and the effects of food (`GU__FED_f_absorption`,
`GU__FED_f_dissolution`, set to the label: food lowers the AUC by about 30 %),
which no fasted training data identify.
"""

from sbmlsim.fit import FitParameter

#: the pharmacokinetics of pravastatin
parameters_pk: list[FitParameter] = [
    # hepatic uptake by OATP1B1: hepatic extraction about 0.5
    FitParameter(
        pid="LI__PRAIM_Vmax",
        start_value=0.0085,
        lower_bound=5e-4,
        upper_bound=0.1,
        unit="mmole/min/l",
    ),
    # renal clearance relative to the filtration of the unbound pravastatin:
    # 0.43-0.46 l/min, 47 % of an intravenous dose in the urine
    FitParameter(
        pid="KI__PRAEX_f",
        start_value=13.5,
        lower_bound=1,
        upper_bound=60,
        unit="dimensionless",
    ),
    # fraction absorbed, 0.34 (Singhvi1990)
    FitParameter(
        pid="GU__F_pra_abs",
        start_value=0.33,
        lower_bound=0.05,
        upper_bound=0.9,
        unit="dimensionless",
    ),
    # absorption from the lumen and dissolution: tmax about 1 hr
    FitParameter(
        pid="GU__PRAABS_k",
        start_value=0.015,
        lower_bound=1e-3,
        upper_bound=0.5,
        unit="1/min",
    ),
    FitParameter(
        pid="GU__Ka_dis_pra",
        start_value=2.1,
        lower_bound=0.1,
        upper_bound=20,
        unit="1/hr",
    ),
    # tissue distribution: Vss 0.46 l/kg (Singhvi1990); the exchange with the
    # tissue is fast (`ftissue_pra` fixed)
    FitParameter(
        pid="Kp_pra",
        start_value=0.3,
        lower_bound=0.05,
        upper_bound=3,
        unit="dimensionless",
    ),
]
