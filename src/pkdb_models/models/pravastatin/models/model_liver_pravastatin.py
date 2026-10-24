"""Pravastatin part of the liver model.

The hepatic uptake of pravastatin from the plasma via OATP1B1 (SLCO1B1) and
its biliary excretion via MRP2 into the intestinal lumen, from which it is
partly reabsorbed (enterohepatic circulation, see the intestine model). The
bile is not a state of its own: the biliary excretion goes into the lumen
directly. The metabolism of pravastatin in the liver (SQ31945, about 13 % of
an intravenous dose in the urine as metabolites, Singhvi1990) is not modeled.
"""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    Model,
    Parameter,
    Reaction,
    Species,
    create_model,
)
from sbmlutils.metadata import SBO

from pkdb_models.models.pravastatin.models import annotations, templates
from pkdb_models.models.pravastatin.models.fits import FITS


class U(templates.U):
    """UnitDefinitions."""


_m = Model(
    "pravastatin_liver_pravastatin",
    name="Model for pravastatin elimination in the liver",
    notes="""
    # Model for pravastatin elimination in the liver

    Model for hepatic uptake of pravastatin via OATP1B1 (SLCO1B1) and subsequent
    excretion in the bile via MRP2 encoded in <a href="http://sbml.org">SBML</a>.

    * no metabolism of pravastatin
    * irreversible uptake and excretion of pravastatin via the bile into the
      intestinal lumen
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)

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
]

_m.reactions = [
    Reaction(
        "PRAIM",
        name="pravastatin import (OATP1B1)",
        equation="pra_ext -> pra",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vbaso",
        pars=[
            Parameter(
                "PRAIM_Vmax",
                **FITS.parameter("LI__PRAIM_Vmax", unit=U.mmole_per_min_l),
                name="Vmax for pravastatin import via OATP1B1",
                sboTerm=SBO.MAXIMAL_VELOCITY,
            ),
            Parameter(
                sid="f_OATP1B1",
                name="parameter for OATP1B1 activity",
                value=1.0,
                unit=U.dimensionless,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes="""
                parameter controls genetic variants (1.0 reference function,
                < 1.0 reduced function, > 1.0 increased function)
                """,
            ),
            Parameter(
                "PRAIM_Km_pra",
                0.01,
                unit=U.mM,
                name="Km for pravastatin import via OATP1B1",
                sboTerm=SBO.MICHAELIS_CONSTANT,
            ),
        ],
        notes="""
        Import of pravastatin via OATP1B1 (SLCO1B1) from the plasma in the liver.
        Here the genetic variants of SLCO1B1 and the inhibition of OATP1B1 have
        their effects.

        Irreversible import of pravastatin via Michaelis-Menten kinetics. The
        Km of 10 µM is far above the plasma concentrations (0.01-0.5 µM), so
        the uptake is linear and Vmax/Km sets the intrinsic clearance; the
        hepatic extraction is about 0.5 (F 0.17-0.18 with a fraction absorbed
        of 0.34, Singhvi1990).
        """,
        formula=(
            "f_OATP1B1 * PRAIM_Vmax * Vli * pra_ext/(pra_ext + PRAIM_Km_pra)",
            U.mmole_per_min,
        ),
    ),
    Reaction(
        "PRAEX",
        name="pravastatin bile export (MRP2)",
        equation="pra -> pra_lumen",
        sboTerm=SBO.TRANSPORT_REACTION,
        compartment="Vli",
        pars=[
            Parameter(
                "PRAEX_k",
                0.1,
                unit=U.per_min,
                name="rate for pravastatin export via MRP2",
                sboTerm=SBO.KINETIC_CONSTANT,
                notes="""
                Rate of the biliary excretion, a half-life of pravastatin in
                the liver of about 7 min. It changes only the timing of the
                enterohepatic circulation, not the exposure, and is not
                fitted.
                """,
            ),
            Parameter(
                sid="f_MRP2",
                name="parameter for MRP2 activity",
                value=1.0,
                unit=U.dimensionless,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                notes="""
                parameter controls genetic variants (1.0 reference function,
                < 1.0 reduced function, > 1.0 increased function)
                """,
            ),
        ],
        notes="""
        Export of pravastatin via MRP2 from the liver into the bile, which
        flows into the intestinal lumen (enterohepatic circulation). Here the
        genetic variants of MRP2 have their effects.

        Irreversible first order export.
        """,
        formula=(
            "f_MRP2 * PRAEX_k * Vli * pra",
            U.mmole_per_min,
        ),
    ),
]

model_liver_pravastatin = _m

if __name__ == "__main__":
    from pkdb_models.models.pravastatin import MODEL_BASE_PATH
    from pkdb_models.models.pravastatin.models.model_liver_base import model_liver_base

    result = create_model(
        filepath=MODEL_BASE_PATH / f"{model_liver_pravastatin.sid}.xml",
        model=[
            model_liver_base,
            model_liver_pravastatin,
        ],
        sbml_level=3,
        sbml_version=2,
    )
