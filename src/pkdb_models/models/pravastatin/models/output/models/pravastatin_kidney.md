# Model for pravastatin elimination in the kidneys

Model `pravastatin_kidney`, SBML Level 3 Version 2, read from pravastatin\_kidney.xml, written by sbmlode 0.3.0.

Model for pravastatin elimination in the kidneys

Model for the renal excretion of pravastatin by glomerular filtration and tubular secretion (OAT3), relative to the glomerular filtration rate, encoded in SBML format.

The content of this model has been carefully created in a manual research effort.

Terms of use

Copyright © 2026 Matthias König.

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.

Redistribution and use of any part of this model, with or without modification, are permitted provided that the following conditions are met:

Redistributions of this SBML file must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in a different form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

This model is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

## Units

| Time | Substance | Extent | Volume | Area | Length |
| --- | --- | --- | --- | --- | --- |
| min | mmol | mmol | l | m<sup>2</sup> | m |

## Compartments

| Symbol | Id | Name | Size | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{Vext}$ | `Vext` | plasma | $1$ | l | ✓ |
| $\mathrm{Vki}$ | `Vki` | kidney | $0.3$ | l | ✓ |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{pra}_{\mathrm{ext}}$ | `pra_ext` | pravastatin (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{pra}_{\mathrm{urine}}$ | `pra_urine` | pravastatin (urine) | $\mathrm{Vurine}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{renal\_function}}$ | `f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) | $101$ | ml/min | ✓ |
| $\mathrm{fu}_{\mathrm{pra}}$ | `fu_pra` | fraction unbound in plasma pravastatin | $0.5$ | \- | ✓ |
| $\mathrm{PRAEX}_{\mathrm{f}}$ | `PRAEX_f` | renal clearance of unbound pravastatin relative to the GFR | $16.5960789851112$ | \- | ✓ |
| $f_{\mathrm{OAT3}}$ | `f_OAT3` | parameter for OAT3 activity | $1$ | \- | ✓ |
| $\mathrm{GFR}$ | `GFR` | glomerular filtration rate |  | ml/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{pra}_{\mathrm{urine}} &= 0 \cdot \mathrm{Vurine}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{GFR} &= f_{\mathrm{renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{PRAEX}}$ | `PRAEX` | excretion pravastatin | $\mathrm{pra}_{\mathrm{ext}} \longrightarrow \mathrm{pra}_{\mathrm{urine}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{PRAEX}} &= \mathrm{GFR} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{pra}} \cdot \mathopen{}\left(1 + f_{\mathrm{OAT3}} \cdot \mathopen{}\left(\mathrm{PRAEX}_{\mathrm{f}} - 1\right)\right) \cdot \mathrm{pra}_{\mathrm{ext}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{pra}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{PRAEX}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{pra}_{\mathrm{urine}}}{\mathrm{d} t} &= v_{\mathrm{PRAEX}}
\end{aligned}
$$
