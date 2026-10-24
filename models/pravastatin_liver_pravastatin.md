# Model for pravastatin elimination in the liver

Model `pravastatin_liver_pravastatin`, SBML Level 3 Version 2, read from pravastatin\_liver\_pravastatin.xml, written by sbmlode 0.3.0.

Model for pravastatin elimination in the liver

Model for hepatic uptake of pravastatin via OATP1B1 (SLCO1B1) and subsequent excretion in the bile via MRP2 encoded in SBML.

no metabolism of pravastatin

irreversible uptake and excretion of pravastatin via the bile into the intestinal lumen

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
| $\mathrm{Vbaso}$ | `Vbaso` | basolateral membrane | $1$ | m<sup>2</sup> | ✓ |
| $\mathrm{Vli}$ | `Vli` | liver | $1.5$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{pra}$ | `pra` | pravastatin (liver) | $\mathrm{Vli}$ | $0$ | mmol/l | concentration |
| $\mathrm{pra}_{\mathrm{ext}}$ | `pra_ext` | pravastatin (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{pra}_{\mathrm{lumen}}$ | `pra_lumen` | pravastatin (intestinal volume) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{PRAIM}_{\mathrm{Vmax}}$ | `PRAIM_Vmax` | Vmax for pravastatin import via OATP1B1 | $0.00492447459626885$ | mmol/min/l | ✓ |
| $f_{\mathrm{OATP1B1}}$ | `f_OATP1B1` | parameter for OATP1B1 activity | $1$ | \- | ✓ |
| $\mathrm{PRAIM}_{\mathrm{Km\_pra}}$ | `PRAIM_Km_pra` | Km for pravastatin import via OATP1B1 | $0.01$ | mmol/l | ✓ |
| $\mathrm{PRAEX}_{\mathrm{k}}$ | `PRAEX_k` | rate for pravastatin export via MRP2 | $0.1$ | 1/min | ✓ |
| $f_{\mathrm{MRP2}}$ | `f_MRP2` | parameter for MRP2 activity | $1$ | \- | ✓ |

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{PRAIM}}$ | `PRAIM` | pravastatin import (OATP1B1) | $\mathrm{pra}_{\mathrm{ext}} \longrightarrow \mathrm{pra}$ |
| $v_{\mathrm{PRAEX}}$ | `PRAEX` | pravastatin bile export (MRP2) | $\mathrm{pra} \longrightarrow \mathrm{pra}_{\mathrm{lumen}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{PRAIM}} &= \frac{f_{\mathrm{OATP1B1}} \cdot \mathrm{PRAIM}_{\mathrm{Vmax}} \cdot \mathrm{Vli} \cdot \mathrm{pra}_{\mathrm{ext}}}{\mathrm{pra}_{\mathrm{ext}} + \mathrm{PRAIM}_{\mathrm{Km\_pra}}} \\[1ex]
v_{\mathrm{PRAEX}} &= f_{\mathrm{MRP2}} \cdot \mathrm{PRAEX}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{pra}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{pra}}{\mathrm{d} t} &= \frac{v_{\mathrm{PRAIM}} - v_{\mathrm{PRAEX}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{pra}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{PRAIM}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{pra}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{v_{\mathrm{PRAEX}}}{\mathrm{Vlumen}}
\end{aligned}
$$
