[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6420970.svg)](https://doi.org/10.5281/zenodo.6420970)

# pravastatin model
This repository provides the pravastatin physiologically based pharmacokinetic (PBPK) model:
its oral absorption via OATP2B1, its hepatic uptake via OATP1B1 (SLCO1B1) and biliary excretion
with the enterohepatic circulation, its renal filtration and tubular secretion relative to the GFR,
and the effects of the SLCO1B1 genotypes, renal and hepatic impairment, food and interacting drugs.
The fitted parameters carry their uncertainty from the adopted fit (`fits/`).

The model is distributed as [SBML](http://sbml.org) format available from [`pravastatin_body_pravastatin_flat.xml`](./models/pravastatin_body_pravastatin_flat.xml) with
corresponding [SBML4humans model report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fpravastatin-model%2Fmain%2Fmodels%2Fpravastatin_body_pravastatin_flat.xml) and [model equations](./models/pravastatin_body_pravastatin_flat.md).

The COMBINE archive is available from [`pravastatin_model.omex`](./pravastatin_model.omex).

The model of pravastatin and the LDL cholesterol (`pravastatin_body_all_flat.xml`) couples the
hepatic pravastatin to the HMG-CoA reductase of a model of the hepatic cholesterol; it is not
calibrated to data yet.

### Comp submodels
* **liver** submodel [`pravastatin_liver_pravastatin.xml`](./models/pravastatin_liver_pravastatin.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fpravastatin-model%2Fmain%2Fmodels%2Fpravastatin_liver_pravastatin.xml) and [equations](./models/pravastatin_liver_pravastatin.md).
* **kidney** submodel [`pravastatin_kidney.xml`](./models/pravastatin_kidney.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fpravastatin-model%2Fmain%2Fmodels%2Fpravastatin_kidney.xml) and [equations](./models/pravastatin_kidney.md).
* **intestine** submodel [`pravastatin_intestine.xml`](./models/pravastatin_intestine.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fpravastatin-model%2Fmain%2Fmodels%2Fpravastatin_intestine.xml) and [equations](./models/pravastatin_intestine.md).
* **whole-body** submodel [`pravastatin_body_pravastatin.xml`](./models/pravastatin_body_pravastatin.xml) with [SBML4humans report](https://sbml4humans.de/report?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthiaskoenig%2Fpravastatin-model%2Fmain%2Fmodels%2Fpravastatin_body_pravastatin.xml) and [equations](./models/pravastatin_body_pravastatin.md).

## How to cite
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6420970.svg)](https://doi.org/10.5281/zenodo.6420970)

> König, M. & Leal Pujol, H. (2026).
> *Physiologically based pharmacokinetic (PBPK) model of pravastatin.*
> Zenodo. [https://doi.org/10.5281/zenodo.6420970](https://doi.org/10.5281/zenodo.6420970)

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.

## Run simulations
Clone the repository and run the complete analysis with uv (https://docs.astral.sh/uv/getting-started/installation/):
```bash
git clone https://github.com/matthiaskoenig/pravastatin-model.git
cd pravastatin-model
uv run run_simulation pkdb_models.models.pravastatin -a all -r results
```

## Funding
Matthias König was supported by the Federal Ministry of Research, Technology and Space (BMFTR, Germany) within ATLAS by grant number 031L0304B and by the German Research Foundation (DFG) within the Research Unit Program FOR 5151 QuaLiPerF (Quantifying Liver Perfusion-Function Relationship in Complex Resection - A Systems Medicine Approach) by grant number 436883643 and by grant number 465194077 (Priority Programme SPP 2311, Subproject SimLivA). This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B).

© 2021-2026 Matthias König
