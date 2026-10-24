"""Pravastatin parameter fitting.

The fit problems of the pravastatin model: which fit mapping collections enter
a fit and which parameters are adjusted, see `FIT_DEFINITIONS`. The commands
`run_fit`, `run_report` and `run_identifiability` of pkpdsim run them with the
package of the model, a fit is followed by the identifiability analysis of its
parameters (`--no-identifiability` skips it):

    run_fit pkdb_models.models.pravastatin --subset=PK --runs=3 --cores=3 --seed=1234 --method=DE

The identifiability analysis is the profile likelihood of every fitted
parameter around the best parameter set and the Fisher information of the same
set, which end up in the identifiability section of the report of the fit.

The results, figures and the HTML report are written into the fit folder of the
model (`MODEL.fit_dir`), unless `--output_dir` is given. The identifiability of
parameters which were fitted earlier is analysed without fitting again with the
`run_identifiability` command, a report of stored parameters is created with
the `run_report` command:

    run_identifiability pkdb_models.models.pravastatin --subset=PK results/fit/PK_<fit id>/parameters.json
    run_report pkdb_models.models.pravastatin --subset=PK results/fit/PK_<fit id>/parameters.json

The model of pravastatin has no pharmacodynamic data: the experiments of the
LDL cholesterol were removed (see TODO.md), so there is no PD subset.
"""

from pkpdsim.fit import default_fit_settings
from sbmlsim.fit.cli import FitDefinition

from pkdb_models.models.pravastatin import DATA_PATHS, PRAVASTATIN_PATH
from pkdb_models.models.pravastatin.fitting.mapping_collections import (
    f_collections_pk,
)
from pkdb_models.models.pravastatin.fitting.parameters import parameters_pk
from pkdb_models.models.pravastatin.tolerances import absolute_tolerance

#: settings of the fits, stored with the result and read back by the report;
#: the species get a tolerance of their own scale, the plasma concentrations
#: of the terminal phase are about 1e-7 mM, see `tolerances`
FIT_SETTINGS = default_fit_settings(
    absolute_tolerance=absolute_tolerance(1e-6, species=1e-10)
)

#: the fit problems of the pravastatin model, the keys are the `--subset` argument
FIT_DEFINITIONS: dict[str, FitDefinition] = {
    # the pharmacokinetics of pravastatin in plasma and urine
    "PK": FitDefinition(
        mapping_collections=f_collections_pk,
        parameters=parameters_pk,
        base_path=PRAVASTATIN_PATH,
        data_path=DATA_PATHS,
        settings=FIT_SETTINGS,
    ),
}
