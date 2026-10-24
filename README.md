[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6420970.svg)](https://doi.org/10.5281/zenodo.6420970)
[![Release](https://img.shields.io/github/v/release/matthiaskoenig/pravastatin-model)](https://github.com/matthiaskoenig/pravastatin-model/releases)
[![Documentation](https://github.com/matthiaskoenig/pravastatin-model/actions/workflows/docs.yml/badge.svg)](https://matthiaskoenig.github.io/pravastatin-model/)
[![CI](https://github.com/matthiaskoenig/pravastatin-model/actions/workflows/ci.yml/badge.svg)](https://github.com/matthiaskoenig/pravastatin-model/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/docker/v/matthiaskoenig/pravastatin?sort=semver&label=docker)](https://hub.docker.com/r/matthiaskoenig/pravastatin)
[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org)
[![Code license: MIT](https://img.shields.io/badge/code%20license-MIT-blue)](https://opensource.org/license/MIT)
[![Model license: CC BY-SA 4.0](https://img.shields.io/badge/model%20license-CC%20BY--SA%204.0-lightgrey)](https://creativecommons.org/licenses/by-sa/4.0/)

# Physiologically based pharmacokinetic (PBPK) model of pravastatin

This repository provides the pravastatin physiologically based pharmacokinetic (PBPK) model: its oral absorption via OATP2B1, its hepatic uptake via OATP1B1 (SLCO1B1) and biliary excretion with the enterohepatic circulation, its renal filtration and tubular secretion, and the effects of the SLCO1B1 genotypes, renal and hepatic impairment, food and interacting drugs.

Documentation: <https://matthiaskoenig.github.io/pravastatin-model/>

## Quick start

```bash
git clone https://github.com/matthiaskoenig/pravastatin-model.git && cd pravastatin-model
uv sync
uv run run_simulation pkdb_models.models.pravastatin --action all -r results
```

## How to cite

> König, M. & Leal Pujol, H. (2026). *Physiologically based pharmacokinetic (PBPK) model of pravastatin*. Zenodo. https://doi.org/10.5281/zenodo.6420970

## License

* Source Code: [MIT](https://opensource.org/license/MIT)
* Documentation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
* Models: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

&copy; 2021-2026 Matthias König and Helen Leal Pujol
