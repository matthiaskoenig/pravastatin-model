"""Pravastatin model factory.

Creates the pravastatin model (`pravastatin_body_pravastatin`) and the model of
pravastatin and cholesterol (`pravastatin_body_all`), each with its tissue
models and its flattened whole-body model.
"""

from copy import deepcopy
from pathlib import Path
from typing import Any

from pkpdsim.licenses import License, write_license
from pymetadata.omex import EntryFormat, ManifestEntry, Omex
from sbmlode import OdeSystem
from sbmlutils.comp import flatten_sbml
from sbmlutils.factory import Model, create_model

from pkdb_models.models.pravastatin import MODEL_BASE_PATH
from pkdb_models.models.pravastatin.models.model_body_cholesterol import (
    model_body_cholesterol,
)
from pkdb_models.models.pravastatin.models.model_body_pravastatin import (
    model_body_pravastatin,
)
from pkdb_models.models.pravastatin.models.model_intestine import model_intestine
from pkdb_models.models.pravastatin.models.model_kidney import model_kidney
from pkdb_models.models.pravastatin.models.model_liver_all import model_liver_all
from pkdb_models.models.pravastatin.models.model_liver_base import model_liver_base
from pkdb_models.models.pravastatin.models.model_liver_cholesterol import (
    model_liver_cholesterol,
)
from pkdb_models.models.pravastatin.models.model_liver_pravastatin import (
    model_liver_pravastatin,
)


def _body_pravastatin_all() -> Model:
    """Body model of pravastatin whose liver is the liver of pravastatin and cholesterol.

    The liver model definition of the pravastatin body model is removed, so that
    the liver model definition of the cholesterol body model
    (`pravastatin_liver_all`) is the one of the merged model.
    """
    model = deepcopy(model_body_pravastatin)
    model.external_model_definitions = [
        emd for emd in model.external_model_definitions if emd.sid != "liver"
    ]
    return model


def _add_odes(results: dict[str, dict[str, Any]], sbml_path: Path) -> None:
    """Write the differential equations of a model as markdown and add them to the results."""
    md_path = sbml_path.parent / f"{sbml_path.stem}.md"
    OdeSystem.from_sbml(sbml_path).write(md_path)
    results[f"{sbml_path.stem}_md"] = {
        "path": md_path,
        "entry": ManifestEntry(
            location=f"./models/{md_path.name}",
            format=EntryFormat.MARKDOWN,
            master=False,
        ),
    }


def create_pravastatin_models(model_output_dir: Path) -> dict[str, dict[str, Any]]:
    """Create the tissue models and the whole-body models of pravastatin.

    The differential equations of every model are written as markdown, the
    flattened model of pravastatin is the master of the COMBINE archive.

    Args:
        model_output_dir: directory of the models, the COMBINE archive and the
            license texts are written into its parent.

    Returns:
        The files of the models with their entries in the COMBINE archive.
    """
    output_dir = model_output_dir
    model_output_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict[str, Any]] = {
        "README": {
            "path": MODEL_BASE_PATH.parent / "README.md",
            "entry": ManifestEntry(
                location="./README.md",
                format=EntryFormat.MARKDOWN,
                master=False,
            ),
        },
        "cc-by": {
            "path": write_license(model_output_dir.parent, License.CC_BY_SA_4_0),
            "entry": ManifestEntry(
                location="./cc-by-sa-4.0.txt",
                format=EntryFormat.TXT,
                master=False,
            ),
        },
        "mit": {
            "path": write_license(
                model_output_dir.parent,
                License.MIT,
                copyright="2021-2026 Matthias König",
            ),
            "entry": ManifestEntry(
                location="./mit.txt",
                format=EntryFormat.TXT,
                master=False,
            ),
        },
    }
    for models in [
        (model_intestine,),
        (model_kidney,),
        # liver of pravastatin
        (model_liver_base, model_liver_pravastatin),
        # liver of cholesterol
        (model_liver_base, model_liver_cholesterol),
        # liver of pravastatin and cholesterol
        (
            model_liver_base,
            model_liver_pravastatin,
            model_liver_cholesterol,
            model_liver_all,
        ),
        # body of pravastatin
        (model_body_pravastatin,),
        # body of pravastatin and cholesterol
        (_body_pravastatin_all(), model_body_cholesterol),
    ]:
        # the models are merged into the last one
        model_sid = models[-1].sid
        factory_results = create_model(
            filepath=output_dir / f"{model_sid}.xml",
            model=models,
            sbml_level=3,
            sbml_version=2,
        )
        sbml_path = factory_results.sbml_path
        results[model_sid] = {
            "path": sbml_path,
            "entry": ManifestEntry(
                location=f"./models/{sbml_path.name}",
                format=EntryFormat.SBML_L3V2,
                master=False,
            ),
        }
        _add_odes(results, sbml_path)

    # create the flat whole-body models
    for key in ["pravastatin_body_pravastatin", "pravastatin_body_all"]:
        sbml_path = results[key]["path"]
        sbml_path_flat = output_dir / f"{sbml_path.stem}_flat.xml"
        flatten_sbml(sbml_path, sbml_flat_path=sbml_path_flat)

        results[f"{key}_flat"] = {
            "path": sbml_path_flat,
            "entry": ManifestEntry(
                location=f"./models/{sbml_path_flat.name}",
                format=EntryFormat.SBML_L3V2,
                master=(key == "pravastatin_body_pravastatin"),
            ),
        }
        _add_odes(results, sbml_path_flat)

    # create omex
    omex = Omex()
    for info in results.values():
        omex.add_entry(entry_path=info["path"], entry=info["entry"])
    omex.to_omex(omex_path=output_dir.parent / "pravastatin_model.omex")

    return results


if __name__ == "__main__":
    # create the models
    create_pravastatin_models(MODEL_BASE_PATH)
