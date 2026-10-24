"""Collect the data of the pravastatin studies from the PK-DB study folders.

The studies are copied from a `pkdb_data` checkout (`PKDB_DATA`, else
`../pkdb_data`, see `pkpdsim.data.studies_dir`) into the data folder of the
model, see `pkpdsim.data.collect_tsv_files`.
Besides the pravastatin studies, four simvastatin studies have pravastatin
groups: Jacobson2004, Keskitalo2009, Neuvonen1998 and Sugimoto2001.
"""

from pathlib import Path

from pkpdsim.data import collect_tsv_files
from pkpdsim.data import studies_dir as pkdb_studies_dir

from pkdb_models.models.pravastatin import (
    DATA_PATH_PRAVASTATIN,
    DATA_PATH_SIMVASTATIN,
)

#: the studies of other substances which the pravastatin experiments use
SIMVASTATIN_STUDIES = {"Jacobson2004", "Keskitalo2009", "Neuvonen1998", "Sugimoto2001"}


def collect_data(studies_dir: Path | None = None) -> None:
    """Copy the data of the pravastatin studies into the data folder of the model.

    Args:
        studies_dir: the `studies` folder of pkdb_data, by default the one of
            the checkout `pkpdsim.data.studies_dir` finds.
    """
    if studies_dir is None:
        studies_dir = pkdb_studies_dir()
    DATA_PATH_PRAVASTATIN.parent.mkdir(exist_ok=True)
    collect_tsv_files(
        source_dir=studies_dir / "pravastatin", target_dir=DATA_PATH_PRAVASTATIN
    )
    collect_tsv_files(
        source_dir=studies_dir / "simvastatin",
        target_dir=DATA_PATH_SIMVASTATIN,
        filter_study=lambda study: study in SIMVASTATIN_STUDIES,
    )


if __name__ == "__main__":
    collect_data()
