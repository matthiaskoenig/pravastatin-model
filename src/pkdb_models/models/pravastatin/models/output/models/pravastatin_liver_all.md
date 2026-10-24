# Model for pravastatin and cholesterol metabolism in the liver

Model `pravastatin_liver_all`, SBML Level 3 Version 2, read from pravastatin\_liver\_all.xml, written by sbmlode 0.3.0.

Model for pravastatin and cholesterol metabolism in the liver

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
| $\mathrm{ldlc}_{\mathrm{ext}}$ | `ldlc_ext` | ldl-cholesterol (plasma) | $\mathrm{Vext}$ | $3$ | mmol/l | concentration, boundary |
| $\mathrm{vldlc}_{\mathrm{ext}}$ | `vldlc_ext` | vldl-cholesterol (plasma) | $\mathrm{Vext}$ | $1$ | mmol/l | concentration |
| $\mathrm{acoa}$ | `acoa` | acetyl-CoA (liver) | $\mathrm{Vli}$ | $0.043$ | mmol/l | concentration, boundary |
| $\mathrm{hmgcoa}$ | `hmgcoa` | HMG-CoA (liver) | $\mathrm{Vli}$ | $0.022$ | mmol/l | concentration |
| $\mathrm{cho}$ | `cho` | cholesterol (liver) | $\mathrm{Vli}$ | $0.02$ | mmol/l | concentration |
| $\mathrm{hmgcoareductase}$ | `hmgcoareductase` | HMG-CoA reductase (liver) | $\mathrm{Vli}$ |  | \- | amount |
| $\mathrm{hmgcoasynthase}$ | `hmgcoasynthase` | HMG-CoA synthase (liver) | $\mathrm{Vli}$ |  | \- | amount |
| $\mathrm{ldlr}$ | `ldlr` | LDLR | $\mathrm{Vli}$ |  | \- | amount |
| $\mathrm{ldlr}_{\mathrm{membrane}}$ | `ldlr_membrane` | LDLR membrane | $\mathrm{Vbaso}$ |  | \- | amount |
| $\mathrm{ldlr}_{\mathrm{ldlc}}$ | `ldlr_ldlc` | LDLR-LDLC complex | $\mathrm{Vli}$ |  | \- | amount |
| $\mathrm{ldlr}_{\mathrm{degraded}}$ | `ldlr_degraded` | LDLR degraded | $\mathrm{Vli}$ |  | \- | amount |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $\mathrm{cf}_{\mathrm{units\_per\_mmole}}$ | `cf_units_per_mmole` | conversion factor for dimensionless species | $1$ | 1/mmol | ✓ |
| $\mathrm{conversion}_{\mathrm{min\_per\_day}}$ | `conversion_min_per_day` | conversion factor min to hours | $1440$ | min/day | ✓ |
| $\mathrm{pra}_{\mathrm{inhibitor\_activity}}$ | `pra_inhibitor_activity` | Inhibitor activity of pravastatin | $1$ | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{ldlc}}$ | `Mr_ldlc` | Molecular weight cho \[g/mole\] | $386.654$ | g/mol | ✓ |
| $v_{\mathrm{cho\_ref}}$ | `v_cho_ref` | reference cholesterol turnover \[mg/day\] | $1000$ | mg/day | ✓ |
| $\mathrm{SYNTHESIS}_{\mathrm{HMG\_Vmax}}$ | `SYNTHESIS_HMG_Vmax` | Protein synthesis Vmax for HMGR and HMGS | $0.001$ | mmol/min/l | ✓ |
| $\mathrm{DEGRADATION}_{\mathrm{HMG\_Vmax}}$ | `DEGRADATION_HMG_Vmax` | Protein degradation Vmax for HMGR and HMGS | $0.0003$ | mmol/min/l | ✓ |
| $\mathrm{HMG}_{\mathrm{kr\_cho}}$ | `HMG_kr_cho` | Protein regulation kr for HMGR and HMGS | $0.02$ | mmol/l | ✓ |
| $\mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax}}$ | `DEGRADATION_LDLR_Vmax` | Protein degradation Vmax for LDLR | $0.0006$ | mmol/min/l | ✓ |
| $\mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax}}$ | `SYNTHESIS_LDLR_Vmax` | Protein synthesis Vmax for LDLR |  | mmol/min/l |  |
| $\mathrm{LDLR}_{\mathrm{kr\_cho}}$ | `LDLR_kr_cho` | Protein regulation kr for LDLR | $0.02$ | mmol/l | ✓ |
| $\mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax\_f}}$ | `SYNTHESIS_LDLR_Vmax_f` | scaling factor for synthesis Vmax for LDL-R | $1$ | \- | ✓ |
| $\mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax\_f}}$ | `DEGRADATION_LDLR_Vmax_f` | scaling factor for degradation Vmax for LDL-R | $1$ | \- | ✓ |
| $\mathrm{PRAIM}_{\mathrm{Vmax}}$ | `PRAIM_Vmax` | Vmax for pravastatin import via OATP1B1 | $0.00492447459626885$ | mmol/min/l | ✓ |
| $f_{\mathrm{OATP1B1}}$ | `f_OATP1B1` | parameter for OATP1B1 activity | $1$ | \- | ✓ |
| $\mathrm{PRAIM}_{\mathrm{Km\_pra}}$ | `PRAIM_Km_pra` | Km for pravastatin import via OATP1B1 | $0.01$ | mmol/l | ✓ |
| $\mathrm{PRAEX}_{\mathrm{k}}$ | `PRAEX_k` | rate for pravastatin export via MRP2 | $0.1$ | 1/min | ✓ |
| $f_{\mathrm{MRP2}}$ | `f_MRP2` | parameter for MRP2 activity | $1$ | \- | ✓ |
| $\mathrm{VLDLCEXP}_{\mathrm{Vmax}}$ | `VLDLCEXP_Vmax` | Vmax VLDL-cholesterol export | $2.5$ | \- | ✓ |
| $\mathrm{VLDLCEXP}_{\mathrm{Km\_cho}}$ | `VLDLCEXP_Km_cho` | Km VLDL-cholesterol export | $0.0005$ | mmol/l | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Kcat}}$ | `LDLRLDLCIMP_Kcat` |  | $6$ | \- | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Km}}$ | `LDLRLDLCIMP_Km` | Km LDLR-LDLC binding | $3$ | mmol/l | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Ki\_ldlr\_ldlc}}$ | `LDLRLDLCIMP_Ki_ldlr_ldlc` | Ki LDLR-LDLC complex on uptake | $0.1$ | \- | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Km\_f}}$ | `LDLRLDLCIMP_Km_f` |  | $1$ | \- | ✓ |
| $\mathrm{LDLRLDLCIMP}_{\mathrm{Kcat\_f}}$ | `LDLRLDLCIMP_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LDLRMEMBRANE}_{\mathrm{Kcat}}$ | `LDLRMEMBRANE_Kcat` |  | $0.025$ | mmol/min/l | ✓ |
| $\mathrm{LDLRMEMBRANE}_{\mathrm{Kcat\_f}}$ | `LDLRMEMBRANE_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LDLRMEMBRANE}_{\mathrm{Keq}}$ | `LDLRMEMBRANE_Keq` |  | $10$ | \- | ✓ |
| $\mathrm{LDLRRECYCLING}_{\mathrm{Kcat}}$ | `LDLRRECYCLING_Kcat` |  | $0.0125$ | mmol/min/l | ✓ |
| $\mathrm{LDLRRECYCLING}_{\mathrm{Kcat\_f}}$ | `LDLRRECYCLING_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{HMGCOASYNTHASE}_{\mathrm{Kcat}}$ | `HMGCOASYNTHASE_Kcat` |  | $245$ | l/mmol | ✓ |
| $\mathrm{HMGCOASYNTHASE}_{\mathrm{Ki\_hmgcoa}}$ | `HMGCOASYNTHASE_Ki_hmgcoa` |  | $0.022$ | mmol/l | ✓ |
| $\mathrm{HMGCOAREDUCTASE}_{\mathrm{Kcat}}$ | `HMGCOAREDUCTASE_Kcat` |  | $0.7$ | \- | ✓ |
| $\mathrm{HMGCOAREDUCTASE}_{\mathrm{Km}}$ | `HMGCOAREDUCTASE_Km` | Km HMG-CoA | $0.004$ | mmol/l | ✓ |
| $\mathrm{HMGCOAREDUCTASE}_{\mathrm{Ki\_pra}}$ | `HMGCOAREDUCTASE_Ki_pra` | Ki HMG-CoA for pravastatin | $2.3 \times 10^{-6}$ | mmol/l | ✓ |
| $\mathrm{ldlr}_{\mathrm{total}}$ | `ldlr_total` | Total LDLR |  | \- |  |
| $\mathrm{ldlr}_{\mathrm{fraction}}$ | `ldlr_fraction` | LDLR fraction |  | \- |  |
| $\mathrm{ldlr}_{\mathrm{membrane\_fraction}}$ | `ldlr_membrane_fraction` | LDLR membrane fraction |  | \- |  |
| $\mathrm{ldlr}_{\mathrm{ldlc\_fraction}}$ | `ldlr_ldlc_fraction` | LDLR-LDLC fraction |  | \- |  |
| $v_{\mathrm{cho\_reference}}$ | `v_cho_reference` | reference cholesterol turnover \[mmole/min\] |  | mmol/min |  |
| $v_{\mathrm{synthesis}}$ | `v_synthesis` | total synthesized cholesterol |  | mg/day |  |
| $v_{\mathrm{uptake}}$ | `v_uptake` | cholesterol uptake (LDL receptor) |  | mg/day |  |
| $v_{\mathrm{export}}$ | `v_export` | cholesterol export (VLDL) |  | mg/day |  |
| $v_{\mathrm{reference}}$ | `v_reference` | cholesterol reference flux |  | mg/day |  |
| $v_{\mathrm{net\_export\_rate}}$ | `v_net_export_rate` | cholesterol net export (VLDL) |  | mmol/min |  |
| $v_{\mathrm{net\_export}}$ | `v_net_export` | cholesterol net export (VLDL) |  | mg/day |  |
| $v_{\mathrm{liver\_balance}}$ | `v_liver_balance` | cholesterol net  export (VLDL) |  | mg/day |  |
| $\mathrm{TURNOVER}_{\mathrm{LDLR}}$ | `TURNOVER_LDLR` | total turnover of LDL-R expression |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{hmgcoareductase} &= 1 \cdot \mathrm{Vli} \\[1ex]
\mathrm{hmgcoasynthase} &= 1 \cdot \mathrm{Vli} \\[1ex]
\mathrm{ldlr} &= 0.1 \cdot \mathrm{Vli} \\[1ex]
\mathrm{ldlr}_{\mathrm{membrane}} &= 0.8 \cdot \mathrm{Vbaso} \\[1ex]
\mathrm{ldlr}_{\mathrm{ldlc}} &= 0.1 \cdot \mathrm{Vli} \\[1ex]
\mathrm{ldlr}_{\mathrm{degraded}} &= 0 \cdot \mathrm{Vli}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
\mathrm{ldlr}_{\mathrm{total}} &= \mathrm{ldlr} + \mathrm{ldlr}_{\mathrm{membrane}} + \mathrm{ldlr}_{\mathrm{ldlc}} \\[1ex]
\mathrm{ldlr}_{\mathrm{fraction}} &= \frac{\mathrm{ldlr}}{\mathrm{ldlr}_{\mathrm{total}}} \\[1ex]
\mathrm{ldlr}_{\mathrm{membrane\_fraction}} &= \frac{\mathrm{ldlr}_{\mathrm{membrane}}}{\mathrm{ldlr}_{\mathrm{total}}} \\[1ex]
\mathrm{ldlr}_{\mathrm{ldlc\_fraction}} &= \frac{\mathrm{ldlr}_{\mathrm{ldlc}}}{\mathrm{ldlr}_{\mathrm{total}}} \\[1ex]
v_{\mathrm{cho\_reference}} &= \frac{\frac{v_{\mathrm{cho\_ref}}}{\mathrm{Mr}_{\mathrm{ldlc}}}}{\mathrm{conversion}_{\mathrm{min\_per\_day}}} \\[1ex]
\mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax}} &= 0.4 \cdot \mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax}} \\[1ex]
v_{\mathrm{reference}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{export}} &= v_{\mathrm{VLDLCEXP}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{uptake}} &= v_{\mathrm{LDLRLDLCIMP}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{net\_export\_rate}} &= v_{\mathrm{VLDLCEXP}} - v_{\mathrm{LDLRLDLCIMP}} \\[1ex]
v_{\mathrm{net\_export}} &= v_{\mathrm{net\_export\_rate}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{synthesis}} &= v_{\mathrm{HMGCOAREDUCTASE}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{liver\_balance}} &= v_{\mathrm{synthesis}} + v_{\mathrm{uptake}} - v_{\mathrm{export}} \\[1ex]
\mathrm{TURNOVER}_{\mathrm{LDLR}} &= v_{\mathrm{SYNTHESIS\_LDLR}} - v_{\mathrm{DEGRADATION\_LDLR}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $v_{\mathrm{PRAIM}}$ | `PRAIM` | pravastatin import (OATP1B1) | $\mathrm{pra}_{\mathrm{ext}} \longrightarrow \mathrm{pra}$ |  |
| $v_{\mathrm{PRAEX}}$ | `PRAEX` | pravastatin bile export (MRP2) | $\mathrm{pra} \longrightarrow \mathrm{pra}_{\mathrm{lumen}}$ |  |
| $v_{\mathrm{VLDLCEXP}}$ | `VLDLCEXP` | VLDL-cholesterol export | $\mathrm{cho} \longrightarrow \mathrm{vldlc}_{\mathrm{ext}}$ |  |
| $v_{\mathrm{LDLRLDLCIMP}}$ | `LDLRLDLCIMP` | LDLR-LDLC binding &amp; internalization | $\mathrm{ldlc}_{\mathrm{ext}} + \mathrm{ldlr}_{\mathrm{membrane}} \longrightarrow \mathrm{ldlr}_{\mathrm{ldlc}}$ | $\mathrm{ldlr}_{\mathrm{ldlc}}$ |
| $v_{\mathrm{LDLR\_TO\_MEMBRANE}}$ | `LDLR_TO_MEMBRANE` | LDLR membrane transport | $\mathrm{ldlr} \rightleftharpoons \mathrm{ldlr}_{\mathrm{membrane}}$ |  |
| $v_{\mathrm{LDLRRECYCLING}}$ | `LDLRRECYCLING` | LDLR recycling | $\mathrm{ldlr}_{\mathrm{ldlc}} \longrightarrow \mathrm{ldlr} + \mathrm{cho}$ |  |
| $v_{\mathrm{HMGCOASYNTHASE}}$ | `HMGCOASYNTHASE` | HMG-CoA synthase | $3 \, \mathrm{acoa} \longrightarrow \mathrm{hmgcoa}$ | $\mathrm{hmgcoasynthase}, \mathrm{hmgcoa}$ |
| $v_{\mathrm{HMGCOAREDUCTASE}}$ | `HMGCOAREDUCTASE` | HMG-CoA reductase | $6 \, \mathrm{hmgcoa} \longrightarrow \mathrm{cho}$ | $\mathrm{pra}, \mathrm{hmgcoareductase}$ |
| $v_{\mathrm{SYNTHESIS\_HMGCOAREDUCTASE}}$ | `SYNTHESIS_HMGCOAREDUCTASE` | HMGCOAREDUCTASE synthesis | $\varnothing \longrightarrow \mathrm{hmgcoareductase}$ | $\mathrm{cho}$ |
| $v_{\mathrm{DEGRADATION\_HMGCOAREDUCTASE}}$ | `DEGRADATION_HMGCOAREDUCTASE` | HMGCOAREDUCTASE degradation | $\mathrm{hmgcoareductase} \longrightarrow \varnothing$ | $\mathrm{cho}$ |
| $v_{\mathrm{SYNTHESIS\_HMGCOASYNTHASE}}$ | `SYNTHESIS_HMGCOASYNTHASE` | HMGCOASYNTHASE synthesis | $\varnothing \longrightarrow \mathrm{hmgcoasynthase}$ | $\mathrm{cho}$ |
| $v_{\mathrm{DEGRADATION\_HMGCOASYNTHASE}}$ | `DEGRADATION_HMGCOASYNTHASE` | HMGCOASYNTHASE degradation | $\mathrm{hmgcoasynthase} \longrightarrow \varnothing$ | $\mathrm{cho}$ |
| $v_{\mathrm{SYNTHESIS\_LDLR}}$ | `SYNTHESIS_LDLR` | LDLR synthesis | $\varnothing \longrightarrow \mathrm{ldlr}$ | $\mathrm{cho}$ |
| $v_{\mathrm{DEGRADATION\_LDLR}}$ | `DEGRADATION_LDLR` | LDLR degradation | $\mathrm{ldlr} \longrightarrow \mathrm{ldlr}_{\mathrm{degraded}}$ | $\mathrm{cho}$ |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{PRAIM}} &= \frac{f_{\mathrm{OATP1B1}} \cdot \mathrm{PRAIM}_{\mathrm{Vmax}} \cdot \mathrm{Vli} \cdot \mathrm{pra}_{\mathrm{ext}}}{\mathrm{pra}_{\mathrm{ext}} + \mathrm{PRAIM}_{\mathrm{Km\_pra}}} \\[1ex]
v_{\mathrm{PRAEX}} &= f_{\mathrm{MRP2}} \cdot \mathrm{PRAEX}_{\mathrm{k}} \cdot \mathrm{Vli} \cdot \mathrm{pra} \\[1ex]
v_{\mathrm{VLDLCEXP}} &= \frac{\mathrm{VLDLCEXP}_{\mathrm{Vmax}} \cdot v_{\mathrm{cho\_reference}} \cdot \mathrm{cho}}{\mathrm{cho} + \mathrm{VLDLCEXP}_{\mathrm{Km\_cho}}} \\[1ex]
v_{\mathrm{LDLRLDLCIMP}} &= \frac{\frac{v_{\mathrm{cho\_reference}} \cdot \mathrm{LDLRLDLCIMP}_{\mathrm{Kcat}} \cdot \mathrm{LDLRLDLCIMP}_{\mathrm{Kcat\_f}} \cdot \mathrm{ldlr}_{\mathrm{membrane}} \cdot \mathrm{ldlc}_{\mathrm{ext}}}{\mathrm{LDLRLDLCIMP}_{\mathrm{Km}} \cdot \mathrm{LDLRLDLCIMP}_{\mathrm{Km\_f}} + \mathrm{ldlc}_{\mathrm{ext}}} \cdot 1}{1 + \frac{\mathrm{ldlr}_{\mathrm{ldlc}}}{\mathrm{LDLRLDLCIMP}_{\mathrm{Ki\_ldlr\_ldlc}}}} \\[1ex]
v_{\mathrm{LDLR\_TO\_MEMBRANE}} &= \mathrm{Vli} \cdot \mathrm{LDLRMEMBRANE}_{\mathrm{Kcat}} \cdot \mathrm{LDLRMEMBRANE}_{\mathrm{Kcat\_f}} \cdot \mathopen{}\left(\mathrm{ldlr} - \frac{\mathrm{ldlr}_{\mathrm{membrane}}}{\mathrm{LDLRMEMBRANE}_{\mathrm{Keq}}}\right) \\[1ex]
v_{\mathrm{LDLRRECYCLING}} &= \mathrm{Vli} \cdot \mathrm{LDLRRECYCLING}_{\mathrm{Kcat}} \cdot \mathrm{LDLRRECYCLING}_{\mathrm{Kcat\_f}} \cdot \mathrm{ldlr}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{HMGCOASYNTHASE}} &= \frac{\mathrm{HMGCOASYNTHASE}_{\mathrm{Kcat}} \cdot v_{\mathrm{cho\_reference}} \cdot \mathrm{hmgcoasynthase} \cdot \mathrm{acoa}}{1 + \frac{\mathrm{hmgcoa}}{\mathrm{HMGCOASYNTHASE}_{\mathrm{Ki\_hmgcoa}}}} \\[1ex]
v_{\mathrm{HMGCOAREDUCTASE}} &= \frac{\mathrm{HMGCOAREDUCTASE}_{\mathrm{Kcat}} \cdot v_{\mathrm{cho\_reference}} \cdot \mathrm{hmgcoareductase} \cdot \mathrm{hmgcoa}}{\mathrm{HMGCOAREDUCTASE}_{\mathrm{Km}} \cdot \mathopen{}\left(1 + \frac{\mathrm{pra} \cdot \mathrm{pra}_{\mathrm{inhibitor\_activity}}}{\mathrm{HMGCOAREDUCTASE}_{\mathrm{Ki\_pra}}}\right) + \mathrm{hmgcoa}} \\[1ex]
v_{\mathrm{SYNTHESIS\_HMGCOAREDUCTASE}} &= \frac{\mathrm{SYNTHESIS}_{\mathrm{HMG\_Vmax}} \cdot \mathrm{Vli}}{1 + \frac{\mathrm{cho}}{\mathrm{HMG}_{\mathrm{kr\_cho}}}} \\[1ex]
v_{\mathrm{DEGRADATION\_HMGCOAREDUCTASE}} &= \mathrm{DEGRADATION}_{\mathrm{HMG\_Vmax}} \cdot \mathrm{hmgcoareductase} \cdot \mathrm{Vli} \cdot \mathopen{}\left(1 + \frac{\mathrm{cho}}{\mathrm{HMG}_{\mathrm{kr\_cho}}}\right) \\[1ex]
v_{\mathrm{SYNTHESIS\_HMGCOASYNTHASE}} &= \frac{\mathrm{SYNTHESIS}_{\mathrm{HMG\_Vmax}} \cdot \mathrm{Vli}}{1 + \frac{\mathrm{cho}}{\mathrm{HMG}_{\mathrm{kr\_cho}}}} \\[1ex]
v_{\mathrm{DEGRADATION\_HMGCOASYNTHASE}} &= \mathrm{DEGRADATION}_{\mathrm{HMG\_Vmax}} \cdot \mathrm{hmgcoasynthase} \cdot \mathrm{Vli} \cdot \mathopen{}\left(1 + \frac{\mathrm{cho}}{\mathrm{HMG}_{\mathrm{kr\_cho}}}\right) \\[1ex]
v_{\mathrm{SYNTHESIS\_LDLR}} &= \frac{\mathrm{Vli} \cdot \mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax}} \cdot \mathrm{SYNTHESIS}_{\mathrm{LDLR\_Vmax\_f}}}{1 + \frac{\mathrm{cho}}{\mathrm{LDLR}_{\mathrm{kr\_cho}}}} \\[1ex]
v_{\mathrm{DEGRADATION\_LDLR}} &= \mathrm{Vli} \cdot \mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax}} \cdot \mathrm{DEGRADATION}_{\mathrm{LDLR\_Vmax\_f}} \cdot \mathrm{ldlr} \cdot \mathopen{}\left(1 + \frac{\mathrm{cho}}{\mathrm{LDLR}_{\mathrm{kr\_cho}}}\right)
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{pra}}{\mathrm{d} t} &= \frac{v_{\mathrm{PRAIM}} - v_{\mathrm{PRAEX}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{pra}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{PRAIM}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{pra}_{\mathrm{lumen}}}{\mathrm{d} t} &= \frac{v_{\mathrm{PRAEX}}}{\mathrm{Vlumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{vldlc}_{\mathrm{ext}}}{\mathrm{d} t} &= \frac{v_{\mathrm{VLDLCEXP}}}{\mathrm{Vext}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hmgcoa}}{\mathrm{d} t} &= \frac{v_{\mathrm{HMGCOASYNTHASE}} - 6 \cdot v_{\mathrm{HMGCOAREDUCTASE}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cho}}{\mathrm{d} t} &= \frac{-v_{\mathrm{VLDLCEXP}} + v_{\mathrm{LDLRRECYCLING}} + v_{\mathrm{HMGCOAREDUCTASE}}}{\mathrm{Vli}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hmgcoareductase}}{\mathrm{d} t} &= \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{SYNTHESIS\_HMGCOAREDUCTASE}} - \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{DEGRADATION\_HMGCOAREDUCTASE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{hmgcoasynthase}}{\mathrm{d} t} &= \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{SYNTHESIS\_HMGCOASYNTHASE}} - \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{DEGRADATION\_HMGCOASYNTHASE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ldlr}}{\mathrm{d} t} &= -\mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLR\_TO\_MEMBRANE}} + \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLRRECYCLING}} + \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{SYNTHESIS\_LDLR}} - \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{DEGRADATION\_LDLR}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ldlr}_{\mathrm{membrane}}}{\mathrm{d} t} &= -\mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLRLDLCIMP}} + \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLR\_TO\_MEMBRANE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ldlr}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLRLDLCIMP}} - \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{LDLRRECYCLING}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{ldlr}_{\mathrm{degraded}}}{\mathrm{d} t} &= \mathrm{cf}_{\mathrm{units\_per\_mmole}} \cdot v_{\mathrm{DEGRADATION\_LDLR}}
\end{aligned}
$$
