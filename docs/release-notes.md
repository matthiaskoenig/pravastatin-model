# Release notes

## Release notes for pravastatin-model 0.9.0

Made from pkdb_models 3a0b49144b with pkpdsim 0.11.0.

The changes since 0.8.2.

### Core libraries

The versions of the core libraries cannot be compared, there is no lock file in the previous release. The release uses:

- pkpdsim 0.11.0
- sbmlsim 0.13.0
- sbmlutils 0.17.0

### Libraries

The versions cannot be compared, there is no lock file in the previous release.

### Data

- Added: `pravastatin/Bard1990`, `pravastatin/Becquemont1999`, `pravastatin/Deng2008`, `pravastatin/Gustavson2005`, `pravastatin/Halstenson1992`, `pravastatin/Hedman2003`, `pravastatin/Ho2007`, `pravastatin/Hunninghake1990a`, `pravastatin/Hunninghake1990b`, `pravastatin/Igel2006`, `pravastatin/Jones1991`, `pravastatin/Kazumi1986`, `pravastatin/Kyrklund2003a`, `pravastatin/Kyrklund2004`, `pravastatin/Mabuchi1987`, `pravastatin/Maeda2006`, `pravastatin/Martin2012`, `pravastatin/Mellies1993`, `pravastatin/Mwinyi2004`, `pravastatin/Nakaya1987`, `pravastatin/Niemi2004`, `pravastatin/Niemi2006`, `pravastatin/Nishizato2003`, `pravastatin/Pan1990`, `pravastatin/Pan1990a`, `pravastatin/Pan1993a`, `pravastatin/Pan2000`, `pravastatin/Raasch1991`, `pravastatin/Reihner1990`, `pravastatin/Saito1988`, `pravastatin/Sigurbjoernsson1998`, `pravastatin/Simons1992`, `pravastatin/Singhvi1990`, `pravastatin/Wu2012`, `simvastatin/Jacobson2004`, `simvastatin/Keskitalo2009`, `simvastatin/Neuvonen1998`, `simvastatin/Sugimoto2001`

### Analysis

#### Models

- `pravastatin_body.xml`: removed
- `pravastatin_body_all.xml`: new, 33 species, 48 reactions, 104 parameters
- `pravastatin_body_all_flat.xml`: new, 44 species, 67 reactions, 166 parameters
- `pravastatin_body_flat.xml`: removed
- `pravastatin_body_pravastatin.xml`: new, 15 species, 18 reactions, 81 parameters
- `pravastatin_body_pravastatin_flat.xml`: new, 17 species, 25 reactions, 103 parameters
- `pravastatin_intestine.xml`: added 1 species, 2 reactions, 12 parameters; removed 2 parameters; changed values `F_pra_abs` 0.95 → 0.217463, `f_OATP2B1` 2 → 1
- `pravastatin_kidney.xml`: added 5 parameters; removed 1 parameter
- `pravastatin_liver.xml`: removed
- `pravastatin_liver_all.xml`: new, 14 species, 14 reactions, 48 parameters
- `pravastatin_liver_cholesterol.xml`: new, 12 species, 12 reactions, 43 parameters
- `pravastatin_liver_pravastatin.xml`: new, 3 species, 2 reactions, 5 parameters

#### Experiments

- Added: `ApplicationExperiment`, `Becquemont1999`, `CirrhosisScan`, `Deng2008`, `FHCalibration`, `GenotypeScan`, `GenotypeScanPKParameters`, `Gustavson2005`, `Halstenson1992`, `Halstenson1992Scan`, `Ho2007`, `Jacobson2004`, `Keskitalo2009`, `Kyrklund2003a`, `Kyrklund2004`, `LDLCUtilizationCalibration`, `Maeda2006`, `Mwinyi2004`, `Neuvonen1998`, `Niemi2004`, `Niemi2004_mpl`, `Niemi2006`, `Nishizato2003`, `Pan1990`, `Pan1990a`, `Pan1993a`, `Pan2000`, `ParametersScan`, `Scan_2d_genotypes_pk_parameters`, `Sigurbjoernsson1998`, `Singhvi1990`, `Sugimoto2001`, `Wu2012`

#### Fits

- `PK`: `PK_20261019_164944__7b050`, no fit record in the previous release

## Release notes for pravastatin-model 0.8.2

We are pleased to release a new version of the pravastatin-model including the 
following changes:

### Features
- fixed naming of EHC rate parameter `PRAEHC_Vmax -> PRAEHC_k`

Your pravastatin-model team

## Release notes for pravastatin-model 0.8.1

We are pleased to release a new version of the pravastatin-model including the 
following changes:

### Features
- bugfix in `f_MRP2` in EHC (affecting MRP2 scan)

Your pravastatin-model team

## Release notes for pravastatin-model 0.8.0

We are pleased to release a new version of the pravastatin-model including the 
following changes:

### Features
- connected isomerization and dilution reactions with stomach pravastatin
- values of parameter fit updated
- minor bugfixes

Your pravastatin-model team

## Release notes for pravastatin-model 0.7.1

We are pleased to release a new version of the pravastatin-model including the 
following changes:

### Features
- fixed typos and links

Your pravastatin-model team

## Release notes for pravastatin-model 0.7.0

We are pleased to release a new version of the pravastatin-model including the 
following changes:

### Features
- initial release of model

Your pravastatin-model team

