"""The simulation experiments of the pravastatin model and their groups.

They are the registry of `MODEL`, the experiments its commands simulate.
"""

from sbmlsim.experiment import SimulationExperiment

from pkdb_models.models.pravastatin import MODEL
from pkdb_models.models.pravastatin.experiments.model_calibration import (
    FHCalibration,
    LDLCUtilizationCalibration,
)
from pkdb_models.models.pravastatin.experiments.scans import (
    CirrhosisScan,
    GenotypeScan,
    GenotypeScanPKParameters,
    Halstenson1992Scan,
    ParametersScan,
    Scan_2d_genotypes_pk_parameters,
)
from pkdb_models.models.pravastatin.experiments.studies import (
    ApplicationExperiment,
    Becquemont1999,
    Deng2008,
    Gustavson2005,
    Halstenson1992,
    Ho2007,
    Jacobson2004,
    Keskitalo2009,
    Kyrklund2003a,
    Kyrklund2004,
    Maeda2006,
    Mwinyi2004,
    Neuvonen1998,
    Niemi2004,
    Niemi2004_mpl,
    Niemi2006,
    Nishizato2003,
    Pan1990,
    Pan1990a,
    Pan1993a,
    Pan2000,
    Sigurbjoernsson1998,
    Singhvi1990,
    Sugimoto2001,
    Wu2012,
)

EXPERIMENTS: dict[str, list[type[SimulationExperiment]]] = {
    # the pharmacokinetic studies of pravastatin
    "studies": [
        Becquemont1999,
        Deng2008,
        Gustavson2005,
        Halstenson1992,
        Ho2007,
        Jacobson2004,
        Keskitalo2009,
        Kyrklund2003a,
        Kyrklund2004,
        Maeda2006,
        Mwinyi2004,
        Neuvonen1998,
        Niemi2004,
        Niemi2006,
        Nishizato2003,
        Pan1990,
        Pan1990a,
        Pan1993a,
        Pan2000,
        Sigurbjoernsson1998,
        Singhvi1990,
        Sugimoto2001,
        Wu2012,
    ],
    "single_dose": [
        Becquemont1999,
        Deng2008,
        Halstenson1992,
        Ho2007,
        Jacobson2004,
        Keskitalo2009,
        Kyrklund2003a,
        Kyrklund2004,
        Maeda2006,
        Mwinyi2004,
        Neuvonen1998,
        Niemi2004,
        Niemi2006,
        Nishizato2003,
        Pan1993a,
        Pan2000,
        Sigurbjoernsson1998,
        Singhvi1990,
        Sugimoto2001,
        Wu2012,
    ],
    "multiple_dose": [
        Gustavson2005,
        Jacobson2004,
        Pan1990,
        Pan1990a,
    ],
    # the genotypes of SLCO1B1 (OATP1B1), ABCG2 (BCRP) and ABCC2 (MRP2)
    "genotypes": [
        Deng2008,
        Ho2007,
        Keskitalo2009,
        Maeda2006,
        Mwinyi2004,
        Niemi2004,
        Niemi2006,
        Nishizato2003,
    ],
    # the calibration of the familial hypercholesterolemia (FH) types and of the
    # LDL cholesterol utilization in the model of pravastatin and cholesterol
    "calibration": [
        LDLCUtilizationCalibration,
        FHCalibration,
    ],
    "misc": [
        ApplicationExperiment,
        Niemi2004_mpl,
    ],
    "scans": [
        CirrhosisScan,
        ParametersScan,
        Halstenson1992Scan,
        GenotypeScan,
        GenotypeScanPKParameters,
        Scan_2d_genotypes_pk_parameters,
    ],
}
EXPERIMENTS["all"] = (
    EXPERIMENTS["studies"]
    + EXPERIMENTS["calibration"]
    + EXPERIMENTS["misc"]
    + EXPERIMENTS["scans"]
)


if __name__ == "__main__":
    MODEL.run_simulation_experiments(EXPERIMENTS["all"], MODEL.simulation_dir / "all")
