"""Kidney model of pravastatin: the renal excretion of pravastatin into the urine.

Pravastatin is filtered and actively secreted in the proximal tubule (OAT3,
SLC22A8): its renal clearance of 0.43-0.46 l/min is more than three times the
filtration of its unbound fraction (Singhvi1990: 6.3 ml/min/kg after 9.9 mg iv,
47 % of the total clearance; Halstenson1992: 25.9 l/hr after 20 mg po at a
creatinine clearance of 101 ml/min). The renal clearance is `PRAEX_f` times
the filtration of the unbound pravastatin, `fu_pra * GFR`, with the glomerular
filtration rate `GFR = f_renal_function * GFR_base`; the secreted part above
the filtration scales with the activity of OAT3 (`f_OAT3`, e.g. its inhibition
by gemfibrozil).

- 5-10 % of an oral dose of pravastatin is excreted in the urine as
  pravastatin, 47 % of an intravenous dose (Singhvi1990).
- "After the intravenous dose, the recovery of radioactivity averaged 60% and 34%
  in urine and faeces, respectively. Corresponding values were 20% (urine) and 71%
  (faeces) for the oral dose." {Singhvi1990}

The metabolites SQ31906 (3'alpha-isopravastatin) and SQ31945
(3'alpha-5'beta-6'beta-trihydroxypravastatin) are not modeled; `pra` is
pravastatin.
"""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    AssignmentRule,
    Compartment,
    Model,
    Parameter,
    Reaction,
    Species,
    create_model,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.pravastatin.models import annotations, templates
from pkdb_models.models.pravastatin.models.fits import FITS


class U(templates.U):
    """UnitDefinitions."""


_m = Model(
    "pravastatin_kidney",
    name="Model for pravastatin elimination in the kidneys",
    notes="""
    # Model for pravastatin elimination in the kidneys

    Model for the renal excretion of pravastatin by glomerular filtration and
    tubular secretion (OAT3), relative to the glomerular filtration rate,
    encoded in <a href="http://sbml.org">SBML</a> format.
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
        "Vki",
        0.3,
        name="kidney",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["ki"],
    ),
    Compartment(
        "Vurine",
        1.0,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        unit=U.liter,
        port=True,
        annotations=annotations.compartments["urine"],
    ),
]

_m.species = [
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
        "pra_urine",
        initialConcentration=0.0,
        name="pravastatin (urine)",
        compartment="Vurine",
        substanceUnit=U.mmole,
        hasOnlySubstanceUnits=True,
        sboTerm=SBO.SIMPLE_CHEMICAL,
        annotations=annotations.species["pra"],
        port=True,
        notes="""
        Urinary species are in amounts.
        """,
    ),
]

_m.parameters = [
    Parameter(
        sid="f_renal_function",
        name="renal function",
        value=1.0,
        unit=U.dimensionless,
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        >1.0: increased kidney function
        1.0: normal kidney function (healthy control)
        <1.0: decreased kidney function

        Renal function relative to the healthy glomerular filtration rate
        GFR_base, which is 101 ml/min at 75 kg; a measured creatinine
        clearance of X ml/min is the renal function X/101.
        """,
    ),
    Parameter(
        "GFR_base",
        101,
        U.ml_per_min,
        name="glomerular filtration rate (healthy)",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
    ),
    Parameter(
        "fu_pra",
        0.5,
        U.dimensionless,
        name="fraction unbound in plasma pravastatin",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        port=True,
    ),
    Parameter(
        "PRAEX_f",
        **FITS.parameter("KI__PRAEX_f", unit=U.dimensionless),
        name="renal clearance of unbound pravastatin relative to the GFR",
        sboTerm=SBO.KINETIC_CONSTANT,
        notes="""
        The renal clearance of pravastatin is PRAEX_f times the filtration of
        its unbound fraction, fu_pra * GFR: 1 is filtration alone, above 1 a
        net tubular secretion (OAT3). The clearance from the plasma of the
        kidney is limited by the renal plasma flow, so the effective renal
        clearance of 0.42-0.46 l/min (Singhvi1990) needs a value of about 16
        (fitted).
        """,
    ),
    Parameter(
        "f_OAT3",
        1.0,
        U.dimensionless,
        name="parameter for OAT3 activity",
        sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        notes="""
        Activity of the tubular secretion of pravastatin by OAT3 (SLC22A8)
        (1.0 reference function, < 1.0 inhibition, e.g. by gemfibrozil). It
        scales the secreted part of the renal clearance, PRAEX_f - 1, not the
        filtration.
        """,
    ),
]
_m.rules.append(
    AssignmentRule(
        "GFR",
        "f_renal_function * GFR_base",
        unit=U.ml_per_min,
        name="glomerular filtration rate",
    )
)

_m.reactions = [
    Reaction(
        "PRAEX",
        name="excretion pravastatin",
        equation="pra_ext -> pra_urine",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vki",
        # [ml/min] * [l/ml] * [-] * [-] * [mmole/l]
        formula=(
            "GFR * 0.001 l_per_ml * fu_pra"
            " * (1 dimensionless + f_OAT3 * (PRAEX_f - 1 dimensionless)) * pra_ext",
            U.mmole_per_min,
        ),
        annotations=[(BQB.IS, "ncit/C75913")],  # renal clearance
    ),
]

model_kidney = _m


if __name__ == "__main__":
    from pkdb_models.models.pravastatin import MODEL_BASE_PATH

    result = create_model(
        filepath=MODEL_BASE_PATH / f"{model_kidney.sid}.xml",
        model=model_kidney,
        sbml_level=3,
        sbml_version=2,
    )
