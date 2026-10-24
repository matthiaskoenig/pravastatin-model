# Pravastatin

Physiologically based pharmacokinetic (PBPK) model of the HMG-CoA reductase inhibitor pravastatin: its oral absorption (dissolution of the tablet and a fraction absorbed, which OATP2B1 and food change), its distribution into the tissues (with a slow distribution into a deep compartment of the rest of the body, the beta phase after an intravenous dose), its hepatic uptake by OATP1B1 (SLCO1B1) and biliary excretion by MRP2 with the enterohepatic circulation, and its renal excretion, the filtration of the unbound pravastatin and the tubular secretion by OAT3 relative to the GFR. The model describes the effects of the SLCO1B1 genotypes (c.521T>C, *1b, *15), of food, of renal and hepatic impairment and of coadministered drugs which inhibit or induce the transporters (gemfibrozil, rifampicin, quercetin, clarithromycin). A second model couples the hepatic pravastatin to a model of the hepatic cholesterol and the plasma LDL cholesterol; it is not calibrated against the pharmacokinetics yet (`TODO.md`).

The published version of the model is [pravastatin-model](https://github.com/matthiaskoenig/pravastatin-model) ([doi:10.5281/zenodo.6420970](https://doi.org/10.5281/zenodo.6420970)).

## Structure

- `__init__.py`: the paths of the model and its model object `MODEL` with its release metadata and its adopted fits, which the commands below run (pkpdsim).
- `models/`: the tissue models (`model_intestine.py`, `model_liver_pravastatin.py`, `model_kidney.py`, and the cholesterol of the liver in `model_liver_cholesterol.py`, `model_liver_all.py`) and the whole-body models (`model_body_pravastatin.py`, `model_body_cholesterol.py`). `models/factory.py` creates the SBML models, the flattened whole-body models which are simulated (`pravastatin_body_pravastatin_flat.xml`, with the cholesterol `pravastatin_body_all_flat.xml`), the ODEs and the COMBINE archive in `models/output/`; the fitted values come from the adopted fits (`models/fits.py`, `models/output/fits/`).
- `experiments/`: the simulation experiments of the clinical studies (`studies/`, doses of pravastatin sodium), the calibration of the cholesterol model (`model_calibration/`) and the scans of hepatic and renal function, of the transporters and of the genotypes (`scans/`). The fit mappings are described with the vocabulary of `pkpdsim.metadata`; the activities of the SLCO1B1 alleles and the factors of the interactions are in `experiments/base_experiment.py`.
- `fitting/`: the fit problem of the pharmacokinetics (`PK`), its parameters and the selection of the training data and of the validation data by question (interactions, doses, populations, limitations).
- `sensitivity/`: the sensitivity analysis of the pharmacokinetics.
- `pravastatin_pk.py`: the pharmacokinetic parameters of the scans, the non-compartmental analysis of `pkpdutils` with the urinary excretion and the renal clearance.
- `tolerances.py`: the absolute tolerances of the integrator per state.
- `simulations.py`: the simulation experiments and their groups, `MODEL` runs them.
- `data/`: the data of the studies, a subset of the PK-DB studies of pravastatin and simvastatin.
- `TODO.md`: the open issues of the model.

## Commands

```bash
# models, simulations
run_simulation pkdb_models.models.pravastatin --action factory
run_simulation pkdb_models.models.pravastatin --action list_experiments
run_simulation pkdb_models.models.pravastatin --action simulate --experiments all
run_simulation pkdb_models.models.pravastatin --action simulate --experiments all --uncertainty

# fits, adoption of a fit, reports of stored parameters, identifiability
run_fit pkdb_models.models.pravastatin --subset=PK --runs=3 --cores=3 --method=DE
run_fit pkdb_models.models.pravastatin --adopt PK_<fit id>
run_report pkdb_models.models.pravastatin --subset=PK results/fit/PK_<fit id>/parameters.json
run_identifiability pkdb_models.models.pravastatin --subset=PK results/fit/PK_<fit id>/parameters.json

# sensitivity analysis (local by default)
python -m pkdb_models.models.pravastatin.sensitivity.sensitivity_analysis
```

The results are written into `results/` of the model.

## Adopted fits and uncertainty

The values of the fitted parameters come from the adopted fit of the model
(`PK_20261019_164944__7b050`), not from numbers in the code.
`run_fit pkdb_models.models.pravastatin --adopt <fit id>` copies the record of
a finished fit (its parameters, problem, profile likelihood and Fisher
information) into `models/output/fits/<fit id>/`, which is tracked; the ids of
the adopted fits are listed in `fits` of the model object (`__init__.py`). The
factory takes the fitted values and their uncertainty from the records
(`models/fits.py`) and writes the uncertainty into the SBML
(`distrib:uncertainty`). `run_simulation ... --uncertainty` runs the
experiments over draws of these distributions and draws the simulations as the
median with a band of quantiles into `results/simulation_uncertainty`; the
experiments of the cholesterol give no pravastatin and run once. A refit is:
fit, adopt, replace the id in `fits`, rebuild the model. See the documentation
of the repository on fitting (`docs/fitting.md`).
