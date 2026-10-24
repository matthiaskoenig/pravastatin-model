"""Whole-body model of pravastatin.

The PBPK model of pravastatin (`pra`) with the oral and intravenous dosing. The
intestine, the liver and the kidney are submodels.

- "Absolute average bioavailability of pravastatin is low at 17% based on urinary
  excretion data." {Singhvi et al. 1990}
- After 9.9 mg intravenously the total clearance is 13.5 ml/min/kg, the renal
  clearance 6.3 ml/min/kg (47 % of the dose in the urine) and the volume of
  distribution at steady state 0.46 l/kg (Singhvi1990).
- About 50 % of pravastatin is bound to plasma proteins (Pravachol label);
  the unbound fraction `fu_pra` enters the renal clearance.
- "The oral absorption of [14C] activity from pravastatin sodium was about 34% and
  the oral bioavailability was about 18%, suggesting first-pass metabolism of
  pravastatin."
- "SQ31906 is formed from pravastatin predominantly in the stomach at acidic pH."

The metabolites SQ31906 (3'alpha-isopravastatin) and SQ31945
(3'alpha-5'beta-6'beta-trihydroxypravastatin) are not modeled.
"""

from typing import NotRequired, TypedDict

import numpy as np
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    PORT_SUFFIX,
    AssignmentRule,
    Compartment,
    ExternalModelDefinition,
    Model,
    Parameter,
    RateRule,
    Reaction,
    ReplacedElement,
    Species,
    Submodel,
    UnitDefinition,
    create_model,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.pravastatin.models import annotations, templates
from pkdb_models.models.pravastatin.models.fits import FITS


# -----------------------------------------------------------------------------
# Whole Body Metabolism
# -----------------------------------------------------------------------------
class U(templates.U):
    """UnitsDefinitions."""

    cm = UnitDefinition("cm")
    hr = UnitDefinition("hr")
    kg = UnitDefinition("kg")

    l_per_hr = UnitDefinition("l_per_hr", "l/hr")
    l_per_kg = UnitDefinition("l_per_kg", "l/kg")
    l_per_min_kg = UnitDefinition("l_per_min_kg", "l/min/kg")
    l_per_mmole = UnitDefinition("l_per_mmole", "l/mmole")

    m2_per_kg = UnitDefinition("m2_per_kg", "meter^2/kg")

    mg_per_day = UnitDefinition("mg_per_day", "mg/day")
    mg_per_g = UnitDefinition("mg_per_g", "mg/g")
    mg_per_hr = UnitDefinition("mg_per_hr", "mg/hr")
    mg_per_l = UnitDefinition("mg_per_l", "mg/l")
    mg_per_min = UnitDefinition("mg_per_min", "mg/min")

    min_per_day = UnitDefinition("min_per_day", "min/day")
    min_per_hr = UnitDefinition("min_per_hr", "min/hr")

    ml = UnitDefinition("ml")
    ml_per_s = UnitDefinition("ml_per_s", "ml/s")
    ml_per_s_kg = UnitDefinition("ml_per_s_kg", "ml/s/kg")

    mmole_per_hr = UnitDefinition("mmole_per_hr", "mmole/hr")
    mmole_per_l = UnitDefinition("mmole_per_l", "mmole/l")
    mmole_per_min_kg = UnitDefinition("mmole_per_min_kg", "mmole/min/kg")
    mmole_per_hr_ml = UnitDefinition("mmole_per_hr_ml", "mmole/hr/ml")

    mul_per_g = UnitDefinition("mulitre_per_g", "microlitre/g")
    mul_per_min_mg = UnitDefinition("mul_per_min_mg", "microliter/min/mg")

    per_hr = UnitDefinition("per_hr", "1/hr")
    per_min_kg = UnitDefinition("per_min_kg", "1/min/kg")

    s_per_min = UnitDefinition("s_per_min", "s/min")


_m = Model(
    "pravastatin_body_pravastatin",
    name="Pravastatin (PRA) body model",
    notes="""
    # PK/PD model for whole-body pravastatin metabolism.
    """
    + terms_of_use,
    units=U,
    model_units=templates.model_units,
    creators=templates.creators,
    annotations=[
        (BQB.IS, "taxonomy/9606"),  # Homo sapiens
    ],
)

_m.ports = []
_m.deletions = []
_m.replaced_elements = []


class SubstanceBody(TypedDict):
    """Definition of a substance transported in the whole-body model."""

    name: str
    unit: UnitDefinition
    cinit: float  # initial concentration [mmole/l]
    Mr: float  # molecular weight [g/mole]
    IVDOSE: NotRequired[float]  # intravenous dose [mg]
    PODOSE: NotRequired[float]  # oral dose [mg]
    fu: float  # fraction unbound in plasma [-]
    ftissue: float  # distribution in tissues [litre/min]
    Kpdeep: NotRequired[float]  # deep/tissue partition coefficient [-]
    kdeep: NotRequired[float]  # rate of the deep distribution [1/min]
    annotations: list[tuple[BQB, str]]


SUBSTANCES_BODY: dict[str, SubstanceBody] = {
    "pra": {
        "name": "pravastatin",
        "unit": U.mmole,
        # initial concentration
        "cinit": 0.0,  # [mmole/l]
        # Molecular weight
        "Mr": 424.53,  # [g/mole]
        # iv doses [mg]
        "IVDOSE": 0,
        # oral absorption
        "PODOSE": 0,
        # fraction unbound in plasma, about 50 % bound (Pravachol label)
        "fu": 0.5,
        # tissue distribution: Vss 0.46 l/kg (Singhvi1990); the exchange is
        # fast, the plasma concentration falls 4-fold in the first 20 min
        # after an intravenous dose, which every fit put at the upper bound
        # of 20 l/min, so it is fixed there and not fitted
        "ftissue": 20.0,  # [litre_per_min] rate of distribution in tissues
        # the tissue/plasma partition coefficient Kp is fitted, see `fits.FITS`
        # slow distribution into a deep compartment of the rest tissue: the
        # beta phase after 1 hr (iv t1/2 0.78 hr, Singhvi1990: 30, 17, 10,
        # 4.6 ng/ml at 1, 1.5, 2, 3 hr). The fits do not identify the two
        # values (flat profiles over the bounds), so they are fixed to the
        # least squares of the log concentrations of Singhvi1990 0.34-3 hr
        # with the fitted PK (Vss 31 l against 34 l)
        "Kpdeep": 0.85,  # [-] deep/tissue partition coefficient
        "kdeep": 0.011,  # [1/min] rate of the deep distribution
        "annotations": annotations.species["pra"],
    },
}

# -----------------------------------------------------------------------------
# Submodels
# -----------------------------------------------------------------------------
COMPARTMENTS_BODY = {
    "gu": "gut",
    "ki": "kidney",
    "li": "liver",
    "lu": "lung",
    "re": "rest",
    "ar": "arterial blood",
    "ve": "venous blood",
    "po": "portal vein",
    "hv": "hepatic vein",
}

SUBMODEL_SID_DICT = {  # tissue to submodel mapping
    "ki": "KI",  # kidney
    "li": "LI",  # liver
    "gu": "GU",  # Gut
}

kidney_id = "pravastatin_kidney"
liver_id = "pravastatin_liver_pravastatin"
gut_id = "pravastatin_intestine"

_m.external_model_definitions = [
    ExternalModelDefinition(
        sid="liver",
        name="liver model definition",
        source=f"{liver_id}.xml",
        modelRef=liver_id,
    ),
    ExternalModelDefinition(
        sid="kidney",
        name="kidney model definition",
        source=f"{kidney_id}.xml",
        modelRef=kidney_id,
    ),
    ExternalModelDefinition(
        sid="gut", name="gut model definition", source=f"{gut_id}.xml", modelRef=gut_id
    ),
]

_m.submodels = [
    Submodel(sid=SUBMODEL_SID_DICT["ki"], modelRef="kidney", name="kidney submodel"),
    Submodel(sid=SUBMODEL_SID_DICT["li"], modelRef="liver", name="liver submodel"),
    Submodel(sid=SUBMODEL_SID_DICT["gu"], modelRef="gut", name="gut submodel"),
]

# -------------------------------------------------------------------------------------------------
# Compartments
# -------------------------------------------------------------------------------------------------
_m.compartments = [
    Compartment(
        "Vre",
        metaId="meta_Vre",
        value=1,
        unit=U.liter,
        constant=False,
        name="rest of body",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["re"],
    ),
    Compartment(
        "Vgu",
        metaId="meta_Vgu",
        value=1,
        unit=U.liter,
        constant=False,
        name="gut",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["gu"],
    ),
    Compartment(
        "Vki",
        metaId="meta_Vki",
        value=1,
        unit=U.liter,
        constant=False,
        name="kidney",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ki"],
    ),
    Compartment(
        "Vli",
        metaId="meta_Vli",
        value=1,
        unit=U.liter,
        constant=False,
        name="liver",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["li"],
    ),
    Compartment(
        "Vlu",
        metaId="meta_Vlu",
        value=1,
        unit=U.liter,
        constant=False,
        name="lung",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["lu"],
    ),
    Compartment(
        "Vve",
        metaId="meta_Vve",
        value=1,
        unit=U.liter,
        constant=False,
        name="venous blood",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ve"],
    ),
    Compartment(
        "Var",
        metaId="meta_Var",
        value=1,
        unit=U.liter,
        constant=False,
        name="arterial blood",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["ar"],
    ),
    Compartment(
        "Vurine",
        metaId="meta_Vurine",
        value=1,
        unit=U.liter,
        constant=True,
        name="urine",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["urine"],
    ),
    Compartment(
        "Vfeces",
        metaId="meta_Vfeces",
        value=1,
        unit=U.liter,
        constant=True,
        name="feces",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
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
        annotations=annotations.compartments["stomach"],
    ),
    Compartment(
        "Vpo",
        metaId="meta_Vpo",
        value=1,
        unit=U.liter,
        constant=False,
        name="portal plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["po"],
    ),
    Compartment(
        "Vhv",
        metaId="meta_Vhv",
        value=1,
        unit=U.liter,
        constant=False,
        name="hepatic venous plasma",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
        annotations=annotations.compartments["hv"],
    ),
]

# create plasma and tissue compartments (for correct blood volume)
for cid in COMPARTMENTS_BODY:
    if cid not in ["ar", "ve", "po", "hv"]:
        _m.compartments.extend(
            [
                Compartment(
                    f"V{cid}_tissue",
                    value=1,
                    unit=U.liter,
                    constant=False,
                    name=f"{cid} tissue",
                    metaId=f"meta_V{cid}_tissue",
                    port=True,
                    annotations=[
                        *annotations.compartments["parenchyma"],
                        *[
                            (BQB.IS_PART_OF, aid[1])
                            for aid in annotations.compartments[cid]
                        ],
                    ],
                    sboTerm=SBO.PHYSICAL_COMPARTMENT,
                ),
                Compartment(
                    f"V{cid}_plasma",
                    value=1,
                    unit=U.liter,
                    constant=False,
                    name=f"{cid} plasma",
                    metaId=f"meta_V{cid}_plasma",
                    port=True,
                    annotations=[
                        *annotations.compartments["plasma"],
                        *[
                            (BQB.IS_PART_OF, aid[1])
                            for aid in annotations.compartments[cid]
                        ],
                    ],
                    sboTerm=SBO.PHYSICAL_COMPARTMENT,
                ),
            ]
        )


# calculate gut lumen
_m.compartments.append(
    Compartment(
        "Vgulumen",
        metaId="meta_Vgulumen",
        value=1,
        unit=U.liter,
        constant=False,
        name="gut lumen",
        sboTerm=SBO.PHYSICAL_COMPARTMENT,
    )
)
_m.parameters = [
    Parameter("f_lumen", 0.9, name="fraction lumen of intestine", unit=U.dimensionless)
]
_m.rules = [
    AssignmentRule("Vgulumen", "f_lumen * Vgu", unit=U.liter),
]

# replace volumes of submodels
_m.replaced_elements.extend(
    [
        # kidney
        ReplacedElement(
            sid="Vki_tissue_RE",
            metaId="Vki_tissue_RE",
            elementRef="Vki_tissue",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"Vki{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vki_plasma_RE",
            metaId="Vki_plasma_RE",
            elementRef="Vki_plasma",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"Vext{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vurine_RE",
            metaId="Vurine_RE",
            elementRef="Vurine",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"Vurine{PORT_SUFFIX}",
        ),
        # liver
        ReplacedElement(
            sid="Vli_tissue_RE",
            metaId="Vli_tissue_RE",
            elementRef="Vli_tissue",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"Vli{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vli_plasma_RE",
            metaId="Vli_plasma_RE",
            elementRef="Vli_plasma",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"Vext{PORT_SUFFIX}",
        ),
        # intestine
        ReplacedElement(
            sid="Vstomach_RE",
            metaId="Vstomach_RE",
            elementRef="Vstomach",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vstomach{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vgu_plasma_RE",
            metaId="Vgu_plasma_RE",
            elementRef="Vgu_plasma",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vext{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vgulumen_RE",
            metaId="Vgulumen_RE",
            elementRef="Vgulumen",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vlumen{PORT_SUFFIX}",
        ),
        # the lumen of the liver model is the gut lumen
        ReplacedElement(
            sid="Vgulumen_li_RE",
            metaId="Vgulumen_li_RE",
            elementRef="Vgulumen",
            submodelRef=SUBMODEL_SID_DICT["li"],
            portRef=f"Vlumen{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vgu_RE",
            metaId="Vgu_RE",
            elementRef="Vgu",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vgu{PORT_SUFFIX}",
        ),
        ReplacedElement(
            sid="Vfeces_RE",
            metaId="Vfeces_RE",
            elementRef="Vfeces",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"Vfeces{PORT_SUFFIX}",
        ),
    ]
)

# -------------------------------------------------------------------------------------------------
# Species
# -------------------------------------------------------------------------------------------------
_m.species = []
for sid, sdict in SUBSTANCES_BODY.items():
    for cid, cname in COMPARTMENTS_BODY.items():
        if cid in ["ve", "ar", "po", "hv"]:
            sid_ex = f"C{cid}_{sid}"
            cid_ex = f"V{cid}"
        else:
            # plasma compartment
            sid_ex = f"C{cid}_plasma_{sid}"
            cid_ex = f"V{cid}_plasma"

        _m.species.append(
            Species(
                sid_ex,
                metaId=f"meta_{sid_ex}",
                initialConcentration=sdict["cinit"],
                compartment=cid_ex,
                substanceUnit=sdict["unit"],
                name=f"{sdict['name']} ({cname} plasma)",
                hasOnlySubstanceUnits=False,
                port=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
            )
        )

    # tissue species
    for cid, cname in COMPARTMENTS_BODY.items():
        if (
            "ftissue" in sdict
            and not np.isclose(sdict["ftissue"], 0.0)
            and cid not in ["ve", "ar", "li", "ki", "gu", "po", "hv"]
        ):
            sid_ex = f"C{cid}_{sid}"
            cid_ex = f"V{cid}_tissue"

            _m.species.extend(
                [
                    Species(
                        sid_ex,
                        metaId=f"meta_{sid_ex}",
                        initialConcentration=sdict["cinit"],
                        compartment=cid_ex,
                        substanceUnit=sdict["unit"],
                        name=f"{sdict['name']} ({cname})",
                        hasOnlySubstanceUnits=False,
                        port=True,
                        sboTerm=SBO.SIMPLE_CHEMICAL,
                        annotations=annotations.species[sid],
                    )
                ]
            )
            if cid == "re" and "kdeep" in sdict:
                # the slow distribution into the deep tissue
                _m.species.append(
                    Species(
                        f"C{cid}_deep_{sid}",
                        metaId=f"meta_C{cid}_deep_{sid}",
                        initialConcentration=sdict["cinit"],
                        compartment=cid_ex,
                        substanceUnit=sdict["unit"],
                        name=f"{sdict['name']} deep ({cname})",
                        hasOnlySubstanceUnits=False,
                        sboTerm=SBO.SIMPLE_CHEMICAL,
                        annotations=annotations.species[sid],
                    )
                )

    # urine metabolites & stomach dummy species
    if sid in ["pra"]:
        _m.species.extend(
            [
                Species(
                    f"Aurine_{sid}",
                    metaId=f"meta_Aurine_{sid}",
                    initialConcentration=0,
                    compartment="Vurine",
                    substanceUnit=sdict["unit"],
                    name=f"{sdict['name']} (urine)",
                    hasOnlySubstanceUnits=True,
                    sboTerm=SBO.SIMPLE_CHEMICAL,
                    annotations=annotations.species[sid],
                ),
            ]
        )

    # feces metabolites
    if sid in ["pra"]:
        _m.species.append(
            Species(
                f"Afeces_{sid}",
                metaId=f"meta_Afeces_{sid}",
                initialConcentration=0,
                compartment="Vfeces",
                substanceUnit=sdict["unit"],
                name=f"{sdict['name']} (feces)",
                hasOnlySubstanceUnits=True,
                sboTerm=SBO.SIMPLE_CHEMICAL,
                annotations=annotations.species[sid],
            )
        )

# replace species
replaced_species = {
    "li": ["pra"],
    "ki": ["pra"],
    "gu": ["pra"],
}

# blood to external species
for tkey, skey_list in replaced_species.items():
    for skey in skey_list:
        _m.replaced_elements.extend(
            [
                ReplacedElement(
                    sid=f"C{tkey}_plasma_{skey}_RE",
                    metaId=f"C{tkey}_plasma_{skey}_RE",
                    elementRef=f"C{tkey}_plasma_{skey}",
                    submodelRef=SUBMODEL_SID_DICT[tkey],
                    portRef=f"{skey}_ext{PORT_SUFFIX}",
                ),
            ]
        )

# urine species replacements
for skey in ["pra"]:
    _m.replaced_elements.append(
        ReplacedElement(
            sid=f"Aurine_{skey}_RE",
            metaId=f"Aurine_{skey}_RE",
            elementRef=f"Aurine_{skey}",
            submodelRef=SUBMODEL_SID_DICT["ki"],
            portRef=f"{skey}_urine{PORT_SUFFIX}",
        )
    )

# feces species replacements
for skey in ["pra"]:
    _m.replaced_elements.append(
        ReplacedElement(
            sid=f"Afeces_{skey}_RE",
            metaId=f"Afeces_{skey}_RE",
            elementRef=f"Afeces_{skey}",
            submodelRef=SUBMODEL_SID_DICT["gu"],
            portRef=f"{skey}_feces{PORT_SUFFIX}",
        )
    )

# gut absorption (mapping of species)
for sid in ["pra"]:
    # enterohepatic circulation
    _m.species.append(
        Species(
            sid=f"Cgulumen_{sid}",
            initialConcentration=0.0,
            metaId=f"meta_Cgulumen_{sid}",
            name="pravastatin (gut lumen)",
            compartment="Vgulumen",
            substanceUnit=U.mmole,
            hasOnlySubstanceUnits=False,
            port=True,
        )
    )

    _m.replaced_elements.extend(
        [
            ReplacedElement(
                sid=f"Cgulumen_{sid}_RE1",
                metaId=f"Cgulumen_{sid}_RE1",
                elementRef=f"Cgulumen_{sid}",
                submodelRef=SUBMODEL_SID_DICT["gu"],
                portRef=f"{sid}_lumen{PORT_SUFFIX}",
            ),
            ReplacedElement(
                sid=f"Cgulumen_{sid}_RE2",
                metaId=f"Cgulumen_{sid}_RE2",
                elementRef=f"Cgulumen_{sid}",
                submodelRef=SUBMODEL_SID_DICT["li"],
                portRef=f"{sid}_lumen{PORT_SUFFIX}",
            ),
        ]
    )

# -------------------------------------------------------------------------------------------------
# Parameters
# -------------------------------------------------------------------------------------------------
_m.parameters.extend(
    [
        # whole body data
        Parameter(
            "BW",
            75,
            U.kg,
            constant=True,
            name="body weight [kg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "BW_ref",
            75,
            U.kg,
            constant=True,
            name="reference body weight [kg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes=(
                "Body weight at which the exchange flows of the tissue "
                "distribution (`ftissue_<sid>`) are given; they scale with the "
                "body weight as the volumes, the blood flows and the renal "
                "clearance do."
            ),
        ),
        Parameter(
            "HEIGHT",
            170,
            U.cm,
            constant=True,
            name="height [cm]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "HR",
            70,
            U.per_min,
            constant=True,
            name="heart rate [1/min]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "HRrest",
            70,
            U.per_min,
            constant=True,
            name="resting heart rate [1/min]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "BSA",
            0,
            U.m2,
            constant=False,
            name="body surface area [m^2]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # 1.548,
        Parameter(
            "COBW",
            1.25,
            U.ml_per_s_kg,
            constant=True,
            name="cardiac output per bodyweight [ml/s/kg]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "CO",
            np.nan,
            U.ml_per_s,
            constant=False,
            name="cardiac output [ml/s]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            annotations=[
                (BQB.IS, "ncit/C119246"),
                (BQB.IS, "omit/0003637"),
            ],
            notes="""BW*COBW (100 ml/s)""",
        ),
        Parameter(
            "QC",
            np.nan,
            U.l_per_min,
            constant=False,
            name="cardiac output [L/min]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            annotations=[
                (BQB.IS, "ncit/C119246"),
                (BQB.IS, "omit/0003637"),
            ],
        ),
        Parameter(
            "COHRI",
            150,
            U.ml,
            constant=True,
            name="increase of cardiac output per heartbeat [ml/min*min]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # fractional tissue volumes
        Parameter(
            "Fblood",
            0.02,
            U.dimensionless,
            constant=False,
            name="blood fraction of organ volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "HCT",
            0.51,
            U.dimensionless,
            constant=True,
            metaId="meta_HCT",
            name="hematocrit",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # fractional tissue volumes
        Parameter(
            "FVgi",
            0.0297,
            U.l_per_kg,
            constant=True,
            name="fractional tissue volume gastrointestinal tract",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""FVgi = FVgu + FVpa + FVsp = 0.0171 + 0.01 + 0.0026 = 0.0297""",
            annotations=[
                (BQB.IS_VERSION_OF, item[1]) for item in annotations.compartments["gi"]
            ],
        ),
        Parameter(
            "FVki",
            0.0044,
            U.l_per_kg,
            constant=True,
            name="kidney fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVli",
            0.0210,
            U.l_per_kg,
            constant=True,
            name="liver fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVlu",
            0.0076,
            U.l_per_kg,
            constant=True,
            name="lung fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVre",
            0,
            U.l_per_kg,
            constant=False,
            name="rest of body fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # calculated based on other tissues
        Parameter(
            "FVve",
            0.0514,
            U.l_per_kg,
            constant=True,
            name="venous fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVar",
            0.0257,
            U.l_per_kg,
            constant=True,
            name="arterial fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVpo",
            0.001,
            U.l_per_kg,
            constant=True,
            name="portal fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FVhv",
            0.001,
            U.l_per_kg,
            constant=True,
            name="hepatic venous fractional tissue volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        # fractional tissue blood flows
        Parameter(
            "FQgu",
            0.18,
            U.dimensionless,
            constant=True,
            name="gut fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
        Assumed FQgu is the sum of FQgu + FQsp + FQpa for correct portal blood flow.
        with FQgu=0.146, FQsp=0.017, FQpa=0.017
        """,
        ),
        Parameter(
            "FQki",
            0.190,
            U.dimensionless,
            constant=True,
            name="kidney fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FQh",
            0.215,
            U.dimensionless,
            constant=True,
            name="hepatic (venous side) fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FQlu",
            1,
            U.dimensionless,
            constant=True,
            name="lung fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "FQre",
            0,
            U.dimensionless,
            constant=False,
            name="rest of body fractional tissue blood flow",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "conversion_min_per_day",
            1440,
            U.min_per_day,
            constant=True,
            name="Conversion factor min to day",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "f_cirrhosis",
            0,
            U.dimensionless,
            constant=True,
            name="severity of cirrhosis [0, 0.95]",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            annotations=[
                (BQB.IS, "ncit/C2951"),  # Cirrhosis
                (BQB.IS, "efo/0001422"),  # cirrhosis of liver
            ],
        ),
        Parameter(
            "f_shunts",
            0,
            U.dimensionless,
            constant=False,
            name="fraction of portal venous blood shunted by the liver",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            annotations=[
                (
                    BQB.IS,
                    "hp/HP:0002629",
                ),  # Gastrointestinal arteriovenous malformation
            ],
        ),
        Parameter(
            "f_tissue_loss",
            0,
            U.dimensionless,
            constant=False,
            name="fraction of lost parenchymal liver volume",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
    ]
)

# free concentration and renal function
_m.parameters.extend(
    [
        Parameter(
            "fu_pra",
            SUBSTANCES_BODY["pra"]["fu"],
            U.dimensionless,
            metaId="meta_fu_pra",
            constant=True,
            name="fraction unbound in plasma pravastatin",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
        ),
        Parameter(
            "f_GFR_Qki",
            101 / 1.06875,
            U.ml_per_l,
            constant=True,
            name="relationship GFR and Qki",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            GFR per renal blood flow (94.5 ml/l). Calibrated so that the
            healthy GFR is 101 ml/min at the renal blood flow of 1.06875 l/min
            of 75 kg, the normal GFR of the classes of renal impairment
            (`pkpdsim.impairment`).
            """,
        ),
        Parameter(
            "GFR_base",
            np.nan,
            U.ml_per_min,
            constant=False,
            name="glomerular filtration rate (healthy)",
            sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
            notes="""
            The GFR of healthy kidneys, which scales with the renal blood flow
            and so with the body weight; the GFR is `KI__f_renal_function`
            times this rate.
            """,
        ),
    ]
)

_m.rules = [
    *_m.rules,
    AssignmentRule("f_shunts", "f_cirrhosis", unit=U.dimensionless),
    AssignmentRule("f_tissue_loss", "f_cirrhosis", unit=U.dimensionless),
]

replaced_parameters = {
    "li": [],
    "gu": ["Mr_pra"],
    "ki": ["fu_pra", "GFR_base"],
}

for ckey, pids in replaced_parameters.items():
    for pid in pids:
        _m.replaced_elements.append(
            ReplacedElement(
                sid=f"{pid}_{ckey}_RE",
                metaId=f"{pid}_{ckey}_RE",
                elementRef=f"{pid}",
                submodelRef=SUBMODEL_SID_DICT[ckey],
                portRef=f"{pid}{PORT_SUFFIX}",
            )
        )

# species specific parameters
for sid, sdict in SUBSTANCES_BODY.items():
    _m.parameters.extend(
        [
            # molecular weights
            Parameter(
                f"Mr_{sid}",
                sdict["Mr"],
                U.g_per_mole,
                constant=True,
                name=f"Molecular weight {sid} [g/mole]",
                sboTerm=SBO.MOLECULAR_MASS,
            ),
        ]
    )

    # tissue distribution
    if ("ftissue" in sdict) and (not np.isclose(sdict["ftissue"], 0.0)):
        _m.parameters.extend(
            [
                Parameter(
                    f"ftissue_{sid}",
                    sdict["ftissue"],
                    U.l_per_min,
                    constant=True,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"tissue distribution {sid}",
                    notes="Exchange flow at the reference body weight `BW_ref`.",
                ),
                Parameter(
                    f"Kp_{sid}",
                    **FITS.parameter(f"Kp_{sid}", unit=U.dimensionless),
                    constant=True,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"tissue/plasma partition coefficient {sid}",
                ),
            ]
        )
    if "kdeep" in sdict:
        _m.parameters.extend(
            [
                Parameter(
                    f"Kpdeep_{sid}",
                    sdict["Kpdeep"],
                    U.dimensionless,
                    constant=True,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"deep/tissue partition coefficient {sid}",
                    notes="""
                    Ratio of the deep to the free concentration of the rest
                    tissue in the equilibrium of the slow distribution: with
                    `Kp` it sets the volume of distribution of the terminal
                    phase.
                    """,
                ),
                Parameter(
                    f"kdeep_{sid}",
                    sdict["kdeep"],
                    U.per_min,
                    constant=True,
                    sboTerm=SBO.KINETIC_CONSTANT,
                    name=f"rate of the deep distribution {sid}",
                    notes="""
                    Rate of the slow exchange between the rest tissue and its
                    deep compartment: the concentrations fall fast in the
                    first 2 hr after a dose (distribution and elimination) and
                    slower after it (terminal half-life 0.8 hr after an
                    intravenous dose, 1.5-2 hr after an oral dose).
                    """,
                ),
            ]
        )

    # dosing
    if "IVDOSE" in sdict:
        _m.parameters.extend(
            [
                Parameter(
                    f"IVDOSE_{sid}",
                    sdict["IVDOSE"],
                    U.mg,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"IV bolus dose {sid} [mg]",
                ),
                # iv kinetics after application
                Parameter(
                    f"ti_{sid}",
                    10,
                    U.second,
                    constant=True,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"injection time {sid} [s]",
                ),
                Parameter(
                    f"Ki_{sid}",
                    0.02,
                    U.per_min,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"Ki [1/min] injection {sid}",
                ),
                # continuous infusion
                Parameter(
                    f"Ri_{sid}",
                    0,
                    U.mg_per_min,
                    constant=True,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"Ri [mg/min] rate of infusion {sid}",
                ),
                Parameter(
                    f"cum_dose_{sid}",
                    0,
                    U.mg,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"Cumulative dose due to infusion {sid}",
                ),
            ]
        )

# -------------------------------------------------------------------------------------------------
# AssignmentRules
# -------------------------------------------------------------------------------------------------
_m.rules = [
    *_m.rules,
    # Rest body volume
    AssignmentRule(
        "FVre",
        "1.0 l_per_kg - (FVgi + FVki + FVli + FVlu + FVve + FVar)",
        U.l_per_kg,
    ),
    # Rest body perfusion
    AssignmentRule("FQre", "1.0 dimensionless - (FQki + FQh)", U.dimensionless),
    # Body surface area (Haycock1978)
    AssignmentRule(
        "BSA", "0.024265 m2 * power(BW/1 kg, 0.5378) * power(HEIGHT/1 cm, 0.3964)", U.m2
    ),
    # cardiac output (depending on heart rate and bodyweight)
    AssignmentRule("CO", "BW*COBW + (HR-HRrest)*COHRI / 60 s_per_min", U.ml_per_s),
    # cardiac output (depending on bodyweight)
    AssignmentRule("QC", "CO/1000 ml_per_l * 60 s_per_min", U.l_per_min),
    # volumes
    AssignmentRule("Vgu", "BW*FVgi", U.liter),
    AssignmentRule("Vki", "BW*FVki", U.liter),
    AssignmentRule("Vli", "BW*FVli", U.liter),
    AssignmentRule("Vlu", "BW*FVlu", U.liter),
    AssignmentRule("Vre", "BW*FVre", U.liter),
    # venous and arterial blood volume (corrected for tissue blood volumes)
    AssignmentRule(
        "Vve",
        "BW*FVve - FVve/(FVar+FVve) * BW * Fblood * (1 l_per_kg - FVve - FVar)",
        U.liter,
    ),
    AssignmentRule(
        "Var",
        "BW*FVar - FVar/(FVar+FVve) * BW * Fblood * (1 l_per_kg - FVve - FVar)",
        U.liter,
    ),
    AssignmentRule(
        "Vpo",
        "(1 dimensionless - HCT) * (BW*FVpo - FVpo/(FVar+FVve+FVpo+FVhv) "
        "* BW * Fblood * (1 l_per_kg - (FVar+FVve+FVpo+FVhv)))",
        U.liter,
    ),
    AssignmentRule(
        "Vhv",
        "(1 dimensionless - HCT) * (BW*FVhv - FVhv/(FVar+FVve+FVpo+FVhv) "
        "* BW * Fblood * (1 l_per_kg - (FVar+FVve+FVpo+FVhv)))",
        U.liter,
    ),
    # blood flows
    AssignmentRule("Qgu", "QC*FQgu", U.l_per_min, name="gut blood flow"),
    AssignmentRule("Qki", "QC*FQki", U.l_per_min, name="kidney blood flow"),
    AssignmentRule(
        "Qh", "QC*FQh", U.l_per_min, name="hepatic (venous side) blood flow"
    ),
    AssignmentRule("Qha", "Qh - Qgu", U.l_per_min, name="hepatic artery blood flow"),
    AssignmentRule("Qlu", "QC*FQlu", U.l_per_min, name="lung blood flow"),
    AssignmentRule("Qre", "QC*FQre", U.l_per_min, name="rest of body blood flow"),
    AssignmentRule("Qpo", "Qgu", U.l_per_min, name="portal blood flow"),
    # glomerular filtration rate of healthy kidneys
    AssignmentRule(
        "GFR_base",
        "f_GFR_Qki * Qki",
        U.ml_per_min,
        name="glomerular filtration rate (healthy)",
    ),
]

# Volumes for explicit tissue models
for cid, cname in COMPARTMENTS_BODY.items():
    if cid not in ["ve", "ar", "po", "hv"]:
        _m.rules.append(
            # plasma volume associated with tissue
            AssignmentRule(
                f"V{cid}_plasma",
                value=f"V{cid} * Fblood * (1 dimensionless - HCT)",
                unit=U.liter,
                name=f"plasma volume of {cname}",
            ),
        )

        if cid == "li":
            _m.rules.append(
                # Cirrhosis: Adjustment of fractional liver tissue volume
                AssignmentRule(
                    f"V{cid}_tissue",
                    value=f"V{cid}*(1 dimensionless - f_tissue_loss) * (1 dimensionless - Fblood)",
                    unit=U.liter,
                    name=f"tissue volume of {cname}",
                ),
            )
        else:
            _m.rules.append(
                AssignmentRule(
                    f"V{cid}_tissue",
                    value=f"V{cid}*(1 dimensionless - Fblood)",
                    unit=U.liter,
                    name=f"tissue volume of {cname}",
                ),
            )

for sid, sdict in SUBSTANCES_BODY.items():
    sname = sdict["name"]

    # injection
    if "IVDOSE" in sdict:
        _m.rules.extend(
            [
                AssignmentRule(
                    f"Ki_{sid}",
                    f"0.693 dimensionless/ti_{sid} * 60 s_per_min",
                    U.per_min,
                    name="injection rate IV",
                    notes="""
                log(2) ~ 0.693 used for conversion of half-life injection time to
                injection rate.
                """,
                ),
            ]
        )

    # ---------------------------------
    # X Amount [mg], C Concentration
    # ---------------------------------
    for cid, cname in COMPARTMENTS_BODY.items():
        if cid not in ["ve", "ar", "po", "hv"]:
            _m.rules.extend(
                [
                    AssignmentRule(
                        f"A{cid}_plasma_{sid}",
                        f"C{cid}_plasma_{sid}*V{cid}_plasma",
                        U.mmole,
                        name=f"{sname} amount ({cname}) [mmole]",
                    ),
                    AssignmentRule(
                        f"X{cid}_plasma_{sid}",
                        f"A{cid}_plasma_{sid}*Mr_{sid}",
                        U.mg,
                        name=f"{sname} amount ({cname}) [mg]",
                    ),
                    AssignmentRule(
                        f"M{cid}_plasma_{sid}",
                        f"A{cid}_plasma_{sid}/V{cid}_plasma*Mr_{sid}",
                        U.mg_per_l,
                        name=f"{sname} concentration ({cname}) [mg/l]",
                    ),
                ]
            )
        else:
            _m.rules.extend(
                [
                    AssignmentRule(
                        f"A{cid}_{sid}",
                        f"C{cid}_{sid}*V{cid}",
                        U.mmole,
                        name=f"{sname} amount ({cname}) [mmole]",
                    ),
                    AssignmentRule(
                        f"X{cid}_{sid}",
                        f"A{cid}_{sid}*Mr_{sid}",
                        U.mg,
                        name=f"{sname} amount ({cname}) [mg]",
                    ),
                    AssignmentRule(
                        f"M{cid}_{sid}",
                        f"A{cid}_{sid}/V{cid}*Mr_{sid}",
                        U.mg_per_l,
                        name=f"{sname} concentration ({cname}) [mg/l]",
                    ),
                ]
            )

    # urine metabolites
    if sid in ["pra"]:
        cid, cname = "urine", "urine"
        _m.rules.append(
            AssignmentRule(
                f"X{cid}_{sid}",
                f"A{cid}_{sid}*Mr_{sid}",
                U.mg,
                name=f"{sname} amount ({cname}) [mg]",
            ),
        )
    # feces metabolites
    if sid in ["pra"]:
        cid, cname = "feces", "feces"
        _m.rules.append(
            AssignmentRule(
                f"X{cid}_{sid}",
                f"A{cid}_{sid}*Mr_{sid}",
                U.mg,
                name=f"{sname} amount ({cname})",
            ),
        )

# --------------------------------------------------------------------------------------------------
# Reactions
# --------------------------------------------------------------------------------------------------
_m.reactions = []

for sid, sdict in SUBSTANCES_BODY.items():
    sname = sdict["name"]

    # --------------------
    # tissue distribution
    # --------------------
    if "ftissue" in sdict:
        for cid in COMPARTMENTS_BODY:
            if cid not in ["ve", "ar", "li", "gu", "ki", "po", "hv"]:
                _m.reactions.append(
                    Reaction(
                        sid=f"transport_{cid}_{sid}",
                        name=f"transport {sname}",
                        formula=(
                            f"ftissue_{sid} * BW/BW_ref * (C{cid}_plasma_{sid}*Kp_{sid} - C{cid}_{sid})",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} <-> C{cid}_{sid}",
                        compartment=f"V{cid}_tissue",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                )
                if cid == "re" and "kdeep" in sdict:
                    _m.reactions.append(
                        Reaction(
                            sid=f"deep_{cid}_{sid}",
                            name=f"deep distribution {sname} (tissue)",
                            formula=(
                                f"kdeep_{sid} * V{cid}_tissue * "
                                f"(Kpdeep_{sid} * C{cid}_{sid} - C{cid}_deep_{sid})",
                                U.mmole_per_min,
                            ),
                            equation=f"C{cid}_{sid} <-> C{cid}_deep_{sid}",
                            compartment=f"V{cid}_tissue",
                            sboTerm=SBO.TRANSPORT_REACTION,
                        ),
                    )

    if "IVDOSE" in sdict:
        _m.reactions.extend(
            [
                # --------------------
                # iv application
                # --------------------
                Reaction(
                    sid=f"iv_{sid}",
                    name=f"iv {sname}",
                    formula=(f"Ki_{sid}*IVDOSE_{sid}/Mr_{sid}", U.mmole_per_min),
                    equation=f"-> Cve_{sid}",
                    sboTerm=SBO.TRANSPORT_REACTION,
                    annotations=[(BQB.IS, "ncit/C38276")],
                    compartment="Vve",
                ),
            ]
        )

    for cid, cname in COMPARTMENTS_BODY.items():
        if cid in ["ve", "ar", "po", "hv"]:
            continue
        # --------------------
        # ve -> lung -> ar
        # --------------------
        if cid == "lu":
            rid_in = f"Flow_ve_{cid}_{sid}"
            name_in = f"inflow {cname} {sname}"

            rid_out = f"Flow_{cid}_ar_{sid}"
            name_out = f"outflow {cname} {sname}"

            # distribution in plasma volume
            _m.reactions.extend(
                [
                    Reaction(
                        sid=rid_in,
                        name=name_in,
                        formula=(f"Q{cid}*Cve_{sid}", U.mmole_per_min),
                        equation=f"Cve_{sid} -> C{cid}_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=rid_out,
                        name=name_out,
                        formula=(
                            f"Q{cid}*C{cid}_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} -> Car_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )
        # --------------------
        # ar -> organ -> ve
        # --------------------
        if cid in ["ki", "re"]:
            rid_in = f"Flow_ar_{cid}_{sid}"
            name_in = f"inflow {cname} {sname}"
            rid_out = f"Flow_{cid}_ve_{sid}"
            name_out = f"outflow {cname} {sname}"

            # only distribution in plasma volume
            _m.reactions.extend(
                [
                    Reaction(
                        sid=rid_in,
                        name=name_in,
                        formula=(f"Q{cid}*Car_{sid}", U.mmole_per_min),
                        equation=f"Car_{sid} -> C{cid}_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=rid_out,
                        name=name_out,
                        formula=(
                            f"Q{cid}*C{cid}_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} -> Cve_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )
        # --------------------
        # ar -> organ -> po
        # --------------------
        if cid in ["gu"]:
            rid_in = f"Flow_ar_{cid}_{sid}"
            name_in = f"inflow {cname} {sname}"
            rid_out = f"Flow_{cid}_po_{sid}"
            name_out = f"outflow {cname} {sname}"

            _m.reactions.extend(
                [
                    # only distribution in plasma volume
                    Reaction(
                        sid=rid_in,
                        name=name_in,
                        formula=(f"Q{cid}*Car_{sid}", U.mmole_per_min),
                        equation=f"Car_{sid} -> C{cid}_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=rid_out,
                        name=name_out,
                        formula=(
                            f"Q{cid}*C{cid}_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} -> Cpo_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )
        # --------------------
        # ar -> li
        # po -> li
        # li -> hv -> ve
        # --------------------
        if cid == "li":
            # liver
            _m.reactions.extend(
                [
                    Reaction(
                        sid=f"Flow_arli_li_{sid}",
                        name=f"arterial inflow liver {sname}",
                        formula=(
                            f"(1 dimensionless - f_shunts)*Qha*Car_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"Car_{sid} -> Cli_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    # shunted arterial flow
                    Reaction(
                        sid=f"Flow_arli_hv_{sid}",
                        name="flow arterial shunts",
                        formula=(f"f_shunts*Qha*Car_{sid}", U.mmole_per_min),
                        equation=f"Car_{sid} -> Chv_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    # (unshunted) portal flow
                    Reaction(
                        sid=f"Flow_po_li_{sid}",
                        name=f"outflow po {sname}",
                        formula=(
                            f"(1 dimensionless - f_shunts)*Qpo*Cpo_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"Cpo_{sid} -> Cli_plasma_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    # portal shunts
                    Reaction(
                        sid=f"Flow_po_hv_{sid}",
                        name="flow portal shunts",
                        formula=(f"f_shunts*Qpo*Cpo_{sid}", U.mmole_per_min),
                        equation=f"Cpo_{sid} -> Chv_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=f"Flow_li_hv_{sid}",
                        name=f"outflow liver {sname}",
                        formula=(
                            f"(1 dimensionless - f_shunts)*(Qpo+Qha)*Cli_plasma_{sid}",
                            U.mmole_per_min,
                        ),
                        equation=f"Cli_plasma_{sid} -> Chv_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                    Reaction(
                        sid=f"Flow_hv_ve_{sid}",
                        name=f"outflow hepatic vein {sname}",
                        formula=(f"Qh*Chv_{sid}", U.mmole_per_min),
                        equation=f"Chv_{sid} -> Cve_{sid}",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
                ]
            )

# --------------------------------------------------------------------------------------------------
# RateRules
# --------------------------------------------------------------------------------------------------
_m.rate_rules = []

for sid, sdict in SUBSTANCES_BODY.items():
    if "PODOSE" in sdict:
        # Dissolution and absorption
        _m.parameters.extend(
            [
                Parameter(
                    f"PODOSE_{sid}",
                    sdict["PODOSE"],
                    U.mg,
                    constant=False,
                    sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                    name=f"oral dose {sid} [mg]",
                ),
            ]
        )
        _m.replaced_elements.extend(
            [
                ReplacedElement(
                    sid=f"PODOSE_{sid}_RE",
                    metaId=f"PODOSE_{sid}_RE",
                    elementRef=f"PODOSE_{sid}",
                    submodelRef=SUBMODEL_SID_DICT["gu"],
                    portRef=f"PODOSE_{sid}{PORT_SUFFIX}",
                )
            ]
        )

    if "IVDOSE" in sdict:
        _m.rate_rules.extend(
            [
                # injection of dose
                RateRule(
                    f"IVDOSE_{sid}", f"-iv_{sid}*Mr_{sid} + Ri_{sid}", U.mg_per_min
                ),
                # cumulative infusion dose
                RateRule(f"cum_dose_{sid}", f"Ri_{sid}", U.mg_per_min),
            ]
        )

model_body_pravastatin: Model = _m


if __name__ == "__main__":
    from pkdb_models.models.pravastatin import MODEL_BASE_PATH

    result = create_model(
        filepath=MODEL_BASE_PATH / f"{model_body_pravastatin.sid}.xml",
        model=model_body_pravastatin,
        sbml_level=3,
        sbml_version=2,
    )
