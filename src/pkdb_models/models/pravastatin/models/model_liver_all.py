"""Liver model of pravastatin and cholesterol.

The model has no elements of its own: it is created together with the base
liver model and the pravastatin and cholesterol parts of the liver, which the
factory merges into one model.
"""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import Model, create_model

from pkdb_models.models.pravastatin.models import templates
from pkdb_models.models.pravastatin.models.model_liver_base import U

_m = Model(
    "pravastatin_liver_all",
    name="Model for pravastatin and cholesterol metabolism in the liver",
    notes="""
    # Model for pravastatin and cholesterol metabolism in the liver
    """
    + terms_of_use,
    creators=templates.creators,
    units=U,
    model_units=templates.model_units,
)
model_liver_all = _m

if __name__ == "__main__":
    from pkdb_models.models.pravastatin import MODEL_BASE_PATH
    from pkdb_models.models.pravastatin.models.model_liver_base import model_liver_base
    from pkdb_models.models.pravastatin.models.model_liver_cholesterol import (
        model_liver_cholesterol,
    )
    from pkdb_models.models.pravastatin.models.model_liver_pravastatin import (
        model_liver_pravastatin,
    )

    result = create_model(
        filepath=MODEL_BASE_PATH / f"{model_liver_all.sid}.xml",
        model=[
            model_liver_base,
            model_liver_pravastatin,
            model_liver_cholesterol,
            model_liver_all,
        ],
        sbml_level=3,
        sbml_version=2,
    )

    # create a second model with a constant hepatic cholesterol (boundary
    # condition), by changing the models in place
    model_liver_all.sid = "pravastatin_liver_cholesterol_constant"
    for species in model_liver_cholesterol.species:
        if species.sid == "cho":
            species.boundaryCondition = True

    result_constant = create_model(
        filepath=MODEL_BASE_PATH / f"{model_liver_all.sid}.xml",
        model=[
            model_liver_base,
            model_liver_pravastatin,
            model_liver_cholesterol,
            model_liver_all,
        ],
        sbml_level=3,
        sbml_version=2,
    )
