"""Pravastatin: PBPK model of pravastatin and its effect on the LDL cholesterol.

The paths of the model and its model object `MODEL`, which the commands
`run_simulation`, `run_fit`, `run_report` and `run_identifiability` of pkpdsim
run by its package `pkdb_models.models.pravastatin`.
"""

from pathlib import Path

from pkpdsim.model import FigureSettings, PKPDModel, SimulatorSettings
from pkpdsim.release.settings import Author, ReleaseSettings

from pkdb_models.models.pravastatin.tolerances import ABSOLUTE_TOLERANCE

PRAVASTATIN_PATH = Path(__file__).parent

MODEL_BASE_PATH = PRAVASTATIN_PATH / "models" / "output" / "models"
#: the model of pravastatin
MODEL_PATH = MODEL_BASE_PATH / "pravastatin_body_pravastatin_flat.xml"
#: the model of pravastatin and the cholesterol
MODEL_PATH_CHOLESTEROL = MODEL_BASE_PATH / "pravastatin_body_all_flat.xml"

DATA_PATH_BASE = PRAVASTATIN_PATH / "data"
DATA_PATH_PRAVASTATIN = DATA_PATH_BASE / "pravastatin"
DATA_PATH_SIMVASTATIN = DATA_PATH_BASE / "simvastatin"
DATA_PATHS = [
    DATA_PATH_PRAVASTATIN,
    DATA_PATH_SIMVASTATIN,
]

MODEL = PKPDModel(
    name="pravastatin",
    package=__name__,
    title="Pravastatin PBPK/PD model",
    path=PRAVASTATIN_PATH,
    model_path=MODEL_PATH,
    data_paths=tuple(DATA_PATHS),
    archive_path=MODEL_BASE_PATH.parent / "pravastatin_model.omex",
    factory=".models.factory:create_pravastatin_models",
    experiments=".simulations:EXPERIMENTS",
    fit_definitions=".fitting.fitting:FIT_DEFINITIONS",
    fits=("PK_20261019_164944__7b050",),
    simulator=SimulatorSettings(
        absolute_tolerance=ABSOLUTE_TOLERANCE, relative_tolerance=1e-10
    ),
    figures=FigureSettings(formats=("svg",), fig_dpi=300, legend_fontsize=10),
    fit_identifiability=True,
    # the release of the model repository
    release=ReleaseSettings(
        title="Physiologically based pharmacokinetic (PBPK) model of pravastatin",
        repository="matthiaskoenig/pravastatin-model",
        doi="10.5281/zenodo.6420970",
        authors=(
            Author(
                "König, Matthias",
                "0000-0003-1725-179X",
                (
                    "Humboldt-Universität zu Berlin, Faculty of Life Sciences, Department of Biology, Institute of Theoretical Biology, Systems Medicine of the Liver; University of Stuttgart, Institute of Structural Mechanics and Dynamics in Aerospace Engineering; University of Southern Denmark, Clinical Pharmacology, Pharmacy and Environmental Medicine, Department of Public Health; University Hospital Schleswig-Holstein, Campus Lübeck, First Department of Medicine, Lübeck, Germany"
                ),
            ),
            Author(
                "Leal Pujol, Helen",
                "0000-0003-2919-5668",
                "Humboldt-University Berlin, Institute for Theoretical Biology, Berlin",
            ),
        ),
        keywords=(
            "model",
            "pravastatin",
            "statin",
            "OATP1B1",
            "SLCO1B1",
            "pharmacokinetics",
            "PBPK",
            "physiologically based pharmacokinetic model",
            "SBML",
        ),
        docker_image="matthiaskoenig/pravastatin",
        funding=(
            "Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B)."
        ),
        description=(
            "This repository provides the pravastatin physiologically based"
            " pharmacokinetic (PBPK) model: its oral absorption via OATP2B1, its"
            " hepatic uptake via OATP1B1 (SLCO1B1) and biliary excretion with"
            " the enterohepatic circulation, its renal filtration and tubular"
            " secretion, and the effects of the SLCO1B1 genotypes, renal and"
            " hepatic impairment, food and interacting drugs."
        ),
        first_year=2021,
    ),
)
"""The pravastatin model: its commands, see `pkpdsim.model`."""
