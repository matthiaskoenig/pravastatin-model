"""Cholesterol part of the liver model.

The hepatic cholesterol balance: the synthesis of cholesterol from acetyl-CoA
via HMG-CoA (HMG-CoA synthase and HMG-CoA reductase, inhibited by pravastatin),
the uptake of LDL cholesterol by the LDL receptor, the export as VLDL
cholesterol and the turnover of the proteins, regulated by the hepatic
cholesterol.
"""

import numpy as np
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    AssignmentRule,
    FactoryResult,
    Model,
    Parameter,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.pravastatin.models import annotations, templates
from pkdb_models.models.pravastatin.models.model_liver_pravastatin import U as Ubase


class U(Ubase):
    """UnitsDefinition."""

    per_mmole = UnitDefinition("per_mmole", "1/mmole")
    per_litre = UnitDefinition("per_l", "1/l")
    l_per_mmole = UnitDefinition("l_per_mmole", "l/mmole")
    g_per_mole = UnitDefinition("g_per_mole", "g/mole")
    mg_per_day = UnitDefinition("mg_per_day", "mg/day")
    min_per_day = UnitDefinition("min_per_day", "min/day")


_m = Model(
    "pravastatin_liver_cholesterol",
    name="Model for cholesterol metabolism in the liver",
    notes="""
    # Model for cholesterol metabolism in the liver
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.species = [
    Species(
        sid="ldlc_ext",
        initialConcentration=3.0,
        name="ldl-cholesterol (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        port=True,
        boundaryCondition=True,  # constant external LDL-C (False: free LDL-C)
        sboTerm=SBO.MACROMOLECULAR_COMPLEX,
        annotations=annotations.species["ldlc"],
        notes="""
        reference values from studies (normal ranges ~3 mM)
        """,
    ),
    Species(
        sid="vldlc_ext",
        initialConcentration=1.0,
        name="vldl-cholesterol (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        port=True,
        boundaryCondition=False,
        sboTerm=SBO.MACROMOLECULAR_COMPLEX,
        annotations=annotations.species["vldlc"],
    ),
    # liver (cholesterol)
    Species(
        sid="acoa",
        initialConcentration=0.043,
        name="acetyl-CoA (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        boundaryCondition=True,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["acoa"],
        notes="""
        0.043 ± 0.031 mM Corkey1988; 0.028 - 0.081 [mM] Lumbers1969
        """,
    ),
    Species(
        sid="hmgcoa",
        initialConcentration=0.022,
        name="HMG-CoA (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["hmgcoa"],
        notes="""
        0.022 ± 0.027 [mM] Corkey1988
        """,
    ),
    Species(
        sid="cho",
        initialConcentration=0.020,
        name="cholesterol (liver)",
        compartment="Vli",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        port=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["cholesterol"],
        boundaryCondition=False,
        notes="""
        5.8 - 160 [µmol/l] [Chuang2017]; mice
        ~ 8.17 [µmol/l] [Rudling1997]; rat
        reference point 0.020 with variation [0.01 - 0.100]
        """,
    ),
    # --- HMGCOA (effective units dimensionless) ---
    Species(
        sid="hmgcoareductase",
        initialConcentration=1,
        name="HMG-CoA reductase (liver)",
        compartment="Vli",
        substanceUnit=U.dimensionless,
        hasOnlySubstanceUnits=True,
        conversionFactor="cf_units_per_mmole",
        sboTerm=SBO.MACROMOLECULE,
        annotations=annotations.species["hmgcoareductase"],
    ),
    Species(
        sid="hmgcoasynthase",
        initialConcentration=1,
        name="HMG-CoA synthase (liver)",
        compartment="Vli",
        substanceUnit=U.dimensionless,
        hasOnlySubstanceUnits=True,
        conversionFactor="cf_units_per_mmole",
        sboTerm=SBO.MACROMOLECULE,
        annotations=annotations.species["hmgcoasynthase"],
    ),
    # --- LDL receptor (LDLR) ---
    # protein amounts (are modeled relative to reference point of 1 [mM])
    # here only the relative changes are important for the kinetics
    # initially the pool is 1 with equal distribution in three species
    Species(
        sid="ldlr",
        initialConcentration=1 * 1.0 / 10,
        name="LDLR",
        compartment="Vli",
        substanceUnit=U.dimensionless,
        hasOnlySubstanceUnits=True,
        conversionFactor="cf_units_per_mmole",
        sboTerm=SBO.MACROMOLECULE,
        annotations=annotations.species["ldlr"],
    ),
    Species(
        sid="ldlr_membrane",
        initialConcentration=8 * 1.0 / 10,
        name="LDLR membrane",
        compartment="Vbaso",
        substanceUnit=U.dimensionless,
        hasOnlySubstanceUnits=True,
        conversionFactor="cf_units_per_mmole",
        sboTerm=SBO.MACROMOLECULE,
        annotations=annotations.species["ldlr_membrane"],
    ),
    Species(
        sid="ldlr_ldlc",
        initialConcentration=1 * 1.0 / 10,
        name="LDLR-LDLC complex",
        compartment="Vli",
        substanceUnit=U.dimensionless,
        hasOnlySubstanceUnits=True,
        conversionFactor="cf_units_per_mmole",
        sboTerm=SBO.MACROMOLECULAR_COMPLEX,
        annotations=annotations.species["ldlr_ldlc"],
    ),
    Species(
        sid="ldlr_degraded",
        initialConcentration=0,
        name="LDLR degraded",
        compartment="Vli",
        substanceUnit=U.dimensionless,
        hasOnlySubstanceUnits=True,
        conversionFactor="cf_units_per_mmole",
        sboTerm=SBO.MACROMOLECULE,
        annotations=annotations.species["ldlr_degraded"],
        notes="""
        Species added for tracking degradation of LDLR.
        """,
    ),
]
_m.rules = [
    AssignmentRule(
        "ldlr_total",
        "ldlr + ldlr_membrane + ldlr_ldlc",
        unit=U.dimensionless,
        name="Total LDLR",
        sboTerm=SBO.MASS_CONSERVATION_LAW,
    ),
    AssignmentRule(
        "ldlr_fraction",
        "ldlr/ldlr_total",
        unit=U.dimensionless,
        name="LDLR fraction",
    ),
    AssignmentRule(
        "ldlr_membrane_fraction",
        "ldlr_membrane/ldlr_total",
        unit=U.dimensionless,
        name="LDLR membrane fraction",
    ),
    AssignmentRule(
        "ldlr_ldlc_fraction",
        "ldlr_ldlc/ldlr_total",
        unit=U.dimensionless,
        name="LDLR-LDLC fraction",
    ),
]

_m.parameters = [
    Parameter(
        sid="cf_units_per_mmole",
        value=1.0,
        unit=U.per_mmole,
        name="conversion factor for dimensionless species",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    # global parameters
    Parameter(
        "conversion_min_per_day",
        1440,
        U.min_per_day,
        constant=True,
        name="conversion factor min to hours",
        port=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
    ),
    # pravastatin inhibitor activity of other possible pravastatin metabolites
    # “75% of the inhibitory activity of pravastatin is attributable to the parent drug” {Pan et al. 1990b}.
    Parameter(
        "pra_inhibitor_activity",
        1,  # TODO: FIXME
        U.dimensionless,
        constant=True,
        name="Inhibitor activity of pravastatin",
        port=True,
        sboTerm=SBO.INHIBITORY_CONSTANT,
    ),
    Parameter(
        "Mr_ldlc",
        386.654,
        U.g_per_mole,
        constant=True,
        name="Molecular weight cho [g/mole]",
        port=True,
        sboTerm=SBO.MOLECULAR_MASS,
    ),
    # 1 [g/day]
    Parameter(
        "v_cho_ref",
        1000,
        unit=U.mg_per_day,
        name="reference cholesterol turnover [mg/day]",
        port=True,
        sboTerm=SBO.BASAL_RATE_CONSTANT,
    ),
]
_m.rules.extend(
    [
        AssignmentRule(
            "v_cho_reference",
            "v_cho_ref / Mr_ldlc / conversion_min_per_day",
            unit=U.mmole_per_min,
            name="reference cholesterol turnover [mmole/min]",
        ),
    ]
)


_m.reactions = [
    # ---------------------------------------------------------------------------------
    # Cholesterol balance/turnover
    # ---------------------------------------------------------------------------------
    # All reactions scaled with global scaling factor
    # ---------------------------------------------------------------------------------
    # cholesterol export as VLDL (LDL)
    Reaction(
        sid="VLDLCEXP",
        name="VLDL-cholesterol export",
        compartment="Vbaso",
        equation="cho -> vldlc_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            # 1.4 [g/day]
            Parameter(
                "VLDLCEXP_Vmax",
                0.05 * 50,
                unit=U.dimensionless,
                sboTerm=SBO.MAXIMAL_VELOCITY,
                name="Vmax VLDL-cholesterol export",
            ),
            Parameter(
                "VLDLCEXP_Km_cho",
                0.0005,
                unit=U.mM,
                sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
                name="Km VLDL-cholesterol export",
            ),
        ],
        formula=(
            "VLDLCEXP_Vmax * v_cho_reference * cho / (cho + VLDLCEXP_Km_cho)",
            U.mmole_per_min,
        ),
    ),
    # irreversible import of LDLC
    # Pooled process of binding(formation of LDLR-LDLC complex) depending on affinity
    # Km, and subsequeqnt internalization.
    Reaction(
        sid="LDLRLDLCIMP",
        name="LDLR-LDLC binding & internalization",
        compartment="Vbaso",
        equation="ldlc_ext + ldlr_membrane -> ldlr_ldlc [ldlr_ldlc]",
        sboTerm=SBO.TRANSPORT_REACTION,
        pars=[
            Parameter(
                "LDLRLDLCIMP_Kcat",
                0.05 * 60 * 2,
                unit=U.dimensionless,
                sboTerm=SBO.CATALYTIC_RATE_CONSTANT,
            ),
            Parameter(
                "LDLRLDLCIMP_Km",
                3.0,
                unit=U.mM,
                sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
                name="Km LDLR-LDLC binding",
                notes="""
                Set to 3mM for reference state of 3mM in healthy patient as 3mM plasma
                LDL-C.
                """,
            ),
            Parameter(
                "LDLRLDLCIMP_Ki_ldlr_ldlc",
                0.1,
                unit=U.dimensionless,
                sboTerm=SBO.INHIBITORY_CONSTANT,
                name="Ki LDLR-LDLC complex on uptake",
                notes="""Feedback of complex to uptake. Mechanism?""",
            ),
            Parameter(
                "LDLRLDLCIMP_Km_f",
                1,
                unit=U.dimensionless,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
            Parameter(
                "LDLRLDLCIMP_Kcat_f",
                1,
                unit=U.dimensionless,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            ),
        ],
        formula=(
            # linear dependency on Protein amount Vmax = kcat * P
            "v_cho_reference * LDLRLDLCIMP_Kcat * LDLRLDLCIMP_Kcat_f * ldlr_membrane * "
            "ldlc_ext/(LDLRLDLCIMP_Km * LDLRLDLCIMP_Km_f + ldlc_ext) * "
            "1 dimensionless/(1 dimensionless + ldlr_ldlc/LDLRLDLCIMP_Ki_ldlr_ldlc)",
            U.mmole_per_min,
        ),
    ),
]

# ---------------------------------------------------------------------------------
# LDL-Receptor turnover
# ---------------------------------------------------------------------------------
#
# - "recycling of LDL receptors to the cell surface occurs approximately 150 times"
# - "The LDL receptor makes one round trip into and out of the cell every 10 min
#     for a total of several hundred trips in its 20-hr lifespan
#     (4, 28)"{BrownGoldsteinLecture}
# - what fraction of LDLR is at the membrane?
# - what is the half-life of LDLR? (20 hr lifespan)
#
# Reaction pooling all processes involved in membrane transport of the finished
# LDL-R protein. E.g. transport from the endoplasmatic reticulum to the Golgi
# apparatus and subsequent transport to the plasma membrane
#
# LDLR
# -> membrane:
#   LDLRMEMBRANE_Kcat * ldlr => LDLRMEMBRANE_Kcat/3
# -> recycling
#   LDLRRECYCLING_Kcat * ldlr_ldlc => LDLRRECYCLING_Kcat/3
# -> synthesis
#   SYNTHESIS_LDLR_Vmax / (1 dimensionless + cho / LDLR_kr_cho) => SYNTHESIS_LDLR_Vmax/2
# -> degradation:
#   DEGRADATION_LDLR_Vmax * ldlr * (1 dimensionless + cho / LDLR_kr_cho)
#   = DEGRADATION_LDLR_Vmax * 2/3
#
# d LDLR/dt = -LDLRMEMBRANE_Kcat/3 + LDLRRECYCLING_Kcat/3 + SYNTHESIS_LDLR_Vmax/2 -
#     DEGRADATION_LDLR_Vmax * 2/3
#
# LDLR-LDLC & LDLR membrane
# -> internalization
#   v_cho_reference_li * LDLRLDLCIMP_Kcat * ldlr_membrane *
#     ldlc_ext/(LDLRLDLCIMP_Km + ldlc_ext)
#   => v_cho_reference_li * LDLRLDLCIMP_Kcat/6

_m.reactions.extend(
    [
        Reaction(
            sid="LDLR_TO_MEMBRANE",
            name="LDLR membrane transport",
            compartment="Vbaso",
            equation="ldlr <-> ldlr_membrane",
            sboTerm=SBO.TRANSPORT_REACTION,
            pars=[
                Parameter(
                    "LDLRMEMBRANE_Kcat",
                    0.05 * 0.5,
                    unit=U.mmole_per_min_l,
                    sboTerm=SBO.CATALYTIC_RATE_CONSTANT,
                ),
                Parameter(
                    "LDLRMEMBRANE_Kcat_f",
                    1,
                    unit=U.dimensionless,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                ),
                Parameter(
                    "LDLRMEMBRANE_Keq",
                    10,
                    unit=U.dimensionless,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    notes="""
                    Feedback of LDLR membrane on LDLR pool via equilibration constant.
                    Keq = ldlr_membrane/ldlr_substrate
                    """,
                ),
            ],
            formula=(
                # first order dependency
                "Vli * LDLRMEMBRANE_Kcat * LDLRMEMBRANE_Kcat_f * (ldlr - ldlr_membrane/LDLRMEMBRANE_Keq)",
                U.mmole_per_min,
            ),
        ),
        Reaction(
            sid="LDLRRECYCLING",
            name="LDLR recycling",
            compartment="Vli",
            equation="ldlr_ldlc -> ldlr + cho",
            sboTerm=SBO.TRANSPORT_REACTION,
            pars=[
                Parameter(
                    "LDLRRECYCLING_Kcat",
                    0.05 * 0.25,
                    unit=U.mmole_per_min_l,
                    sboTerm=SBO.CATALYTIC_RATE_CONSTANT,
                ),
                Parameter(
                    "LDLRRECYCLING_Kcat_f",
                    1,
                    unit=U.dimensionless,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                ),
            ],
            formula=(
                # first order dependency
                "Vli * LDLRRECYCLING_Kcat * LDLRRECYCLING_Kcat_f * ldlr_ldlc",
                U.mmole_per_min,
            ),
        ),
        # first order reaction from 3 acoa -> hmgcoa
        # for description: how was cholesterol synthesis pathway simplified and why;
        # discussion about kinetics.
        # - product inhibition mechanism if sufficient HMG-CoA exists in the liver
        # - only first-order dependency on acoa (simplification for pathway reduction)
        Reaction(
            sid="HMGCOASYNTHASE",
            name="HMG-CoA synthase",
            compartment="Vli",
            equation="3 acoa -> hmgcoa [hmgcoasynthase, hmgcoa]",
            sboTerm=SBO.BIOCHEMICAL_REACTION,
            pars=[
                Parameter(
                    "HMGCOASYNTHASE_Kcat",
                    350 * 0.7,
                    unit=U.l_per_mmole,
                    sboTerm=SBO.CATALYTIC_RATE_CONSTANT,
                    notes="""
                    higher then HMG-CoA Reductase:
                    3E-3 [mmole/min/l] /1.4 [l]/ 0.03 [mole/l] = 71.4E-3 [1/min]
                    """,
                ),
                Parameter(
                    "HMGCOASYNTHASE_Ki_hmgcoa",
                    0.022,
                    unit=U.mM,
                    sboTerm=SBO.INHIBITORY_CONSTANT,
                    notes="""
                product inhibition ~ reference concentration
                """,
                ),
            ],
            formula=(
                # first order with product inhibition and dependence on hmgcoasynthase
                "HMGCOASYNTHASE_Kcat * v_cho_reference * hmgcoasynthase * acoa / "
                "(1 dimensionless + hmgcoa / HMGCOASYNTHASE_Ki_hmgcoa)",
                U.mmole_per_min,
            ),
        ),
        Reaction(
            sid="HMGCOAREDUCTASE",
            name="HMG-CoA reductase",
            compartment="Vli",
            equation="6 hmgcoa -> cho [pra, hmgcoareductase]",
            sboTerm=SBO.BIOCHEMICAL_REACTION,
            pars=[
                # +1.0 [g/day]
                Parameter(
                    "HMGCOAREDUCTASE_Kcat",
                    0.7,
                    unit=U.dimensionless,
                    sboTerm=SBO.CATALYTIC_RATE_CONSTANT,
                ),
                # ~ 1 g/day; 1/368.7/1.440 mmole/min = 1.88E-3 mmole/min / 1.4 [l]
                # = 1.34E-3 mmole/min/l
                Parameter(
                    "HMGCOAREDUCTASE_Km",
                    4e-3,
                    unit=U.mM,
                    sboTerm=SBO.MICHAELIS_CONSTANT_FOR_SUBSTRATE,
                    name="Km HMG-CoA",
                    notes="""""",
                ),
                # Hoeg1987
                Parameter(
                    "HMGCOAREDUCTASE_Ki_pra",
                    2.3e-6,  # Hoeg1987
                    unit=U.mM,
                    sboTerm=SBO.INHIBITORY_CONSTANT,
                    name="Ki HMG-CoA for pravastatin",
                ),
            ],
            formula=(
                # michaelis menten kinetic with competitive inhibition of pra and
                # dependence on hmgoareductase
                # linear dependency on Protein amount Vmax = kcat * P
                "HMGCOAREDUCTASE_Kcat * v_cho_reference * hmgcoareductase * hmgcoa / "
                "(HMGCOAREDUCTASE_Km * (1 dimensionless + (pra * pra_inhibitor_activity) / HMGCOAREDUCTASE_Ki_pra) + hmgcoa)",
                U.mmole_per_min,
            ),
        ),
    ]
)

# --------------------------------
# Protein synthesis & degradation
# --------------------------------
# - main proteins relevant for LDL-C metabolism are modeled dynamically
#     LDL-R: LDL-receptor
#     HMG-CoA synthase
#     HMG-CoA reductase
# - for every protein a irreversible synthesis and degration reaction exists with steady
#   state as
#   0 = dS_i/dt + dD_i/dt
# - no transcription
# - synthesis is zero-order dependence of protein
# - degradation is first order dependence on protein: dD_i/dt = f(c[i])
# - LDL-receptor is handled differently then synthase and reductase
# - Cholesterol inhibits synthesis and activates degradation
# - at the reference point the protein amount should be 1.0
# - protein is in relative units


_m.parameters.extend(
    [
        # HMG-CoA synthase and reductase
        Parameter(
            "SYNTHESIS_HMG_Vmax",
            1e-3,
            unit=U.mmole_per_min_l,  # 2/60 [mmole/hr]
            name="Protein synthesis Vmax for HMGR and HMGS",
            sboTerm=SBO.MAXIMAL_VELOCITY,
        ),
        Parameter(
            "DEGRADATION_HMG_Vmax",
            3e-4,
            unit=U.mmole_per_min_l,
            name="Protein degradation Vmax for HMGR and HMGS",
            sboTerm=SBO.MAXIMAL_VELOCITY,
        ),
        Parameter(
            "HMG_kr_cho",
            0.020,
            unit=U.mM,
            name="Protein regulation kr for HMGR and HMGS",
            sboTerm=SBO.INHIBITORY_CONSTANT,
        ),
        # LDL Receptor (LDLR)
        Parameter(
            "DEGRADATION_LDLR_Vmax",
            0.0006,
            unit=U.mmole_per_min_l,
            name="Protein degradation Vmax for LDLR",
            sboTerm=SBO.MAXIMAL_VELOCITY,
        ),
        Parameter(
            "SYNTHESIS_LDLR_Vmax",
            np.nan,
            unit=U.mmole_per_min_l,  # 2/60 [mmole/hr]
            name="Protein synthesis Vmax for LDLR",
            sboTerm=SBO.MAXIMAL_VELOCITY,
            constant=False,
            notes="""
            Synthesis parameter was determined based on steady state condition
            with assumption of 0.1 (10%) of pool as free LDLR.
            ```
            DEGRADATION_LDLR_Vmax * LDLR_ss * 2 = SYNTHESIS_LDLR_Vmax/2
            SYNTHESIS_LDLR_Vmax = 4 * DEGRADATION_LDLR_Vmax * LDLR_ss
            ```
            """,
        ),
        Parameter(
            "LDLR_kr_cho",
            0.020,
            unit=U.mM,
            name="Protein regulation kr for LDLR",
            sboTerm=SBO.INHIBITORY_CONSTANT,
        ),
        Parameter(
            "SYNTHESIS_LDLR_Vmax_f",
            1,
            unit=U.dimensionless,
            name="scaling factor for synthesis Vmax for LDL-R",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "DEGRADATION_LDLR_Vmax_f",
            1,
            unit=U.dimensionless,
            name="scaling factor for degradation Vmax for LDL-R",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
    ]
)
_m.rules.append(
    AssignmentRule(
        "SYNTHESIS_LDLR_Vmax",
        "0.4 dimensionless * DEGRADATION_LDLR_Vmax",
        U.mmole_per_min_l,
    )
)


# DEGRADATION_LDLR_Vmax * LDLR = SYNTHESIS_HMG_Vmax

for cid in ["hmgcoareductase", "hmgcoasynthase", "ldlr"]:
    synthesis_id = f"SYNTHESIS_{cid.upper()}"
    synthesis_name = f"{cid.upper()} synthesis"
    degradation_id = f"DEGRADATION_{cid.upper()}"
    degradation_name = f"{cid.upper()} degradation"

    if cid in ["hmgcoareductase", "hmgcoasynthase"]:
        formula_synthesis = (
            "SYNTHESIS_HMG_Vmax * Vli / (1 dimensionless + cho / HMG_kr_cho)"
        )
        formula_degradation = (
            f"DEGRADATION_HMG_Vmax * {cid} * Vli * (1 dimensionless + cho / HMG_kr_cho)"
        )
        equation_degradation = f"{cid} -> [cho]"
    elif cid in ["ldlr"]:
        formula_synthesis = (
            "Vli * SYNTHESIS_LDLR_Vmax * SYNTHESIS_LDLR_Vmax_f / "
            "(1 dimensionless + cho / LDLR_kr_cho)"
        )
        formula_degradation = (
            f"Vli * DEGRADATION_LDLR_Vmax * DEGRADATION_LDLR_Vmax_f"
            f" * {cid} * (1 dimensionless + cho / LDLR_kr_cho)"
        )
        equation_degradation = f"{cid} -> {cid}_degraded [cho]"

    _m.reactions.extend(
        [
            Reaction(
                sid=synthesis_id,
                name=synthesis_name,
                compartment="Vli",
                equation=f"-> {cid} [cho]",
                sboTerm=SBO.BIOCHEMICAL_REACTION,
                pars=[],
                formula=(formula_synthesis, U.mmole_per_min),
            ),
            Reaction(
                sid=degradation_id,
                name=degradation_name,
                compartment="Vli",
                equation=equation_degradation,
                sboTerm=SBO.BIOCHEMICAL_REACTION,
                pars=[],
                formula=(formula_degradation, U.mmole_per_min),
            ),
        ]
    )
# --------------------------------
_m.rules = [
    *_m.rules,
    # rules to convert the rates into [g/day]
    # [mmole/min] * [g/mole] * 1440 [min/day] -> [mg/day]
    AssignmentRule(
        "v_synthesis",
        "HMGCOAREDUCTASE * Mr_ldlc * conversion_min_per_day",
        U.mg_per_day,
        name="total synthesized cholesterol",
    ),
    AssignmentRule(
        "v_uptake",
        "LDLRLDLCIMP * Mr_ldlc * conversion_min_per_day",
        U.mg_per_day,
        name="cholesterol uptake (LDL receptor)",
    ),
    AssignmentRule(
        "v_export",
        "VLDLCEXP * Mr_ldlc * conversion_min_per_day",
        U.mg_per_day,
        name="cholesterol export (VLDL)",
    ),
    AssignmentRule(
        "v_reference",
        "v_cho_reference * Mr_ldlc * conversion_min_per_day",
        U.mg_per_day,
        name="cholesterol reference flux",
    ),
    AssignmentRule(
        "v_net_export_rate",
        "VLDLCEXP - LDLRLDLCIMP",
        U.mmole_per_min,
        name="cholesterol net export (VLDL)",
    ),
    AssignmentRule(
        "v_net_export",
        "v_net_export_rate * Mr_ldlc * conversion_min_per_day",
        U.mg_per_day,
        name="cholesterol net export (VLDL)",
    ),
    AssignmentRule(
        "v_liver_balance",
        "v_synthesis + v_uptake  - v_export",
        U.mg_per_day,
        name="cholesterol net  export (VLDL)",
    ),
    AssignmentRule(
        "TURNOVER_LDLR",
        "SYNTHESIS_LDLR - DEGRADATION_LDLR",
        U.mmole_per_min,
        name="total turnover of LDL-R expression",
    ),
]

model_liver_cholesterol = _m

if __name__ == "__main__":
    from pkdb_models.models.pravastatin import MODEL_BASE_PATH
    from pkdb_models.models.pravastatin.models.model_liver_base import model_liver_base

    result: FactoryResult = create_model(
        filepath=MODEL_BASE_PATH / f"{model_liver_cholesterol.sid}.xml",
        model=[
            model_liver_base,
            model_liver_cholesterol,
        ],
        sbml_level=3,
        sbml_version=2,
    )
