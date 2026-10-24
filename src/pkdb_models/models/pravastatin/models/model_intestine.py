"""Intestine model of pravastatin.

The oral dose is applied into the stomach, dissolved and emptied into the
intestinal lumen (`dissolution_pra`, `Ka_dis_pra`). Pravastatin leaves the
lumen with the first order rate `PRAABS_k`: a fraction `F_pra_abs * f_OATP2B1`
is absorbed via OATP2B1 (SLCO2B1) into the plasma, the rest is excreted in the
feces. The biliary pravastatin of the liver enters the same lumen and is
partly reabsorbed (enterohepatic circulation). Food (`fed`) reduces the
fraction absorbed (`FED_f_absorption`) and slows the dissolution and gastric
emptying (`FED_f_dissolution`): food lowers the bioavailability of pravastatin
by about a third (Pravachol label; Pan2000).

- "The oral absorption of [14C] activity from pravastatin sodium was about 34%
  and the oral bioavailability was about 18%" {Singhvi1990}
- The isomerization of pravastatin to SQ31906 in the acidic stomach is part of
  the loss of the fraction absorbed; the isomer is not modeled.
"""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    Model,
    Parameter,
    RateRule,
    Reaction,
    Species,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.pravastatin.models import annotations, templates
from pkdb_models.models.pravastatin.models.fits import FITS


class U(templates.U):
    """UnitDefinitions."""

    per_hr = UnitDefinition("per_hr", "1/hr")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")
    min_per_hr = UnitDefinition("min_per_hr", "min/hr")


_m = Model(
    "pravastatin_intestine",
    name="Model for pravastatin elimination in the small intestine",
    notes="""
    # Model for pravastatin transport from the small intestine into the liver

    Model for enterohepatic uptake of pravastatin via OATP2B1 (SLCO2B1)

    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

_m.compartments = [
    Compartment(
        "Vext",
        1.0,
        name="plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["plasma"],
    ),
    Compartment(
        "Vgu",
        1.2825,  # 0.0171 [l/kg] * 75 kg
        name="intestine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vlumen",
        1.2825 * 0.9,  # 0.0171 [l/kg] * 75 kg * 0.9,
        name="intestinal lumen (inner part of intestine)",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        constant=False,
        port=True,
        annotations=annotations.compartments["gu_lumen"],
    ),
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["feces"],
    ),
    Compartment(
        "Vstomach",
        metaId="meta_Vstomach",
        value=1,
        unit=U.liter,
        constant=True,
        name="stomach",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        port=True,
        annotations=annotations.compartments["stomach"],
    ),
]


_m.species = [
    Species(
        "pra_stomach",
        metaId="meta_pra_stomach",
        initialConcentration=0.0,
        compartment="Vstomach",
        substanceUnit=U.mmole,
        name="pravastatin (stomach)",
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["pra"],
        boundaryCondition=True,
        notes="""Species in amounts, no dependency on stomach volume.""",
    ),
    Species(
        "pra_lumen",
        initialConcentration=0.0,
        name="pravastatin (intestinal volume)",
        compartment="Vlumen",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["pra"],
        port=True,
    ),
    Species(
        "pra_ext",
        initialConcentration=0.0,
        name="pravastatin (plasma)",
        compartment="Vext",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=False,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["pra"],
        port=True,
    ),
    Species(
        "pra_feces",
        initialConcentration=0.0,
        name="pravastatin (feces)",
        compartment="Vfeces",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["pra"],
        port=True,
    ),
]

_m.parameters = [
    Parameter(
        "F_pra_abs",
        **FITS.parameter("GU__F_pra_abs", unit=U.dimensionless),
        constant=True,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        name="fraction absorbed pravastatin (fasted)",
        notes="""
        Fraction of the pravastatin leaving the intestinal lumen which is
        absorbed via OATP2B1, `F_pra_abs * f_OATP2B1 * f_absorption`; the rest
        is excreted with the feces. It applies to the dose and to every pass of
        the enterohepatic circulation. The oral absorption of 14C-pravastatin
        is about 34 % (Singhvi1990).
        """,
    ),
    Parameter(
        "PRAABS_k",
        **FITS.parameter("GU__PRAABS_k", unit=U.per_min),
        name="rate of pravastatin leaving the intestinal lumen",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        First order rate of the absorption from the lumen; together with the
        dissolution and gastric emptying it gives the tmax of 0.75-1.5 hr of
        the tablets.
        """,
    ),
    Parameter(
        "f_OATP2B1",
        1.0,
        unit=U.dimensionless,
        name="parameter for OATP2B1 activity",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        parameter controls genetic variants and the inhibition of the
        intestinal uptake (1.0 reference function, < 1.0 reduced function,
        > 1.0 increased function); it scales the fraction absorbed.
        """,
    ),
    Parameter(
        "fed",
        0.0,
        unit=U.dimensionless,
        name="fed state (0 fasted, 1 fed)",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        The dose is taken in the fasted state (0) or with a meal (1). The
        effects of food on the fraction absorbed and on the dissolution and
        gastric emptying are `FED_f_absorption` and `FED_f_dissolution`.
        """,
    ),
    Parameter(
        "FED_f_absorption",
        0.75,
        unit=U.dimensionless,
        name="fed effect on the fraction absorbed",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        Food reduces the AUC of pravastatin by about 30 % (Pravachol label;
        Pan2000, dosed after breakfast).
        """,
    ),
    Parameter(
        "FED_f_dissolution",
        0.4,
        unit=U.dimensionless,
        name="fed effect on the dissolution and gastric emptying",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        Food delays the tmax of pravastatin from about 1 hr to 1.5-2 hr
        (Gustavson2005, Pan2000).
        """,
    ),
]

_m.rules.extend(
    [
        AssignmentRule(
            "f_absorption",
            "1 dimensionless + fed * (FED_f_absorption - 1 dimensionless)",
            unit=U.dimensionless,
            name="factor of the fraction absorbed",
        ),
        AssignmentRule(
            "f_dissolution",
            "1 dimensionless + fed * (FED_f_dissolution - 1 dimensionless)",
            unit=U.dimensionless,
            name="factor of the dissolution and gastric emptying",
        ),
        AssignmentRule(
            "F_absorbed",
            "F_pra_abs * f_OATP2B1 * f_absorption",
            unit=U.dimensionless,
            name="fraction absorbed",
        ),
        AssignmentRule(
            "absorption",
            "PRAABS_k * Vlumen * pra_lumen",
            unit=U.mmole_per_min,
            name="pravastatin leaving the lumen",
        ),
    ]
)

_m.reactions = [
    Reaction(
        "PRAABS",
        name="absorption pravastatin (OATP2B1)",
        equation="pra_lumen -> pra_ext",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vgu",
        formula=("F_absorbed * absorption", U.mmole_per_min),
        notes="""
        Import via OATP2B1 is irreversible at apical membrane of enterocytes.
        """,
    ),
    # fraction excreted (not available for absorption)
    Reaction(
        sid="PRAEXC",
        name="excretion pravastatin (feces)",
        compartment="Vlumen",
        equation="pra_lumen -> pra_feces",
        sboTerm=SBO.TRANSPORT_REACTION,
        formula=(
            "(1 dimensionless - F_absorbed) * absorption",
            U.mmole_per_min,
        ),
    ),
]

_m.parameters.extend(
    [
        Parameter(
            "PODOSE_pra",
            0,
            U.mg,
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="oral dose pravastatin [mg]",
            port=True,
        ),
        Parameter(
            "POSTOMACH_pra",
            0,
            U.mg,
            constant=False,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="oral dose in stomach pravastatin [mg]",
        ),
        Parameter(
            "Ka_application_pra",
            1000,
            U.per_hr,
            constant=True,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="Ka [1/hr] application pravastatin",
            notes="""Fast application to shift applied dose in the stomach.""",
        ),
        Parameter(
            "Ka_dis_pra",
            **FITS.parameter("GU__Ka_dis_pra", unit=U.per_hr),
            constant=True,
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            name="Ka_dis [1/hr] dissolution pravastatin",
            notes="""Dissolution of the tablet and gastric emptying (fasted).""",
        ),
        Parameter(
            "Mr_pra",
            424.53,
            U.g_per_mole,
            constant=True,
            name="Molecular weight pravastatin [g/mole]",
            sboTerm=SBO.MOLECULAR_MASS,
            port=True,
        ),
    ]
)

# -------------------------------------
# Dissolution of tablet/dose in stomach
# -------------------------------------
_m.reactions.extend(
    [
        # fraction dose available for absorption from stomach
        Reaction(
            sid="application_pra",
            name="PO application pravastatin",
            formula=(
                "Ka_application_pra/60 min_per_hr * PODOSE_pra/Mr_pra",
                U.mmole_per_min,
            ),
            equation=" -> pra_stomach",
            compartment="Vgu",
        ),
        # fraction dose available for absorption from stomach
        Reaction(
            sid="dissolution_pra",
            name="dissolution pravastatin",
            formula=(
                "f_dissolution * Ka_dis_pra/60 min_per_hr * POSTOMACH_pra/Mr_pra",
                U.mmole_per_min,
            ),
            equation="pra_stomach -> pra_lumen",
            compartment="Vgu",
        ),
    ]
)
_m.rate_rules.extend(
    [
        RateRule("PODOSE_pra", "-application_pra * Mr_pra", U.mg_per_min),
        RateRule(
            "POSTOMACH_pra",
            "(application_pra - dissolution_pra) * Mr_pra",
            U.mg_per_min,
        ),
    ]
)

model_intestine = _m


if __name__ == "__main__":
    from pkdb_models.models.pravastatin import MODEL_BASE_PATH

    result = create_model(
        filepath=MODEL_BASE_PATH / f"{model_intestine.sid}.xml",
        model=model_intestine,
        sbml_level=3,
        sbml_version=2,
    )
