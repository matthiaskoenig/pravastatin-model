"""Whole-body model of the cholesterol, coupled to the whole-body model of pravastatin.

The plasma LDL and VLDL cholesterol in the circulation of the pravastatin body
model, the whole-body net consumption of LDL cholesterol and the conversion of
VLDL into LDL cholesterol. The liver submodel is the liver of pravastatin and
cholesterol (`pravastatin_liver_all`). The model is merged with the whole-body
model of pravastatin (`pravastatin_body_pravastatin`), whose compartments,
blood flows and parameters it uses.
"""

from copy import deepcopy

import numpy as np
from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    PORT_SUFFIX,
    AssignmentRule,
    ExternalModelDefinition,
    Model,
    Parameter,
    Reaction,
    ReplacedElement,
    Species,
)
from sbmlutils.metadata import BQB, SBO

from pkdb_models.models.pravastatin.models import annotations, templates
from pkdb_models.models.pravastatin.models.model_body_pravastatin import (
    COMPARTMENTS_BODY,
    SUBMODEL_SID_DICT,
    SubstanceBody,
    U,
)

# -----------------------------------------------------------------------------
# Whole Body Metabolism
# -----------------------------------------------------------------------------
_m = Model(
    "pravastatin_body_all",
    name="Cholesterol whole body model for coupling with pravastatin",
    notes="""
    # PK/PD model for whole-body cholesterol metabolism.
    """
    + terms_of_use,
    units=U,
    model_units=templates.model_units,
    creators=templates.creators,
    annotations=[
        (BQB.IS, "taxonomy/9606"),  # Homo sapiens
    ],
)

_m.species = []
_m.reactions = []
_m.ports = []
_m.deletions = []
_m.replaced_elements = []
_m.rate_rules = []

liver_id = "pravastatin_liver_all"

_m.external_model_definitions = [
    ExternalModelDefinition(
        sid="liver",
        name="liver model definition",
        source=f"{liver_id}.xml",
        modelRef=liver_id,
    ),
]

SUBSTANCES_BODY: dict[str, SubstanceBody] = {
    "ldlc": {
        "name": "ldl-cholesterol",
        "unit": U.mmole,
        # initial concentration (! set identical in liver model !)
        "cinit": 3.0,  # [mmole/l] optimal <3.36 [mM], intermediate 3.36-3.11 [mM]; high > 4.11;
        "Mr": 386.654,  # [g/mole] (molecular weight of cholesterol!)
        "fu": 1.0,  # [-] fraction unbound in plasma
        "ftissue": 0.0,  # [litre/min] distribution in tissues (no distribution)
        "annotations": annotations.species["ldlc"],
    },
    "vldlc": {
        "name": "vldl-cholesterol",
        "unit": U.mmole,
        # initial concentration (! set identical in liver model !)
        "cinit": 1.0,  # FIXME
        "Mr": 386.654,  # [g/mole] (molecular weight of cholesterol!)
        "fu": 1.0,  # [-] fraction unbound in plasma
        "ftissue": 0.0,  # [litre/min] distribution in tissues (no distribution)
        "annotations": annotations.species["vldlc"],
    },
}

COMPARTMENTS_BODY = deepcopy(COMPARTMENTS_BODY)
SUBMODEL_SID_DICT = deepcopy(SUBMODEL_SID_DICT)

# -------------------------------------------------------------------------------------------------
# Species
# -------------------------------------------------------------------------------------------------
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
    if ("ftissue" in sdict) and (not np.isclose(sdict["ftissue"], 0.0)):
        for cid, cname in COMPARTMENTS_BODY.items():
            if cid not in ["ve", "ar", "li", "ki", "gu", "po", "hv"]:
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


# replace species
replaced_species = {
    "li": ["vldlc", "ldlc"],
    "ki": [],
    "gu": [],
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


# -------------------------------------------------------------------------------------------------
# Parameters
# -------------------------------------------------------------------------------------------------
_m.parameters.append(
    Parameter(
        "pra_inhibitor_activity",
        1,
        U.dimensionless,
        constant=True,
        name="HMG-CoA Reductase inhibitor activity of pravastatin",
        sboTerm=SBO.INHIBITORY_CONSTANT,
    ),
)

replaced_parameters = {
    "li": ["pra_inhibitor_activity", "Mr_ldlc"],
    "gu": [],
    "ki": [],
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
    if "ftissue" in sdict:
        _m.parameters.append(
            Parameter(
                f"ftissue_{sid}",
                sdict["ftissue"],
                U.l_per_min,
                constant=True,
                sboTerm=SBO.QUANTITATIVE_SYSTEMS_DESCRIPTION_PARAMETER,
                name=f"tissue distribution {sid}",
                notes="Exchange flow at the reference body weight `BW_ref`.",
            )
        )


_m.parameters.extend(
    [
        Parameter(
            "ldlc_init",
            3,
            unit=U.mM,
            name="Initial LDLC -concentration",
            port=True,
            sboTerm=SBO.MOLAL_CONCENTRATION_OF_AN_ENTITY,
        ),
        Parameter(
            "v_cho_ref",
            1000,
            unit=U.mg_per_day,
            name="reference cholesterol turnover [mg/day]",
            port=True,
            sboTerm=SBO.BASAL_RATE_CONSTANT,
        ),
    ]
)


_m.replaced_elements.append(
    ReplacedElement(
        sid="v_cho_ref_li_RE",
        metaId="v_cho_ref_li_RE",
        elementRef="v_cho_ref",
        submodelRef=SUBMODEL_SID_DICT["li"],
        portRef=f"v_cho_ref{PORT_SUFFIX}",
    )
)

# whole-body net change in cholesterol
# FIXME: scale with bodyweight!

_m.parameters.extend(
    [
        # +1.0 [g/day]
        Parameter(
            "ldlc_diet_k",
            1.0,
            unit=U.dimensionless,
            sboTerm=SBO.KINETIC_CONSTANT,
            name="rate of cholesterol uptake from diet",
            notes="""
       +1.0 [g/day] cholesterol uptake diet
       """,
        ),
        # -1.2 [g/day]
        Parameter(
            "ldlc_loss_k",
            1.2,
            unit=U.dimensionless,
            sboTerm=SBO.KINETIC_CONSTANT,
            name="rate of cholesterol loss in feces",
            notes="""
        -1.2 [g/day] loss feces
        """,
        ),
        # -0.8 [g/day]
        Parameter(
            "ldlc_utilization_Vmax",
            0.6521437702939304,
            unit=U.dimensionless,
        ),
        Parameter(
            "ldlc_consumption_Km",
            60,
            unit=U.mmole_per_l,
        ),
        Parameter(
            "f_ldlc_utilization_Vmax",
            1,
            U.dimensionless,
            constant=True,
            name="scaling factor for utilization",
            sboTerm=SBO.MAXIMAL_VELOCITY,
            notes="""
        FH patients are simulated via a different net consumption (i.e. here utilization)
        """,
        ),
        Parameter(
            "vldlc_conversion_k",
            2,
            U.l_per_mmole,
            constant=True,
            name="conversion rate for plasma vldlc into plasma ldlc",
            sboTerm=SBO.KINETIC_CONSTANT,
            notes="""
        """,
        ),
    ]
)

# --------------------------------------------------------------------------------------------------
# Reactions
# --------------------------------------------------------------------------------------------------
for sid, sdict in SUBSTANCES_BODY.items():
    sname = sdict["name"]

    # --------------------
    # tissue distribution
    # --------------------
    if ("ftissue" in sdict) and (not np.isclose(sdict["ftissue"], 0.0)):
        for cid in COMPARTMENTS_BODY:
            if cid not in ["ve", "ar", "li", "gu", "ki", "po", "hv"]:
                _m.reactions.append(
                    Reaction(
                        sid=f"transport_{cid}_{sid}",
                        name=f"transport {sname}",
                        formula=(
                            f"ftissue_{sid} * BW/BW_ref * (C{cid}_plasma_{sid} - C{cid}_{sid})",
                            U.mmole_per_min,
                        ),
                        equation=f"C{cid}_plasma_{sid} <-> C{cid}_{sid}",
                        compartment=f"V{cid}_tissue",
                        sboTerm=SBO.TRANSPORT_REACTION,
                    ),
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

_m.rules.extend(
    [
        AssignmentRule(
            "ldlc_change",
            "(Cve_ldlc - ldlc_init) / ldlc_init",
            U.dimensionless,
            name="relative LDL-C reduction in plasma in [0,-1]",
        ),
        AssignmentRule(
            "v_cho_reference",
            "v_cho_ref / Mr_ldlc / conversion_min_per_day",
            unit=U.mmole_per_min,
            name="reference cholesterol turnover [mmole/min]",
        ),
        AssignmentRule(
            "ldlc_loss",
            "v_cho_reference * ldlc_loss_k",
            U.mmole_per_min,
            name="total loss of cholesterol",
            notes="""
        Baseline loss plus additional ldlc dependent loss
        """,
        ),
        AssignmentRule(
            "ldlc_diet",
            "v_cho_reference * ldlc_diet_k",
            U.mmole_per_min,
            name="total dietary cholesterol",
        ),
        AssignmentRule(
            "ldlc_utilization",
            "v_cho_reference * ldlc_utilization_Vmax * f_ldlc_utilization_Vmax",
            U.mmole_per_min,
            name="total utilized cholesterol",
        ),
    ]
)

_m.reactions.extend(
    [
        Reaction(
            sid="ldlc_net_consumption",
            name="whole-body net consumption of plasma LDL-C",
            equation="Cve_ldlc -> ",
            formula=(
                "(ldlc_utilization + ldlc_loss) * (1 dimensionless + Cve_ldlc/ldlc_consumption_Km) - ldlc_diet",
                U.mmole_per_min,
            ),
            sboTerm=SBO.TRANSLOCATION_REACTION,
        ),
        Reaction(
            sid="vldlc_conversion",
            name="VLDL-C to LDL-C conversion",
            equation="Cve_vldlc -> Cve_ldlc",
            formula=(
                "v_cho_reference * vldlc_conversion_k * Cve_vldlc",
                U.mmole_per_min,
            ),
            sboTerm=SBO.TRANSLOCATION_REACTION,
            notes="""VLDL particles are converted to LDL by loosing triglycerides.
            Assumption is that the cholesterol stays constant in the VLDL to LDL conversion.
            """,
        ),
    ]
)

# Unit conversions
_m.rules.extend(
    [
        AssignmentRule(
            "v_ldlc_net_consumption",
            "ldlc_net_consumption * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma cholesterol net consumption [mg/day]",
        ),
        AssignmentRule(
            "v_vldlc_conversion",
            "vldlc_conversion * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma vldlc conversion into ldlc [mg/day]",
        ),
        AssignmentRule(
            "v_ldlc_utilization",  # if treshold reached more ldlc should be utilized
            "ldlc_utilization * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma cholesterol net consumption [mg/day]",
        ),
        # FIXME: dietary uptake of LDL-C takes place in the intestine
        AssignmentRule(
            "v_ldlc_diet",
            "ldlc_diet * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma cholesterol diet [mg/day]",
        ),
        AssignmentRule(
            "v_ldlc_loss",  # if treshold reached, the loss should be higher
            "ldlc_loss * Mr_ldlc * conversion_min_per_day",
            unit=U.mg_per_day,
            name="plasma cholesterol loss [mg/day]",
        ),
    ]
)

model_body_cholesterol: Model = _m
