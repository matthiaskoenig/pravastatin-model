# Model for pravastatin elimination in the small intestine

Model `pravastatin_intestine`, SBML Level 3 Version 2, read from pravastatin\_intestine.xml, written by sbmlode 0.3.0.

Model for pravastatin transport from the small intestine into the liver

Model for enterohepatic uptake of pravastatin via OATP2B1 (SLCO2B1)

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
| $\mathrm{Vgu}$ | `Vgu` | intestine | $1.2825$ | l | ✓ |
| $\mathrm{Vlumen}$ | `Vlumen` | intestinal lumen (inner part of intestine) | $1.15425$ | l |  |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vstomach}$ | `Vstomach` | stomach | $1$ | l | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{pra}_{\mathrm{stomach}}$ | `pra_stomach` | pravastatin (stomach) | $\mathrm{Vstomach}$ |  | mmol | amount, boundary |
| $\mathrm{pra}_{\mathrm{lumen}}$ | `pra_lumen` | pravastatin (intestinal volume) | $\mathrm{Vlumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{pra}_{\mathrm{ext}}$ | `pra_ext` | pravastatin (plasma) | $\mathrm{Vext}$ | $0$ | mmol/l | concentration |
| $\mathrm{pra}_{\mathrm{feces}}$ | `pra_feces` | pravastatin (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $F_{\mathrm{pra\_abs}}$ | `F_pra_abs` | fraction absorbed pravastatin (fasted) | $0.217463051507184$ | \- | ✓ |
| $\mathrm{PRAABS}_{\mathrm{k}}$ | `PRAABS_k` | rate of pravastatin leaving the intestinal lumen | $0.0219368198080403$ | 1/min | ✓ |
| $f_{\mathrm{OATP2B1}}$ | `f_OATP2B1` | parameter for OATP2B1 activity | $1$ | \- | ✓ |
| $\mathrm{fed}$ | `fed` | fed state (0 fasted, 1 fed) | $0$ | \- | ✓ |
| $\mathrm{FED}_{\mathrm{f\_absorption}}$ | `FED_f_absorption` | fed effect on the fraction absorbed | $0.75$ | \- | ✓ |
| $\mathrm{FED}_{\mathrm{f\_dissolution}}$ | `FED_f_dissolution` | fed effect on the dissolution and gastric emptying | $0.4$ | \- | ✓ |
| $\mathrm{PODOSE}_{\mathrm{pra}}$ | `PODOSE_pra` | oral dose pravastatin \[mg\] | $0$ | mg |  |
| $\mathrm{POSTOMACH}_{\mathrm{pra}}$ | `POSTOMACH_pra` | oral dose in stomach pravastatin \[mg\] | $0$ | mg |  |
| $\mathrm{Ka}_{\mathrm{application\_pra}}$ | `Ka_application_pra` | Ka \[1/hr\] application pravastatin | $1000$ | 1/hr | ✓ |
| $\mathrm{Ka}_{\mathrm{dis\_pra}}$ | `Ka_dis_pra` | Ka\_dis \[1/hr\] dissolution pravastatin | $2.01072783691315$ | 1/hr | ✓ |
| $\mathrm{Mr}_{\mathrm{pra}}$ | `Mr_pra` | Molecular weight pravastatin \[g/mole\] | $424.53$ | g/mol | ✓ |
| $f_{\mathrm{absorption}}$ | `f_absorption` | factor of the fraction absorbed |  | \- |  |
| $f_{\mathrm{dissolution}}$ | `f_dissolution` | factor of the dissolution and gastric emptying |  | \- |  |
| $F_{\mathrm{absorbed}}$ | `F_absorbed` | fraction absorbed |  | \- |  |
| $\mathrm{absorption}$ | `absorption` | pravastatin leaving the lumen |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{pra}_{\mathrm{stomach}} &= 0 \cdot \mathrm{Vstomach} \\[1ex]
\mathrm{pra}_{\mathrm{feces}} &= 0 \cdot \mathrm{Vfeces}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
f_{\mathrm{absorption}} &= 1 + \mathrm{fed} \cdot \mathopen{}\left(\mathrm{FED}_{\mathrm{f\_absorption}} - 1\right) \\[1ex]
f_{\mathrm{dissolution}} &= 1 + \mathrm{fed} \cdot \mathopen{}\left(\mathrm{FED}_{\mathrm{f\_dissolution}} - 1\right) \\[1ex]
F_{\mathrm{absorbed}} &= F_{\mathrm{pra\_abs}} \cdot f_{\mathrm{OATP2B1}} \cdot f_{\mathrm{absorption}} \\[1ex]
\mathrm{absorption} &= \mathrm{PRAABS}_{\mathrm{k}} \cdot \mathrm{Vlumen} \cdot \mathrm{pra}_{\mathrm{lumen}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation |
| --- | --- | --- | --- |
| $v_{\mathrm{PRAABS}}$ | `PRAABS` | absorption pravastatin (OATP2B1) | $\mathrm{pra}_{\mathrm{lumen}} \longrightarrow \mathrm{pra}_{\mathrm{ext}}$ |
| $v_{\mathrm{PRAEXC}}$ | `PRAEXC` | excretion pravastatin (feces) | $\mathrm{pra}_{\mathrm{lumen}} \longrightarrow \mathrm{pra}_{\mathrm{feces}}$ |
| $v_{\mathrm{application\_pra}}$ | `application_pra` | PO application pravastatin | $\varnothing \longrightarrow \mathrm{pra}_{\mathrm{stomach}}$ |
| $v_{\mathrm{dissolution\_pra}}$ | `dissolution_pra` | dissolution pravastatin | $\mathrm{pra}_{\mathrm{stomach}} \longrightarrow \mathrm{pra}_{\mathrm{lumen}}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{PRAABS}} &= F_{\mathrm{absorbed}} \cdot \mathrm{absorption} \\[1ex]
v_{\mathrm{PRAEXC}} &= \mathopen{}\left(1 - F_{\mathrm{absorbed}}\right) \cdot \mathrm{absorption} \\[1ex]
v_{\mathrm{application\_pra}} &= \frac{\frac{\mathrm{Ka}_{\mathrm{application\_pra}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{pra}}}{\mathrm{Mr}_{\mathrm{pra}}} \\[1ex]
v_{\mathrm{dissolution\_pra}} &= \frac{\frac{f_{\mathrm{dissolution}} \cdot \mathrm{Ka}_{\mathrm{dis\_pra}}}{60} \cdot \mathrm{POSTOMACH}_{\mathrm{pra}}}{\mathrm{Mr}_{\mathrm{pra}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{pra}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{PRAABS}} - v_{\mathrm{PRAEXC}} + v_{\mathrm{dissolution\_pra}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{pra}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{PRAABS}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{pra}_{\mathrm{feces}}}{\mathrm{d} t} &= v_{\mathrm{PRAEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{pra}}}{\mathrm{d} t} &= -v_{\mathrm{application\_pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{POSTOMACH}_{\mathrm{pra}}}{\mathrm{d} t} &= \mathopen{}\left(v_{\mathrm{application\_pra}} - v_{\mathrm{dissolution\_pra}}\right) \cdot \mathrm{Mr}_{\mathrm{pra}} \qquad \text{(rate rule)}
\end{aligned}
$$
