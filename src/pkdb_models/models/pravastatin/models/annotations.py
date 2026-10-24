"""Annotations of the pravastatin models: the compartments and species."""

# the compartments are the shared ones of all models
from pkpdsim.annotations import compartments as compartments
from sbmlutils.metadata import BQB

species: dict[str, list[tuple[BQB, str]]] = {
    "pra": [
        # pravastatin
        (BQB.IS, "pubchem.compound/54687"),
        (BQB.IS, "chebi/CHEBI:63618"),
        (BQB.IS, "ncit/C62070"),
        (BQB.IS, "inchikey/TUZYXOIXSAXUGO-PZAWKZKUSA-N"),
    ],
    "isopra": [
        # 3'alpha-Isopravastatin (SQ 31906)
        (BQB.IS, "pubchem.compound/157787"),
        (BQB.IS, "inchikey/HIZIJHNJVQOXLO-YMUQFYNDSA-N"),
    ],
    "trihydroxypra": [
        # 3'alpha-5'beta-6'beta-Trihydroxypravastatin (SQ 31945)
        (BQB.IS, "pubchem.compound/76970261"),
        (BQB.IS, "inchikey/VVBBIFAPOZVEDR-RCGTXINMSA-N"),
    ],
    "ldlc": [
        (BQB.IS, "efo/0004195"),
        (BQB.IS, "chebi/CHEBI:47774"),
    ],
    "vldlc": [
        (BQB.IS, "chebi/CHEBI:47773"),
    ],
    "cholesterol": [
        (BQB.IS, "chebi/CHEBI:16113"),
        (BQB.IS, "ncit/C369"),
    ],
    "acoa": [
        (BQB.IS, "chebi/CHEBI:15351"),
    ],
    "hmgcoa": [
        (BQB.IS, "ncit/C129007"),
        (BQB.IS, "chebi/CHEBI:15467"),
    ],
    "hmgcoasynthase": [],
    "hmgcoareductase": [
        (BQB.IS, "ncit/C54701"),
    ],
    "ldlr": [
        (BQB.IS, "ncit/C17074"),
    ],
    "ldlr_membrane": [],
    "ldlr_ldlc": [],
    "ldlr_degraded": [],
}
