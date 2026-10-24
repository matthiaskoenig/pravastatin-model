# Cholesterol whole body model for coupling with pravastatin

Model `pravastatin_body_all`, SBML Level 3 Version 2, read from pravastatin\_body\_all\_flat.xml, written by sbmlode 0.3.0.

PK/PD model for whole-body cholesterol metabolism.

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
| $\mathrm{Vre}$ | `Vre` | rest of body |  | l |  |
| $\mathrm{Vgu}$ | `Vgu` | gut |  | l |  |
| $\mathrm{Vki}$ | `Vki` | kidney |  | l |  |
| $\mathrm{Vli}$ | `Vli` | liver |  | l |  |
| $\mathrm{Vlu}$ | `Vlu` | lung |  | l |  |
| $\mathrm{Vve}$ | `Vve` | venous blood |  | l |  |
| $\mathrm{Var}$ | `Var` | arterial blood |  | l |  |
| $\mathrm{Vurine}$ | `Vurine` | urine | $1$ | l | ✓ |
| $\mathrm{Vfeces}$ | `Vfeces` | feces | $1$ | l | ✓ |
| $\mathrm{Vstomach}$ | `Vstomach` | stomach | $1$ | l | ✓ |
| $\mathrm{Vpo}$ | `Vpo` | portal plasma |  | l |  |
| $\mathrm{Vhv}$ | `Vhv` | hepatic venous plasma |  | l |  |
| $\mathrm{Vgu}_{\mathrm{tissue}}$ | `Vgu_tissue` | gu tissue |  | l |  |
| $\mathrm{Vgu}_{\mathrm{plasma}}$ | `Vgu_plasma` | gu plasma |  | l |  |
| $\mathrm{Vki}_{\mathrm{tissue}}$ | `Vki_tissue` | ki tissue |  | l |  |
| $\mathrm{Vki}_{\mathrm{plasma}}$ | `Vki_plasma` | ki plasma |  | l |  |
| $\mathrm{Vli}_{\mathrm{tissue}}$ | `Vli_tissue` | li tissue |  | l |  |
| $\mathrm{Vli}_{\mathrm{plasma}}$ | `Vli_plasma` | li plasma |  | l |  |
| $\mathrm{Vlu}_{\mathrm{tissue}}$ | `Vlu_tissue` | lu tissue |  | l |  |
| $\mathrm{Vlu}_{\mathrm{plasma}}$ | `Vlu_plasma` | lu plasma |  | l |  |
| $\mathrm{Vre}_{\mathrm{tissue}}$ | `Vre_tissue` | re tissue |  | l |  |
| $\mathrm{Vre}_{\mathrm{plasma}}$ | `Vre_plasma` | re plasma |  | l |  |
| $\mathrm{Vgulumen}$ | `Vgulumen` | gut lumen |  | l |  |
| $\mathrm{LI}_{\mathrm{\_Vbaso}}$ | `LI__Vbaso` | basolateral membrane | $1$ | m<sup>2</sup> | ✓ |

## Species

| Symbol | Id | Name | Compartment | Value | Unit | Properties |
| --- | --- | --- | --- | --- | --- | --- |
| $\mathrm{Cgu}_{\mathrm{plasma\_pra}}$ | `Cgu_plasma_pra` | pravastatin (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_pra}}$ | `Cki_plasma_pra` | pravastatin (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_pra}}$ | `Cli_plasma_pra` | pravastatin (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_pra}}$ | `Clu_plasma_pra` | pravastatin (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_pra}}$ | `Cre_plasma_pra` | pravastatin (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{pra}}$ | `Car_pra` | pravastatin (arterial blood plasma) | $\mathrm{Var}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{pra}}$ | `Cve_pra` | pravastatin (venous blood plasma) | $\mathrm{Vve}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{pra}}$ | `Cpo_pra` | pravastatin (portal vein plasma) | $\mathrm{Vpo}$ | $0$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{pra}}$ | `Chv_pra` | pravastatin (hepatic vein plasma) | $\mathrm{Vhv}$ | $0$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{pra}}$ | `Clu_pra` | pravastatin (lung) | $\mathrm{Vlu}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{pra}}$ | `Cre_pra` | pravastatin (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{deep\_pra}}$ | `Cre_deep_pra` | pravastatin deep (rest) | $\mathrm{Vre}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{Aurine}_{\mathrm{pra}}$ | `Aurine_pra` | pravastatin (urine) | $\mathrm{Vurine}$ |  | mmol | amount |
| $\mathrm{Afeces}_{\mathrm{pra}}$ | `Afeces_pra` | pravastatin (feces) | $\mathrm{Vfeces}$ |  | mmol | amount |
| $\mathrm{Cgulumen}_{\mathrm{pra}}$ | `Cgulumen_pra` | pravastatin (gut lumen) | $\mathrm{Vgulumen}$ | $0$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_ldlc}}$ | `Cgu_plasma_ldlc` | ldl-cholesterol (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_ldlc}}$ | `Cki_plasma_ldlc` | ldl-cholesterol (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_ldlc}}$ | `Cli_plasma_ldlc` | ldl-cholesterol (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_ldlc}}$ | `Clu_plasma_ldlc` | ldl-cholesterol (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_ldlc}}$ | `Cre_plasma_ldlc` | ldl-cholesterol (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $3$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{ldlc}}$ | `Car_ldlc` | ldl-cholesterol (arterial blood plasma) | $\mathrm{Var}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{ldlc}}$ | `Cve_ldlc` | ldl-cholesterol (venous blood plasma) | $\mathrm{Vve}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{ldlc}}$ | `Cpo_ldlc` | ldl-cholesterol (portal vein plasma) | $\mathrm{Vpo}$ | $3$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{ldlc}}$ | `Chv_ldlc` | ldl-cholesterol (hepatic vein plasma) | $\mathrm{Vhv}$ | $3$ | mmol/l | concentration |
| $\mathrm{Cgu}_{\mathrm{plasma\_vldlc}}$ | `Cgu_plasma_vldlc` | vldl-cholesterol (gut plasma) | $\mathrm{Vgu}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cki}_{\mathrm{plasma\_vldlc}}$ | `Cki_plasma_vldlc` | vldl-cholesterol (kidney plasma) | $\mathrm{Vki}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cli}_{\mathrm{plasma\_vldlc}}$ | `Cli_plasma_vldlc` | vldl-cholesterol (liver plasma) | $\mathrm{Vli}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Clu}_{\mathrm{plasma\_vldlc}}$ | `Clu_plasma_vldlc` | vldl-cholesterol (lung plasma) | $\mathrm{Vlu}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cre}_{\mathrm{plasma\_vldlc}}$ | `Cre_plasma_vldlc` | vldl-cholesterol (rest plasma) | $\mathrm{Vre}_{\mathrm{plasma}}$ | $1$ | mmol/l | concentration |
| $\mathrm{Car}_{\mathrm{vldlc}}$ | `Car_vldlc` | vldl-cholesterol (arterial blood plasma) | $\mathrm{Var}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cve}_{\mathrm{vldlc}}$ | `Cve_vldlc` | vldl-cholesterol (venous blood plasma) | $\mathrm{Vve}$ | $1$ | mmol/l | concentration |
| $\mathrm{Cpo}_{\mathrm{vldlc}}$ | `Cpo_vldlc` | vldl-cholesterol (portal vein plasma) | $\mathrm{Vpo}$ | $1$ | mmol/l | concentration |
| $\mathrm{Chv}_{\mathrm{vldlc}}$ | `Chv_vldlc` | vldl-cholesterol (hepatic vein plasma) | $\mathrm{Vhv}$ | $1$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_pra}}$ | `LI__pra` | pravastatin (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_acoa}}$ | `LI__acoa` | acetyl-CoA (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0.043$ | mmol/l | concentration, boundary |
| $\mathrm{LI}_{\mathrm{\_hmgcoa}}$ | `LI__hmgcoa` | HMG-CoA (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0.022$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_cho}}$ | `LI__cho` | cholesterol (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ | $0.02$ | mmol/l | concentration |
| $\mathrm{LI}_{\mathrm{\_hmgcoareductase}}$ | `LI__hmgcoareductase` | HMG-CoA reductase (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_hmgcoasynthase}}$ | `LI__hmgcoasynthase` | HMG-CoA synthase (liver) | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_ldlr}}$ | `LI__ldlr` | LDLR | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_ldlr\_membrane}}$ | `LI__ldlr_membrane` | LDLR membrane | $\mathrm{LI}_{\mathrm{\_Vbaso}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}$ | `LI__ldlr_ldlc` | LDLR-LDLC complex | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{LI}_{\mathrm{\_ldlr\_degraded}}$ | `LI__ldlr_degraded` | LDLR degraded | $\mathrm{Vli}_{\mathrm{tissue}}$ |  | \- | amount |
| $\mathrm{GU}_{\mathrm{\_pra\_stomach}}$ | `GU__pra_stomach` | pravastatin (stomach) | $\mathrm{Vstomach}$ |  | mmol | amount, boundary |

## Parameters

| Symbol | Id | Name | Value | Unit | Constant |
| --- | --- | --- | --- | --- | :---: |
| $f_{\mathrm{lumen}}$ | `f_lumen` | fraction lumen of intestine | $0.9$ | \- | ✓ |
| $\mathrm{BW}$ | `BW` | body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{BW}_{\mathrm{ref}}$ | `BW_ref` | reference body weight \[kg\] | $75$ | kg | ✓ |
| $\mathrm{HEIGHT}$ | `HEIGHT` | height \[cm\] | $170$ | cm | ✓ |
| $\mathrm{HR}$ | `HR` | heart rate \[1/min\] | $70$ | 1/min | ✓ |
| $\mathrm{HRrest}$ | `HRrest` | resting heart rate \[1/min\] | $70$ | 1/min | ✓ |
| $\mathrm{BSA}$ | `BSA` | body surface area \[m^2\] |  | m<sup>2</sup> |  |
| $\mathrm{COBW}$ | `COBW` | cardiac output per bodyweight \[ml/s/kg\] | $1.25$ | ml/s/kg | ✓ |
| $\mathrm{CO}$ | `CO` | cardiac output \[ml/s\] |  | ml/s |  |
| $\mathrm{QC}$ | `QC` | cardiac output \[L/min\] |  | l/min |  |
| $\mathrm{COHRI}$ | `COHRI` | increase of cardiac output per heartbeat \[ml/min\*min\] | $150$ | ml | ✓ |
| $\mathrm{Fblood}$ | `Fblood` | blood fraction of organ volume | $0.02$ | \- |  |
| $\mathrm{HCT}$ | `HCT` | hematocrit | $0.51$ | \- | ✓ |
| $\mathrm{FVgi}$ | `FVgi` | fractional tissue volume gastrointestinal tract | $0.0297$ | l/kg | ✓ |
| $\mathrm{FVki}$ | `FVki` | kidney fractional tissue volume | $0.0044$ | l/kg | ✓ |
| $\mathrm{FVli}$ | `FVli` | liver fractional tissue volume | $0.021$ | l/kg | ✓ |
| $\mathrm{FVlu}$ | `FVlu` | lung fractional tissue volume | $0.0076$ | l/kg | ✓ |
| $\mathrm{FVre}$ | `FVre` | rest of body fractional tissue volume |  | l/kg |  |
| $\mathrm{FVve}$ | `FVve` | venous fractional tissue volume | $0.0514$ | l/kg | ✓ |
| $\mathrm{FVar}$ | `FVar` | arterial fractional tissue volume | $0.0257$ | l/kg | ✓ |
| $\mathrm{FVpo}$ | `FVpo` | portal fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FVhv}$ | `FVhv` | hepatic venous fractional tissue volume | $0.001$ | l/kg | ✓ |
| $\mathrm{FQgu}$ | `FQgu` | gut fractional tissue blood flow | $0.18$ | \- | ✓ |
| $\mathrm{FQki}$ | `FQki` | kidney fractional tissue blood flow | $0.19$ | \- | ✓ |
| $\mathrm{FQh}$ | `FQh` | hepatic (venous side) fractional tissue blood flow | $0.215$ | \- | ✓ |
| $\mathrm{FQlu}$ | `FQlu` | lung fractional tissue blood flow | $1$ | \- | ✓ |
| $\mathrm{FQre}$ | `FQre` | rest of body fractional tissue blood flow |  | \- |  |
| $\mathrm{conversion}_{\mathrm{min\_per\_day}}$ | `conversion_min_per_day` | Conversion factor min to day | $1440$ | min/day | ✓ |
| $f_{\mathrm{cirrhosis}}$ | `f_cirrhosis` | severity of cirrhosis \[0, 0.95\] | $0$ | \- | ✓ |
| $f_{\mathrm{shunts}}$ | `f_shunts` | fraction of portal venous blood shunted by the liver |  | \- |  |
| $f_{\mathrm{tissue\_loss}}$ | `f_tissue_loss` | fraction of lost parenchymal liver volume |  | \- |  |
| $\mathrm{fu}_{\mathrm{pra}}$ | `fu_pra` | fraction unbound in plasma pravastatin | $0.5$ | \- | ✓ |
| $f_{\mathrm{GFR\_Qki}}$ | `f_GFR_Qki` | relationship GFR and Qki | $94.5029239766082$ | ml/l | ✓ |
| $\mathrm{GFR}_{\mathrm{base}}$ | `GFR_base` | glomerular filtration rate (healthy) |  | ml/min |  |
| $\mathrm{Mr}_{\mathrm{pra}}$ | `Mr_pra` | Molecular weight pra \[g/mole\] | $424.53$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{pra}}$ | `ftissue_pra` | tissue distribution pra | $20$ | l/min | ✓ |
| $\mathrm{Kp}_{\mathrm{pra}}$ | `Kp_pra` | tissue/plasma partition coefficient pra | $0.172885468603702$ | \- | ✓ |
| $\mathrm{Kpdeep}_{\mathrm{pra}}$ | `Kpdeep_pra` | deep/tissue partition coefficient pra | $0.85$ | \- | ✓ |
| $\mathrm{kdeep}_{\mathrm{pra}}$ | `kdeep_pra` | rate of the deep distribution pra | $0.011$ | 1/min | ✓ |
| $\mathrm{IVDOSE}_{\mathrm{pra}}$ | `IVDOSE_pra` | IV bolus dose pra \[mg\] | $0$ | mg |  |
| $\mathrm{ti}_{\mathrm{pra}}$ | `ti_pra` | injection time pra \[s\] | $10$ | s | ✓ |
| $\mathrm{Ki}_{\mathrm{pra}}$ | `Ki_pra` | Ki \[1/min\] injection pra |  | 1/min |  |
| $\mathrm{Ri}_{\mathrm{pra}}$ | `Ri_pra` | Ri \[mg/min\] rate of infusion pra | $0$ | mg/min | ✓ |
| $\mathrm{cum}_{\mathrm{dose\_pra}}$ | `cum_dose_pra` | Cumulative dose due to infusion pra | $0$ | mg |  |
| $\mathrm{PODOSE}_{\mathrm{pra}}$ | `PODOSE_pra` | oral dose pra \[mg\] | $0$ | mg |  |
| $\mathrm{pra}_{\mathrm{inhibitor\_activity}}$ | `pra_inhibitor_activity` | HMG-CoA Reductase inhibitor activity of pravastatin | $1$ | \- | ✓ |
| $\mathrm{Mr}_{\mathrm{ldlc}}$ | `Mr_ldlc` | Molecular weight ldlc \[g/mole\] | $386.654$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{ldlc}}$ | `ftissue_ldlc` | tissue distribution ldlc | $0$ | l/min | ✓ |
| $\mathrm{Mr}_{\mathrm{vldlc}}$ | `Mr_vldlc` | Molecular weight vldlc \[g/mole\] | $386.654$ | g/mol | ✓ |
| $\mathrm{ftissue}_{\mathrm{vldlc}}$ | `ftissue_vldlc` | tissue distribution vldlc | $0$ | l/min | ✓ |
| $\mathrm{ldlc}_{\mathrm{init}}$ | `ldlc_init` | Initial LDLC -concentration | $3$ | mmol/l | ✓ |
| $v_{\mathrm{cho\_ref}}$ | `v_cho_ref` | reference cholesterol turnover \[mg/day\] | $1000$ | mg/day | ✓ |
| $\mathrm{ldlc}_{\mathrm{diet\_k}}$ | `ldlc_diet_k` | rate of cholesterol uptake from diet | $1$ | \- | ✓ |
| $\mathrm{ldlc}_{\mathrm{loss\_k}}$ | `ldlc_loss_k` | rate of cholesterol loss in feces | $1.2$ | \- | ✓ |
| $\mathrm{ldlc}_{\mathrm{utilization\_Vmax}}$ | `ldlc_utilization_Vmax` |  | $0.65214377029393$ | \- | ✓ |
| $\mathrm{ldlc}_{\mathrm{consumption\_Km}}$ | `ldlc_consumption_Km` |  | $60$ | mmol/l | ✓ |
| $f_{\mathrm{ldlc\_utilization\_Vmax}}$ | `f_ldlc_utilization_Vmax` | scaling factor for utilization | $1$ | \- | ✓ |
| $\mathrm{vldlc}_{\mathrm{conversion\_k}}$ | `vldlc_conversion_k` | conversion rate for plasma vldlc into plasma ldlc | $2$ | l/mmol | ✓ |
| $\mathrm{Qgu}$ | `Qgu` | gut blood flow |  | l/min |  |
| $\mathrm{Qki}$ | `Qki` | kidney blood flow |  | l/min |  |
| $\mathrm{Qh}$ | `Qh` | hepatic (venous side) blood flow |  | l/min |  |
| $\mathrm{Qha}$ | `Qha` | hepatic artery blood flow |  | l/min |  |
| $\mathrm{Qlu}$ | `Qlu` | lung blood flow |  | l/min |  |
| $\mathrm{Qre}$ | `Qre` | rest of body blood flow |  | l/min |  |
| $\mathrm{Qpo}$ | `Qpo` | portal blood flow |  | l/min |  |
| $\mathrm{Agu}_{\mathrm{plasma\_pra}}$ | `Agu_plasma_pra` | pravastatin amount (gut) \[mmole\] |  | mmol |  |
| $\mathrm{Xgu}_{\mathrm{plasma\_pra}}$ | `Xgu_plasma_pra` | pravastatin amount (gut) \[mg\] |  | mg |  |
| $\mathrm{Mgu}_{\mathrm{plasma\_pra}}$ | `Mgu_plasma_pra` | pravastatin concentration (gut) \[mg/l\] |  | mg/l |  |
| $\mathrm{Aki}_{\mathrm{plasma\_pra}}$ | `Aki_plasma_pra` | pravastatin amount (kidney) \[mmole\] |  | mmol |  |
| $\mathrm{Xki}_{\mathrm{plasma\_pra}}$ | `Xki_plasma_pra` | pravastatin amount (kidney) \[mg\] |  | mg |  |
| $\mathrm{Mki}_{\mathrm{plasma\_pra}}$ | `Mki_plasma_pra` | pravastatin concentration (kidney) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ali}_{\mathrm{plasma\_pra}}$ | `Ali_plasma_pra` | pravastatin amount (liver) \[mmole\] |  | mmol |  |
| $\mathrm{Xli}_{\mathrm{plasma\_pra}}$ | `Xli_plasma_pra` | pravastatin amount (liver) \[mg\] |  | mg |  |
| $\mathrm{Mli}_{\mathrm{plasma\_pra}}$ | `Mli_plasma_pra` | pravastatin concentration (liver) \[mg/l\] |  | mg/l |  |
| $\mathrm{Alu}_{\mathrm{plasma\_pra}}$ | `Alu_plasma_pra` | pravastatin amount (lung) \[mmole\] |  | mmol |  |
| $\mathrm{Xlu}_{\mathrm{plasma\_pra}}$ | `Xlu_plasma_pra` | pravastatin amount (lung) \[mg\] |  | mg |  |
| $\mathrm{Mlu}_{\mathrm{plasma\_pra}}$ | `Mlu_plasma_pra` | pravastatin concentration (lung) \[mg/l\] |  | mg/l |  |
| $\mathrm{Are}_{\mathrm{plasma\_pra}}$ | `Are_plasma_pra` | pravastatin amount (rest) \[mmole\] |  | mmol |  |
| $\mathrm{Xre}_{\mathrm{plasma\_pra}}$ | `Xre_plasma_pra` | pravastatin amount (rest) \[mg\] |  | mg |  |
| $\mathrm{Mre}_{\mathrm{plasma\_pra}}$ | `Mre_plasma_pra` | pravastatin concentration (rest) \[mg/l\] |  | mg/l |  |
| $\mathrm{Aar}_{\mathrm{pra}}$ | `Aar_pra` | pravastatin amount (arterial blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xar}_{\mathrm{pra}}$ | `Xar_pra` | pravastatin amount (arterial blood) \[mg\] |  | mg |  |
| $\mathrm{Mar}_{\mathrm{pra}}$ | `Mar_pra` | pravastatin concentration (arterial blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ave}_{\mathrm{pra}}$ | `Ave_pra` | pravastatin amount (venous blood) \[mmole\] |  | mmol |  |
| $\mathrm{Xve}_{\mathrm{pra}}$ | `Xve_pra` | pravastatin amount (venous blood) \[mg\] |  | mg |  |
| $\mathrm{Mve}_{\mathrm{pra}}$ | `Mve_pra` | pravastatin concentration (venous blood) \[mg/l\] |  | mg/l |  |
| $\mathrm{Apo}_{\mathrm{pra}}$ | `Apo_pra` | pravastatin amount (portal vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xpo}_{\mathrm{pra}}$ | `Xpo_pra` | pravastatin amount (portal vein) \[mg\] |  | mg |  |
| $\mathrm{Mpo}_{\mathrm{pra}}$ | `Mpo_pra` | pravastatin concentration (portal vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Ahv}_{\mathrm{pra}}$ | `Ahv_pra` | pravastatin amount (hepatic vein) \[mmole\] |  | mmol |  |
| $\mathrm{Xhv}_{\mathrm{pra}}$ | `Xhv_pra` | pravastatin amount (hepatic vein) \[mg\] |  | mg |  |
| $\mathrm{Mhv}_{\mathrm{pra}}$ | `Mhv_pra` | pravastatin concentration (hepatic vein) \[mg/l\] |  | mg/l |  |
| $\mathrm{Xurine}_{\mathrm{pra}}$ | `Xurine_pra` | pravastatin amount (urine) \[mg\] |  | mg |  |
| $\mathrm{Xfeces}_{\mathrm{pra}}$ | `Xfeces_pra` | pravastatin amount (feces) |  | mg |  |
| $\mathrm{ldlc}_{\mathrm{change}}$ | `ldlc_change` | relative LDL-C reduction in plasma in \[0,-1\] |  | \- |  |
| $v_{\mathrm{cho\_reference}}$ | `v_cho_reference` | reference cholesterol turnover \[mmole/min\] |  | mmol/min |  |
| $\mathrm{ldlc}_{\mathrm{loss}}$ | `ldlc_loss` | total loss of cholesterol |  | mmol/min |  |
| $\mathrm{ldlc}_{\mathrm{diet}}$ | `ldlc_diet` | total dietary cholesterol |  | mmol/min |  |
| $\mathrm{ldlc}_{\mathrm{utilization}}$ | `ldlc_utilization` | total utilized cholesterol |  | mmol/min |  |
| $v_{\mathrm{ldlc\_net\_consumption}}$ | `v_ldlc_net_consumption` | plasma cholesterol net consumption \[mg/day\] |  | mg/day |  |
| $v_{\mathrm{vldlc\_conversion}}$ | `v_vldlc_conversion` | plasma vldlc conversion into ldlc \[mg/day\] |  | mg/day |  |
| $v_{\mathrm{ldlc\_utilization}}$ | `v_ldlc_utilization` | plasma cholesterol net consumption \[mg/day\] |  | mg/day |  |
| $v_{\mathrm{ldlc\_diet}}$ | `v_ldlc_diet` | plasma cholesterol diet \[mg/day\] |  | mg/day |  |
| $v_{\mathrm{ldlc\_loss}}$ | `v_ldlc_loss` | plasma cholesterol loss \[mg/day\] |  | mg/day |  |
| $\mathrm{KI}_{\mathrm{\_f\_renal\_function}}$ | `KI__f_renal_function` | renal function | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_PRAEX\_f}}$ | `KI__PRAEX_f` | renal clearance of unbound pravastatin relative to the GFR | $16.5960789851112$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_f\_OAT3}}$ | `KI__f_OAT3` | parameter for OAT3 activity | $1$ | \- | ✓ |
| $\mathrm{KI}_{\mathrm{\_GFR}}$ | `KI__GFR` | glomerular filtration rate |  | ml/min |  |
| $\mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}}$ | `LI__cf_units_per_mmole` | conversion factor for dimensionless species | $1$ | 1/mmol | ✓ |
| $\mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}}$ | `LI__conversion_min_per_day` | conversion factor min to hours | $1440$ | min/day | ✓ |
| $\mathrm{LI}_{\mathrm{\_SYNTHESIS\_HMG\_Vmax}}$ | `LI__SYNTHESIS_HMG_Vmax` | Protein synthesis Vmax for HMGR and HMGS | $0.001$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DEGRADATION\_HMG\_Vmax}}$ | `LI__DEGRADATION_HMG_Vmax` | Protein degradation Vmax for HMGR and HMGS | $0.0003$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}$ | `LI__HMG_kr_cho` | Protein regulation kr for HMGR and HMGS | $0.02$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax}}$ | `LI__DEGRADATION_LDLR_Vmax` | Protein degradation Vmax for LDLR | $0.0006$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax}}$ | `LI__SYNTHESIS_LDLR_Vmax` | Protein synthesis Vmax for LDLR |  | mmol/min/l |  |
| $\mathrm{LI}_{\mathrm{\_LDLR\_kr\_cho}}$ | `LI__LDLR_kr_cho` | Protein regulation kr for LDLR | $0.02$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax\_f}}$ | `LI__SYNTHESIS_LDLR_Vmax_f` | scaling factor for synthesis Vmax for LDL-R | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax\_f}}$ | `LI__DEGRADATION_LDLR_Vmax_f` | scaling factor for degradation Vmax for LDL-R | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_PRAIM\_Vmax}}$ | `LI__PRAIM_Vmax` | Vmax for pravastatin import via OATP1B1 | $0.00492447459626885$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_OATP1B1}}$ | `LI__f_OATP1B1` | parameter for OATP1B1 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_PRAIM\_Km\_pra}}$ | `LI__PRAIM_Km_pra` | Km for pravastatin import via OATP1B1 | $0.01$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_PRAEX\_k}}$ | `LI__PRAEX_k` | rate for pravastatin export via MRP2 | $0.1$ | 1/min | ✓ |
| $\mathrm{LI}_{\mathrm{\_f\_MRP2}}$ | `LI__f_MRP2` | parameter for MRP2 activity | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_VLDLCEXP\_Vmax}}$ | `LI__VLDLCEXP_Vmax` | Vmax VLDL-cholesterol export | $2.5$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_VLDLCEXP\_Km\_cho}}$ | `LI__VLDLCEXP_Km_cho` | Km VLDL-cholesterol export | $0.0005$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Kcat}}$ | `LI__LDLRLDLCIMP_Kcat` |  | $6$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Km}}$ | `LI__LDLRLDLCIMP_Km` | Km LDLR-LDLC binding | $3$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Ki\_ldlr\_ldlc}}$ | `LI__LDLRLDLCIMP_Ki_ldlr_ldlc` | Ki LDLR-LDLC complex on uptake | $0.1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Km\_f}}$ | `LI__LDLRLDLCIMP_Km_f` |  | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Kcat\_f}}$ | `LI__LDLRLDLCIMP_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Kcat}}$ | `LI__LDLRMEMBRANE_Kcat` |  | $0.025$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Kcat\_f}}$ | `LI__LDLRMEMBRANE_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Keq}}$ | `LI__LDLRMEMBRANE_Keq` |  | $10$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRRECYCLING\_Kcat}}$ | `LI__LDLRRECYCLING_Kcat` |  | $0.0125$ | mmol/min/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_LDLRRECYCLING\_Kcat\_f}}$ | `LI__LDLRRECYCLING_Kcat_f` |  | $1$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOASYNTHASE\_Kcat}}$ | `LI__HMGCOASYNTHASE_Kcat` |  | $245$ | l/mmol | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOASYNTHASE\_Ki\_hmgcoa}}$ | `LI__HMGCOASYNTHASE_Ki_hmgcoa` |  | $0.022$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Kcat}}$ | `LI__HMGCOAREDUCTASE_Kcat` |  | $0.7$ | \- | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Km}}$ | `LI__HMGCOAREDUCTASE_Km` | Km HMG-CoA | $0.004$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Ki\_pra}}$ | `LI__HMGCOAREDUCTASE_Ki_pra` | Ki HMG-CoA for pravastatin | $2.3 \times 10^{-6}$ | mmol/l | ✓ |
| $\mathrm{LI}_{\mathrm{\_ldlr\_total}}$ | `LI__ldlr_total` | Total LDLR |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_ldlr\_fraction}}$ | `LI__ldlr_fraction` | LDLR fraction |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_ldlr\_membrane\_fraction}}$ | `LI__ldlr_membrane_fraction` | LDLR membrane fraction |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_ldlr\_ldlc\_fraction}}$ | `LI__ldlr_ldlc_fraction` | LDLR-LDLC fraction |  | \- |  |
| $\mathrm{LI}_{\mathrm{\_v\_cho\_reference}}$ | `LI__v_cho_reference` | reference cholesterol turnover \[mmole/min\] |  | mmol/min |  |
| $\mathrm{LI}_{\mathrm{\_v\_synthesis}}$ | `LI__v_synthesis` | total synthesized cholesterol |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_uptake}}$ | `LI__v_uptake` | cholesterol uptake (LDL receptor) |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_export}}$ | `LI__v_export` | cholesterol export (VLDL) |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_reference}}$ | `LI__v_reference` | cholesterol reference flux |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_net\_export\_rate}}$ | `LI__v_net_export_rate` | cholesterol net export (VLDL) |  | mmol/min |  |
| $\mathrm{LI}_{\mathrm{\_v\_net\_export}}$ | `LI__v_net_export` | cholesterol net export (VLDL) |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_v\_liver\_balance}}$ | `LI__v_liver_balance` | cholesterol net  export (VLDL) |  | mg/day |  |
| $\mathrm{LI}_{\mathrm{\_TURNOVER\_LDLR}}$ | `LI__TURNOVER_LDLR` | total turnover of LDL-R expression |  | mmol/min |  |
| $\mathrm{GU}_{\mathrm{\_F\_pra\_abs}}$ | `GU__F_pra_abs` | fraction absorbed pravastatin (fasted) | $0.217463051507184$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_PRAABS\_k}}$ | `GU__PRAABS_k` | rate of pravastatin leaving the intestinal lumen | $0.0219368198080403$ | 1/min | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_OATP2B1}}$ | `GU__f_OATP2B1` | parameter for OATP2B1 activity | $1$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_fed}}$ | `GU__fed` | fed state (0 fasted, 1 fed) | $0$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_FED\_f\_absorption}}$ | `GU__FED_f_absorption` | fed effect on the fraction absorbed | $0.75$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_FED\_f\_dissolution}}$ | `GU__FED_f_dissolution` | fed effect on the dissolution and gastric emptying | $0.4$ | \- | ✓ |
| $\mathrm{GU}_{\mathrm{\_POSTOMACH\_pra}}$ | `GU__POSTOMACH_pra` | oral dose in stomach pravastatin \[mg\] | $0$ | mg |  |
| $\mathrm{GU}_{\mathrm{\_Ka\_application\_pra}}$ | `GU__Ka_application_pra` | Ka \[1/hr\] application pravastatin | $1000$ | 1/hr | ✓ |
| $\mathrm{GU}_{\mathrm{\_Ka\_dis\_pra}}$ | `GU__Ka_dis_pra` | Ka\_dis \[1/hr\] dissolution pravastatin | $2.01072783691315$ | 1/hr | ✓ |
| $\mathrm{GU}_{\mathrm{\_f\_absorption}}$ | `GU__f_absorption` | factor of the fraction absorbed |  | \- |  |
| $\mathrm{GU}_{\mathrm{\_f\_dissolution}}$ | `GU__f_dissolution` | factor of the dissolution and gastric emptying |  | \- |  |
| $\mathrm{GU}_{\mathrm{\_F\_absorbed}}$ | `GU__F_absorbed` | fraction absorbed |  | \- |  |
| $\mathrm{GU}_{\mathrm{\_absorption}}$ | `GU__absorption` | pravastatin leaving the lumen |  | mmol/min |  |

## Initial assignments and assignment rules

The initial assignments set the values at $t = 0$:

$$
\begin{aligned}
\mathrm{Aurine}_{\mathrm{pra}} &= 0 \cdot \mathrm{Vurine} \\[1ex]
\mathrm{Afeces}_{\mathrm{pra}} &= 0 \cdot \mathrm{Vfeces} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_membrane}} &= 0.8 \cdot \mathrm{LI}_{\mathrm{\_Vbaso}} \\[1ex]
\mathrm{GU}_{\mathrm{\_pra\_stomach}} &= 0 \cdot \mathrm{Vstomach} \\[1ex]
\mathrm{LI}_{\mathrm{\_hmgcoareductase}} &= 1 \cdot \mathrm{Vli}_{\mathrm{tissue}} \\[1ex]
\mathrm{LI}_{\mathrm{\_hmgcoasynthase}} &= 1 \cdot \mathrm{Vli}_{\mathrm{tissue}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr}} &= 0.1 \cdot \mathrm{Vli}_{\mathrm{tissue}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}} &= 0.1 \cdot \mathrm{Vli}_{\mathrm{tissue}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_degraded}} &= 0 \cdot \mathrm{Vli}_{\mathrm{tissue}}
\end{aligned}
$$

The assignment rules hold at every time $t$:

$$
\begin{aligned}
f_{\mathrm{shunts}} &= f_{\mathrm{cirrhosis}} \\[1ex]
f_{\mathrm{tissue\_loss}} &= f_{\mathrm{cirrhosis}} \\[1ex]
\mathrm{FVre} &= 1 - \mathrm{FVgi} - \mathrm{FVki} - \mathrm{FVli} \\
&\quad {} - \mathrm{FVlu} - \mathrm{FVve} - \mathrm{FVar} \\[1ex]
\mathrm{FQre} &= 1 - \mathrm{FQki} - \mathrm{FQh} \\[1ex]
\mathrm{BSA} &= 0.024265 \cdot \mathopen{}\left(\frac{\mathrm{BW}}{1}\right)^{0.5378} \cdot \mathopen{}\left(\frac{\mathrm{HEIGHT}}{1}\right)^{0.3964} \\[1ex]
\mathrm{CO} &= \mathrm{BW} \cdot \mathrm{COBW} + \frac{\mathopen{}\left(\mathrm{HR} - \mathrm{HRrest}\right) \cdot \mathrm{COHRI}}{60} \\[1ex]
\mathrm{QC} &= \frac{\mathrm{CO}}{1000} \cdot 60 \\[1ex]
\mathrm{Vgu} &= \mathrm{BW} \cdot \mathrm{FVgi} \\[1ex]
\mathrm{Vgulumen} &= f_{\mathrm{lumen}} \cdot \mathrm{Vgu} \\[1ex]
\mathrm{Vki} &= \mathrm{BW} \cdot \mathrm{FVki} \\[1ex]
\mathrm{Vli} &= \mathrm{BW} \cdot \mathrm{FVli} \\[1ex]
\mathrm{Vlu} &= \mathrm{BW} \cdot \mathrm{FVlu} \\[1ex]
\mathrm{Vre} &= \mathrm{BW} \cdot \mathrm{FVre} \\[1ex]
\mathrm{Vve} &= \mathrm{BW} \cdot \mathrm{FVve} - \frac{\mathrm{FVve}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Var} &= \mathrm{BW} \cdot \mathrm{FVar} - \frac{\mathrm{FVar}}{\mathrm{FVar} + \mathrm{FVve}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVve} - \mathrm{FVar}\right) \\[1ex]
\mathrm{Vpo} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVpo} - \frac{\mathrm{FVpo}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Vhv} &= \mathopen{}\left(1 - \mathrm{HCT}\right) \cdot \mathopen{}\left(\mathrm{BW} \cdot \mathrm{FVhv} - \frac{\mathrm{FVhv}}{\mathrm{FVar} + \mathrm{FVve} + \mathrm{FVpo} + \mathrm{FVhv}} \cdot \mathrm{BW} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{FVar} - \mathrm{FVve} - \mathrm{FVpo} - \mathrm{FVhv}\right)\right) \\[1ex]
\mathrm{Qgu} &= \mathrm{QC} \cdot \mathrm{FQgu} \\[1ex]
\mathrm{Qki} &= \mathrm{QC} \cdot \mathrm{FQki} \\[1ex]
\mathrm{Qh} &= \mathrm{QC} \cdot \mathrm{FQh} \\[1ex]
\mathrm{Qha} &= \mathrm{Qh} - \mathrm{Qgu} \\[1ex]
\mathrm{Qlu} &= \mathrm{QC} \cdot \mathrm{FQlu} \\[1ex]
\mathrm{Qre} &= \mathrm{QC} \cdot \mathrm{FQre} \\[1ex]
\mathrm{Qpo} &= \mathrm{Qgu} \\[1ex]
\mathrm{GFR}_{\mathrm{base}} &= f_{\mathrm{GFR\_Qki}} \cdot \mathrm{Qki} \\[1ex]
\mathrm{Vgu}_{\mathrm{plasma}} &= \mathrm{Vgu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vgu}_{\mathrm{tissue}} &= \mathrm{Vgu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vki}_{\mathrm{plasma}} &= \mathrm{Vki} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vki}_{\mathrm{tissue}} &= \mathrm{Vki} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{plasma}} &= \mathrm{Vli} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vli}_{\mathrm{tissue}} &= \mathrm{Vli} \cdot \mathopen{}\left(1 - f_{\mathrm{tissue\_loss}}\right) \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{plasma}} &= \mathrm{Vlu} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vlu}_{\mathrm{tissue}} &= \mathrm{Vlu} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{plasma}} &= \mathrm{Vre} \cdot \mathrm{Fblood} \cdot \mathopen{}\left(1 - \mathrm{HCT}\right) \\[1ex]
\mathrm{Vre}_{\mathrm{tissue}} &= \mathrm{Vre} \cdot \mathopen{}\left(1 - \mathrm{Fblood}\right) \\[1ex]
\mathrm{Ki}_{\mathrm{pra}} &= \frac{0.693}{\mathrm{ti}_{\mathrm{pra}}} \cdot 60 \\[1ex]
\mathrm{Agu}_{\mathrm{plasma\_pra}} &= \mathrm{Cgu}_{\mathrm{plasma\_pra}} \cdot \mathrm{Vgu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xgu}_{\mathrm{plasma\_pra}} &= \mathrm{Agu}_{\mathrm{plasma\_pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Mgu}_{\mathrm{plasma\_pra}} &= \frac{\mathrm{Agu}_{\mathrm{plasma\_pra}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Aki}_{\mathrm{plasma\_pra}} &= \mathrm{Cki}_{\mathrm{plasma\_pra}} \cdot \mathrm{Vki}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xki}_{\mathrm{plasma\_pra}} &= \mathrm{Aki}_{\mathrm{plasma\_pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Mki}_{\mathrm{plasma\_pra}} &= \frac{\mathrm{Aki}_{\mathrm{plasma\_pra}}}{\mathrm{Vki}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Ali}_{\mathrm{plasma\_pra}} &= \mathrm{Cli}_{\mathrm{plasma\_pra}} \cdot \mathrm{Vli}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xli}_{\mathrm{plasma\_pra}} &= \mathrm{Ali}_{\mathrm{plasma\_pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Mli}_{\mathrm{plasma\_pra}} &= \frac{\mathrm{Ali}_{\mathrm{plasma\_pra}}}{\mathrm{Vli}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Alu}_{\mathrm{plasma\_pra}} &= \mathrm{Clu}_{\mathrm{plasma\_pra}} \cdot \mathrm{Vlu}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xlu}_{\mathrm{plasma\_pra}} &= \mathrm{Alu}_{\mathrm{plasma\_pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Mlu}_{\mathrm{plasma\_pra}} &= \frac{\mathrm{Alu}_{\mathrm{plasma\_pra}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Are}_{\mathrm{plasma\_pra}} &= \mathrm{Cre}_{\mathrm{plasma\_pra}} \cdot \mathrm{Vre}_{\mathrm{plasma}} \\[1ex]
\mathrm{Xre}_{\mathrm{plasma\_pra}} &= \mathrm{Are}_{\mathrm{plasma\_pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Mre}_{\mathrm{plasma\_pra}} &= \frac{\mathrm{Are}_{\mathrm{plasma\_pra}}}{\mathrm{Vre}_{\mathrm{plasma}}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Aar}_{\mathrm{pra}} &= \mathrm{Car}_{\mathrm{pra}} \cdot \mathrm{Var} \\[1ex]
\mathrm{Xar}_{\mathrm{pra}} &= \mathrm{Aar}_{\mathrm{pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Mar}_{\mathrm{pra}} &= \frac{\mathrm{Aar}_{\mathrm{pra}}}{\mathrm{Var}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Ave}_{\mathrm{pra}} &= \mathrm{Cve}_{\mathrm{pra}} \cdot \mathrm{Vve} \\[1ex]
\mathrm{Xve}_{\mathrm{pra}} &= \mathrm{Ave}_{\mathrm{pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Mve}_{\mathrm{pra}} &= \frac{\mathrm{Ave}_{\mathrm{pra}}}{\mathrm{Vve}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Apo}_{\mathrm{pra}} &= \mathrm{Cpo}_{\mathrm{pra}} \cdot \mathrm{Vpo} \\[1ex]
\mathrm{Xpo}_{\mathrm{pra}} &= \mathrm{Apo}_{\mathrm{pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Mpo}_{\mathrm{pra}} &= \frac{\mathrm{Apo}_{\mathrm{pra}}}{\mathrm{Vpo}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Ahv}_{\mathrm{pra}} &= \mathrm{Chv}_{\mathrm{pra}} \cdot \mathrm{Vhv} \\[1ex]
\mathrm{Xhv}_{\mathrm{pra}} &= \mathrm{Ahv}_{\mathrm{pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Mhv}_{\mathrm{pra}} &= \frac{\mathrm{Ahv}_{\mathrm{pra}}}{\mathrm{Vhv}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Xurine}_{\mathrm{pra}} &= \mathrm{Aurine}_{\mathrm{pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{Xfeces}_{\mathrm{pra}} &= \mathrm{Afeces}_{\mathrm{pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \\[1ex]
\mathrm{ldlc}_{\mathrm{change}} &= \frac{\mathrm{Cve}_{\mathrm{ldlc}} - \mathrm{ldlc}_{\mathrm{init}}}{\mathrm{ldlc}_{\mathrm{init}}} \\[1ex]
v_{\mathrm{cho\_reference}} &= \frac{\frac{v_{\mathrm{cho\_ref}}}{\mathrm{Mr}_{\mathrm{ldlc}}}}{\mathrm{conversion}_{\mathrm{min\_per\_day}}} \\[1ex]
\mathrm{ldlc}_{\mathrm{loss}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{ldlc}_{\mathrm{loss\_k}} \\[1ex]
\mathrm{ldlc}_{\mathrm{diet}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{ldlc}_{\mathrm{diet\_k}} \\[1ex]
\mathrm{ldlc}_{\mathrm{utilization}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{ldlc}_{\mathrm{utilization\_Vmax}} \cdot f_{\mathrm{ldlc\_utilization\_Vmax}} \\[1ex]
v_{\mathrm{ldlc\_utilization}} &= \mathrm{ldlc}_{\mathrm{utilization}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{ldlc\_diet}} &= \mathrm{ldlc}_{\mathrm{diet}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{ldlc\_loss}} &= \mathrm{ldlc}_{\mathrm{loss}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
\mathrm{KI}_{\mathrm{\_GFR}} &= \mathrm{KI}_{\mathrm{\_f\_renal\_function}} \cdot \mathrm{GFR}_{\mathrm{base}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_total}} &= \mathrm{LI}_{\mathrm{\_ldlr}} + \mathrm{LI}_{\mathrm{\_ldlr\_membrane}} + \mathrm{LI}_{\mathrm{\_ldlr\_ldlc}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_fraction}} &= \frac{\mathrm{LI}_{\mathrm{\_ldlr}}}{\mathrm{LI}_{\mathrm{\_ldlr\_total}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_membrane\_fraction}} &= \frac{\mathrm{LI}_{\mathrm{\_ldlr\_membrane}}}{\mathrm{LI}_{\mathrm{\_ldlr\_total}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_ldlr\_ldlc\_fraction}} &= \frac{\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}}{\mathrm{LI}_{\mathrm{\_ldlr\_total}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_cho\_reference}} &= \frac{\frac{v_{\mathrm{cho\_ref}}}{\mathrm{Mr}_{\mathrm{ldlc}}}}{\mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}}} \\[1ex]
\mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax}} &= 0.4 \cdot \mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_reference}} &= \mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{GU}_{\mathrm{\_f\_absorption}} &= 1 + \mathrm{GU}_{\mathrm{\_fed}} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_FED\_f\_absorption}} - 1\right) \\[1ex]
\mathrm{GU}_{\mathrm{\_f\_dissolution}} &= 1 + \mathrm{GU}_{\mathrm{\_fed}} \cdot \mathopen{}\left(\mathrm{GU}_{\mathrm{\_FED\_f\_dissolution}} - 1\right) \\[1ex]
\mathrm{GU}_{\mathrm{\_F\_absorbed}} &= \mathrm{GU}_{\mathrm{\_F\_pra\_abs}} \cdot \mathrm{GU}_{\mathrm{\_f\_OATP2B1}} \cdot \mathrm{GU}_{\mathrm{\_f\_absorption}} \\[1ex]
\mathrm{GU}_{\mathrm{\_absorption}} &= \mathrm{GU}_{\mathrm{\_PRAABS\_k}} \cdot \mathrm{Vgulumen} \cdot \mathrm{Cgulumen}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{ldlc\_net\_consumption}} &= \mathrm{ldlc}_{\mathrm{net\_consumption}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
v_{\mathrm{vldlc\_conversion}} &= \mathrm{vldlc}_{\mathrm{conversion}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{conversion}_{\mathrm{min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_export}} &= v_{\mathrm{LI\_\_VLDLCEXP}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_uptake}} &= v_{\mathrm{LI\_\_LDLRLDLCIMP}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_net\_export\_rate}} &= v_{\mathrm{LI\_\_VLDLCEXP}} - v_{\mathrm{LI\_\_LDLRLDLCIMP}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_net\_export}} &= \mathrm{LI}_{\mathrm{\_v\_net\_export\_rate}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_synthesis}} &= v_{\mathrm{LI\_\_HMGCOAREDUCTASE}} \cdot \mathrm{Mr}_{\mathrm{ldlc}} \cdot \mathrm{LI}_{\mathrm{\_conversion\_min\_per\_day}} \\[1ex]
\mathrm{LI}_{\mathrm{\_v\_liver\_balance}} &= \mathrm{LI}_{\mathrm{\_v\_synthesis}} + \mathrm{LI}_{\mathrm{\_v\_uptake}} - \mathrm{LI}_{\mathrm{\_v\_export}} \\[1ex]
\mathrm{LI}_{\mathrm{\_TURNOVER\_LDLR}} &= v_{\mathrm{LI\_\_SYNTHESIS\_LDLR}} - v_{\mathrm{LI\_\_DEGRADATION\_LDLR}}
\end{aligned}
$$

## Reactions

| Rate | Id | Name | Equation | Modifiers |
| --- | --- | --- | --- | --- |
| $v_{\mathrm{transport\_lu\_pra}}$ | `transport_lu_pra` | transport pravastatin | $\mathrm{Clu}_{\mathrm{plasma\_pra}} \rightleftharpoons \mathrm{Clu}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{transport\_re\_pra}}$ | `transport_re_pra` | transport pravastatin | $\mathrm{Cre}_{\mathrm{plasma\_pra}} \rightleftharpoons \mathrm{Cre}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{deep\_re\_pra}}$ | `deep_re_pra` | deep distribution pravastatin (tissue) | $\mathrm{Cre}_{\mathrm{pra}} \rightleftharpoons \mathrm{Cre}_{\mathrm{deep\_pra}}$ |  |
| $v_{\mathrm{iv\_pra}}$ | `iv_pra` | iv pravastatin | $\varnothing \longrightarrow \mathrm{Cve}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_pra}}$ | `Flow_ar_gu_pra` | inflow gut pravastatin | $\mathrm{Car}_{\mathrm{pra}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_pra}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_pra}}$ | `Flow_gu_po_pra` | outflow gut pravastatin | $\mathrm{Cgu}_{\mathrm{plasma\_pra}} \longrightarrow \mathrm{Cpo}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_pra}}$ | `Flow_ar_ki_pra` | inflow kidney pravastatin | $\mathrm{Car}_{\mathrm{pra}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_pra}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_pra}}$ | `Flow_ki_ve_pra` | outflow kidney pravastatin | $\mathrm{Cki}_{\mathrm{plasma\_pra}} \longrightarrow \mathrm{Cve}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_pra}}$ | `Flow_arli_li_pra` | arterial inflow liver pravastatin | $\mathrm{Car}_{\mathrm{pra}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_pra}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_pra}}$ | `Flow_arli_hv_pra` | flow arterial shunts | $\mathrm{Car}_{\mathrm{pra}} \longrightarrow \mathrm{Chv}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_pra}}$ | `Flow_po_li_pra` | outflow po pravastatin | $\mathrm{Cpo}_{\mathrm{pra}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_pra}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_pra}}$ | `Flow_po_hv_pra` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{pra}} \longrightarrow \mathrm{Chv}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_pra}}$ | `Flow_li_hv_pra` | outflow liver pravastatin | $\mathrm{Cli}_{\mathrm{plasma\_pra}} \longrightarrow \mathrm{Chv}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_pra}}$ | `Flow_hv_ve_pra` | outflow hepatic vein pravastatin | $\mathrm{Chv}_{\mathrm{pra}} \longrightarrow \mathrm{Cve}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_pra}}$ | `Flow_ve_lu_pra` | inflow lung pravastatin | $\mathrm{Cve}_{\mathrm{pra}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_pra}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_pra}}$ | `Flow_lu_ar_pra` | outflow lung pravastatin | $\mathrm{Clu}_{\mathrm{plasma\_pra}} \longrightarrow \mathrm{Car}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_pra}}$ | `Flow_ar_re_pra` | inflow rest pravastatin | $\mathrm{Car}_{\mathrm{pra}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_pra}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_pra}}$ | `Flow_re_ve_pra` | outflow rest pravastatin | $\mathrm{Cre}_{\mathrm{plasma\_pra}} \longrightarrow \mathrm{Cve}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_ldlc}}$ | `Flow_ar_gu_ldlc` | inflow gut ldl-cholesterol | $\mathrm{Car}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_ldlc}}$ | `Flow_gu_po_ldlc` | outflow gut ldl-cholesterol | $\mathrm{Cgu}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Cpo}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_ldlc}}$ | `Flow_ar_ki_ldlc` | inflow kidney ldl-cholesterol | $\mathrm{Car}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_ldlc}}$ | `Flow_ki_ve_ldlc` | outflow kidney ldl-cholesterol | $\mathrm{Cki}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_ldlc}}$ | `Flow_arli_li_ldlc` | arterial inflow liver ldl-cholesterol | $\mathrm{Car}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_ldlc}}$ | `Flow_arli_hv_ldlc` | flow arterial shunts | $\mathrm{Car}_{\mathrm{ldlc}} \longrightarrow \mathrm{Chv}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_ldlc}}$ | `Flow_po_li_ldlc` | outflow po ldl-cholesterol | $\mathrm{Cpo}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_ldlc}}$ | `Flow_po_hv_ldlc` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{ldlc}} \longrightarrow \mathrm{Chv}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_ldlc}}$ | `Flow_li_hv_ldlc` | outflow liver ldl-cholesterol | $\mathrm{Cli}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Chv}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_ldlc}}$ | `Flow_hv_ve_ldlc` | outflow hepatic vein ldl-cholesterol | $\mathrm{Chv}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_ldlc}}$ | `Flow_ve_lu_ldlc` | inflow lung ldl-cholesterol | $\mathrm{Cve}_{\mathrm{ldlc}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_ldlc}}$ | `Flow_lu_ar_ldlc` | outflow lung ldl-cholesterol | $\mathrm{Clu}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Car}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_ldlc}}$ | `Flow_ar_re_ldlc` | inflow rest ldl-cholesterol | $\mathrm{Car}_{\mathrm{ldlc}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_ldlc}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_ldlc}}$ | `Flow_re_ve_ldlc` | outflow rest ldl-cholesterol | $\mathrm{Cre}_{\mathrm{plasma\_ldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_gu\_vldlc}}$ | `Flow_ar_gu_vldlc` | inflow gut vldl-cholesterol | $\mathrm{Car}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_gu\_po\_vldlc}}$ | `Flow_gu_po_vldlc` | outflow gut vldl-cholesterol | $\mathrm{Cgu}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Cpo}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_ki\_vldlc}}$ | `Flow_ar_ki_vldlc` | inflow kidney vldl-cholesterol | $\mathrm{Car}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cki}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_ki\_ve\_vldlc}}$ | `Flow_ki_ve_vldlc` | outflow kidney vldl-cholesterol | $\mathrm{Cki}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_arli\_li\_vldlc}}$ | `Flow_arli_li_vldlc` | arterial inflow liver vldl-cholesterol | $\mathrm{Car}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_arli\_hv\_vldlc}}$ | `Flow_arli_hv_vldlc` | flow arterial shunts | $\mathrm{Car}_{\mathrm{vldlc}} \longrightarrow \mathrm{Chv}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_po\_li\_vldlc}}$ | `Flow_po_li_vldlc` | outflow po vldl-cholesterol | $\mathrm{Cpo}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_po\_hv\_vldlc}}$ | `Flow_po_hv_vldlc` | flow portal shunts | $\mathrm{Cpo}_{\mathrm{vldlc}} \longrightarrow \mathrm{Chv}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_li\_hv\_vldlc}}$ | `Flow_li_hv_vldlc` | outflow liver vldl-cholesterol | $\mathrm{Cli}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Chv}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_hv\_ve\_vldlc}}$ | `Flow_hv_ve_vldlc` | outflow hepatic vein vldl-cholesterol | $\mathrm{Chv}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_ve\_lu\_vldlc}}$ | `Flow_ve_lu_vldlc` | inflow lung vldl-cholesterol | $\mathrm{Cve}_{\mathrm{vldlc}} \longrightarrow \mathrm{Clu}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_lu\_ar\_vldlc}}$ | `Flow_lu_ar_vldlc` | outflow lung vldl-cholesterol | $\mathrm{Clu}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Car}_{\mathrm{vldlc}}$ |  |
| $v_{\mathrm{Flow\_ar\_re\_vldlc}}$ | `Flow_ar_re_vldlc` | inflow rest vldl-cholesterol | $\mathrm{Car}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cre}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{Flow\_re\_ve\_vldlc}}$ | `Flow_re_ve_vldlc` | outflow rest vldl-cholesterol | $\mathrm{Cre}_{\mathrm{plasma\_vldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{vldlc}}$ |  |
| $\mathrm{ldlc}_{\mathrm{net\_consumption}}$ | `ldlc_net_consumption` | whole-body net consumption of plasma LDL-C | $\mathrm{Cve}_{\mathrm{ldlc}} \longrightarrow \varnothing$ |  |
| $\mathrm{vldlc}_{\mathrm{conversion}}$ | `vldlc_conversion` | VLDL-C to LDL-C conversion | $\mathrm{Cve}_{\mathrm{vldlc}} \longrightarrow \mathrm{Cve}_{\mathrm{ldlc}}$ |  |
| $v_{\mathrm{KI\_\_PRAEX}}$ | `KI__PRAEX` | excretion pravastatin | $\mathrm{Cki}_{\mathrm{plasma\_pra}} \longrightarrow \mathrm{Aurine}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{LI\_\_PRAIM}}$ | `LI__PRAIM` | pravastatin import (OATP1B1) | $\mathrm{Cli}_{\mathrm{plasma\_pra}} \longrightarrow \mathrm{LI}_{\mathrm{\_pra}}$ |  |
| $v_{\mathrm{LI\_\_PRAEX}}$ | `LI__PRAEX` | pravastatin bile export (MRP2) | $\mathrm{LI}_{\mathrm{\_pra}} \longrightarrow \mathrm{Cgulumen}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{LI\_\_VLDLCEXP}}$ | `LI__VLDLCEXP` | VLDL-cholesterol export | $\mathrm{LI}_{\mathrm{\_cho}} \longrightarrow \mathrm{Cli}_{\mathrm{plasma\_vldlc}}$ |  |
| $v_{\mathrm{LI\_\_LDLRLDLCIMP}}$ | `LI__LDLRLDLCIMP` | LDLR-LDLC binding &amp; internalization | $\mathrm{Cli}_{\mathrm{plasma\_ldlc}} + \mathrm{LI}_{\mathrm{\_ldlr\_membrane}} \longrightarrow \mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}$ | $\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}$ |
| $v_{\mathrm{LI\_\_LDLR\_TO\_MEMBRANE}}$ | `LI__LDLR_TO_MEMBRANE` | LDLR membrane transport | $\mathrm{LI}_{\mathrm{\_ldlr}} \rightleftharpoons \mathrm{LI}_{\mathrm{\_ldlr\_membrane}}$ |  |
| $v_{\mathrm{LI\_\_LDLRRECYCLING}}$ | `LI__LDLRRECYCLING` | LDLR recycling | $\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}} \longrightarrow \mathrm{LI}_{\mathrm{\_ldlr}} + \mathrm{LI}_{\mathrm{\_cho}}$ |  |
| $v_{\mathrm{LI\_\_HMGCOASYNTHASE}}$ | `LI__HMGCOASYNTHASE` | HMG-CoA synthase | $3 \, \mathrm{LI}_{\mathrm{\_acoa}} \longrightarrow \mathrm{LI}_{\mathrm{\_hmgcoa}}$ | $\mathrm{LI}_{\mathrm{\_hmgcoasynthase}}, \mathrm{LI}_{\mathrm{\_hmgcoa}}$ |
| $v_{\mathrm{LI\_\_HMGCOAREDUCTASE}}$ | `LI__HMGCOAREDUCTASE` | HMG-CoA reductase | $6 \, \mathrm{LI}_{\mathrm{\_hmgcoa}} \longrightarrow \mathrm{LI}_{\mathrm{\_cho}}$ | $\mathrm{LI}_{\mathrm{\_pra}}, \mathrm{LI}_{\mathrm{\_hmgcoareductase}}$ |
| $v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOAREDUCTASE}}$ | `LI__SYNTHESIS_HMGCOAREDUCTASE` | HMGCOAREDUCTASE synthesis | $\varnothing \longrightarrow \mathrm{LI}_{\mathrm{\_hmgcoareductase}}$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_DEGRADATION\_HMGCOAREDUCTASE}}$ | `LI__DEGRADATION_HMGCOAREDUCTASE` | HMGCOAREDUCTASE degradation | $\mathrm{LI}_{\mathrm{\_hmgcoareductase}} \longrightarrow \varnothing$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOASYNTHASE}}$ | `LI__SYNTHESIS_HMGCOASYNTHASE` | HMGCOASYNTHASE synthesis | $\varnothing \longrightarrow \mathrm{LI}_{\mathrm{\_hmgcoasynthase}}$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_DEGRADATION\_HMGCOASYNTHASE}}$ | `LI__DEGRADATION_HMGCOASYNTHASE` | HMGCOASYNTHASE degradation | $\mathrm{LI}_{\mathrm{\_hmgcoasynthase}} \longrightarrow \varnothing$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_SYNTHESIS\_LDLR}}$ | `LI__SYNTHESIS_LDLR` | LDLR synthesis | $\varnothing \longrightarrow \mathrm{LI}_{\mathrm{\_ldlr}}$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{LI\_\_DEGRADATION\_LDLR}}$ | `LI__DEGRADATION_LDLR` | LDLR degradation | $\mathrm{LI}_{\mathrm{\_ldlr}} \longrightarrow \mathrm{LI}_{\mathrm{\_ldlr\_degraded}}$ | $\mathrm{LI}_{\mathrm{\_cho}}$ |
| $v_{\mathrm{GU\_\_PRAABS}}$ | `GU__PRAABS` | absorption pravastatin (OATP2B1) | $\mathrm{Cgulumen}_{\mathrm{pra}} \longrightarrow \mathrm{Cgu}_{\mathrm{plasma\_pra}}$ |  |
| $v_{\mathrm{GU\_\_PRAEXC}}$ | `GU__PRAEXC` | excretion pravastatin (feces) | $\mathrm{Cgulumen}_{\mathrm{pra}} \longrightarrow \mathrm{Afeces}_{\mathrm{pra}}$ |  |
| $v_{\mathrm{GU\_\_application\_pra}}$ | `GU__application_pra` | PO application pravastatin | $\varnothing \longrightarrow \mathrm{GU}_{\mathrm{\_pra\_stomach}}$ |  |
| $v_{\mathrm{GU\_\_dissolution\_pra}}$ | `GU__dissolution_pra` | dissolution pravastatin | $\mathrm{GU}_{\mathrm{\_pra\_stomach}} \longrightarrow \mathrm{Cgulumen}_{\mathrm{pra}}$ |  |

The rates of the reactions are:

$$
\begin{aligned}
v_{\mathrm{transport\_lu\_pra}} &= \frac{\mathrm{ftissue}_{\mathrm{pra}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Clu}_{\mathrm{plasma\_pra}} \cdot \mathrm{Kp}_{\mathrm{pra}} - \mathrm{Clu}_{\mathrm{pra}}\right) \\[1ex]
v_{\mathrm{transport\_re\_pra}} &= \frac{\mathrm{ftissue}_{\mathrm{pra}} \cdot \mathrm{BW}}{\mathrm{BW}_{\mathrm{ref}}} \cdot \mathopen{}\left(\mathrm{Cre}_{\mathrm{plasma\_pra}} \cdot \mathrm{Kp}_{\mathrm{pra}} - \mathrm{Cre}_{\mathrm{pra}}\right) \\[1ex]
v_{\mathrm{deep\_re\_pra}} &= \mathrm{kdeep}_{\mathrm{pra}} \cdot \mathrm{Vre}_{\mathrm{tissue}} \cdot \mathopen{}\left(\mathrm{Kpdeep}_{\mathrm{pra}} \cdot \mathrm{Cre}_{\mathrm{pra}} - \mathrm{Cre}_{\mathrm{deep\_pra}}\right) \\[1ex]
v_{\mathrm{iv\_pra}} &= \frac{\mathrm{Ki}_{\mathrm{pra}} \cdot \mathrm{IVDOSE}_{\mathrm{pra}}}{\mathrm{Mr}_{\mathrm{pra}}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_pra}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_pra}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_pra}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_pra}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_pra}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_pra}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_pra}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_pra}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_pra}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_pra}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_pra}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_pra}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_pra}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_pra}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_pra}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_pra}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_pra}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{pra}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_pra}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_pra}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_ldlc}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_ldlc}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_ldlc}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_ldlc}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_ldlc}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_ldlc}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_ldlc}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_ldlc}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_ldlc}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_ldlc}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_ldlc}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_ldlc}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_ldlc}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{ldlc}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_ldlc}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_ldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_gu\_vldlc}} &= \mathrm{Qgu} \cdot \mathrm{Car}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_gu\_po\_vldlc}} &= \mathrm{Qgu} \cdot \mathrm{Cgu}_{\mathrm{plasma\_vldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_ki\_vldlc}} &= \mathrm{Qki} \cdot \mathrm{Car}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_ki\_ve\_vldlc}} &= \mathrm{Qki} \cdot \mathrm{Cki}_{\mathrm{plasma\_vldlc}} \\[1ex]
v_{\mathrm{Flow\_arli\_li\_vldlc}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_arli\_hv\_vldlc}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qha} \cdot \mathrm{Car}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_po\_li\_vldlc}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_po\_hv\_vldlc}} &= f_{\mathrm{shunts}} \cdot \mathrm{Qpo} \cdot \mathrm{Cpo}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_li\_hv\_vldlc}} &= \mathopen{}\left(1 - f_{\mathrm{shunts}}\right) \cdot \mathopen{}\left(\mathrm{Qpo} + \mathrm{Qha}\right) \cdot \mathrm{Cli}_{\mathrm{plasma\_vldlc}} \\[1ex]
v_{\mathrm{Flow\_hv\_ve\_vldlc}} &= \mathrm{Qh} \cdot \mathrm{Chv}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_ve\_lu\_vldlc}} &= \mathrm{Qlu} \cdot \mathrm{Cve}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_lu\_ar\_vldlc}} &= \mathrm{Qlu} \cdot \mathrm{Clu}_{\mathrm{plasma\_vldlc}} \\[1ex]
v_{\mathrm{Flow\_ar\_re\_vldlc}} &= \mathrm{Qre} \cdot \mathrm{Car}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{Flow\_re\_ve\_vldlc}} &= \mathrm{Qre} \cdot \mathrm{Cre}_{\mathrm{plasma\_vldlc}} \\[1ex]
\mathrm{ldlc}_{\mathrm{net\_consumption}} &= \mathopen{}\left(\mathrm{ldlc}_{\mathrm{utilization}} + \mathrm{ldlc}_{\mathrm{loss}}\right) \cdot \mathopen{}\left(1 + \frac{\mathrm{Cve}_{\mathrm{ldlc}}}{\mathrm{ldlc}_{\mathrm{consumption\_Km}}}\right) - \mathrm{ldlc}_{\mathrm{diet}} \\[1ex]
\mathrm{vldlc}_{\mathrm{conversion}} &= v_{\mathrm{cho\_reference}} \cdot \mathrm{vldlc}_{\mathrm{conversion\_k}} \cdot \mathrm{Cve}_{\mathrm{vldlc}} \\[1ex]
v_{\mathrm{KI\_\_PRAEX}} &= \mathrm{KI}_{\mathrm{\_GFR}} \cdot 0.001 \cdot \mathrm{fu}_{\mathrm{pra}} \cdot \mathopen{}\left(1 + \mathrm{KI}_{\mathrm{\_f\_OAT3}} \cdot \mathopen{}\left(\mathrm{KI}_{\mathrm{\_PRAEX\_f}} - 1\right)\right) \cdot \mathrm{Cki}_{\mathrm{plasma\_pra}} \\[1ex]
v_{\mathrm{LI\_\_PRAIM}} &= \frac{\mathrm{LI}_{\mathrm{\_f\_OATP1B1}} \cdot \mathrm{LI}_{\mathrm{\_PRAIM\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{Cli}_{\mathrm{plasma\_pra}}}{\mathrm{Cli}_{\mathrm{plasma\_pra}} + \mathrm{LI}_{\mathrm{\_PRAIM\_Km\_pra}}} \\[1ex]
v_{\mathrm{LI\_\_PRAEX}} &= \mathrm{LI}_{\mathrm{\_f\_MRP2}} \cdot \mathrm{LI}_{\mathrm{\_PRAEX\_k}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_pra}} \\[1ex]
v_{\mathrm{LI\_\_VLDLCEXP}} &= \frac{\mathrm{LI}_{\mathrm{\_VLDLCEXP\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_cho}} + \mathrm{LI}_{\mathrm{\_VLDLCEXP\_Km\_cho}}} \\[1ex]
v_{\mathrm{LI\_\_LDLRLDLCIMP}} &= \frac{\frac{\mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Kcat\_f}} \cdot \mathrm{LI}_{\mathrm{\_ldlr\_membrane}} \cdot \mathrm{Cli}_{\mathrm{plasma\_ldlc}}}{\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Km}} \cdot \mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Km\_f}} + \mathrm{Cli}_{\mathrm{plasma\_ldlc}}} \cdot 1}{1 + \frac{\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}}{\mathrm{LI}_{\mathrm{\_LDLRLDLCIMP\_Ki\_ldlr\_ldlc}}}} \\[1ex]
v_{\mathrm{LI\_\_LDLR\_TO\_MEMBRANE}} &= \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Kcat\_f}} \cdot \mathopen{}\left(\mathrm{LI}_{\mathrm{\_ldlr}} - \frac{\mathrm{LI}_{\mathrm{\_ldlr\_membrane}}}{\mathrm{LI}_{\mathrm{\_LDLRMEMBRANE\_Keq}}}\right) \\[1ex]
v_{\mathrm{LI\_\_LDLRRECYCLING}} &= \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_LDLRRECYCLING\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_LDLRRECYCLING\_Kcat\_f}} \cdot \mathrm{LI}_{\mathrm{\_ldlr\_ldlc}} \\[1ex]
v_{\mathrm{LI\_\_HMGCOASYNTHASE}} &= \frac{\mathrm{LI}_{\mathrm{\_HMGCOASYNTHASE\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoasynthase}} \cdot \mathrm{LI}_{\mathrm{\_acoa}}}{1 + \frac{\mathrm{LI}_{\mathrm{\_hmgcoa}}}{\mathrm{LI}_{\mathrm{\_HMGCOASYNTHASE\_Ki\_hmgcoa}}}} \\[1ex]
v_{\mathrm{LI\_\_HMGCOAREDUCTASE}} &= \frac{\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Kcat}} \cdot \mathrm{LI}_{\mathrm{\_v\_cho\_reference}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoareductase}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoa}}}{\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Km}} \cdot \mathopen{}\left(1 + \frac{\mathrm{LI}_{\mathrm{\_pra}} \cdot \mathrm{pra}_{\mathrm{inhibitor\_activity}}}{\mathrm{LI}_{\mathrm{\_HMGCOAREDUCTASE\_Ki\_pra}}}\right) + \mathrm{LI}_{\mathrm{\_hmgcoa}}} \\[1ex]
v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOAREDUCTASE}} &= \frac{\mathrm{LI}_{\mathrm{\_SYNTHESIS\_HMG\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}}}{1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}}} \\[1ex]
v_{\mathrm{LI\_\_DEGRADATION\_HMGCOAREDUCTASE}} &= \mathrm{LI}_{\mathrm{\_DEGRADATION\_HMG\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoareductase}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}}\right) \\[1ex]
v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOASYNTHASE}} &= \frac{\mathrm{LI}_{\mathrm{\_SYNTHESIS\_HMG\_Vmax}} \cdot \mathrm{Vli}_{\mathrm{tissue}}}{1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}}} \\[1ex]
v_{\mathrm{LI\_\_DEGRADATION\_HMGCOASYNTHASE}} &= \mathrm{LI}_{\mathrm{\_DEGRADATION\_HMG\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_hmgcoasynthase}} \cdot \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathopen{}\left(1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_HMG\_kr\_cho}}}\right) \\[1ex]
v_{\mathrm{LI\_\_SYNTHESIS\_LDLR}} &= \frac{\mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_SYNTHESIS\_LDLR\_Vmax\_f}}}{1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_LDLR\_kr\_cho}}}} \\[1ex]
v_{\mathrm{LI\_\_DEGRADATION\_LDLR}} &= \mathrm{Vli}_{\mathrm{tissue}} \cdot \mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax}} \cdot \mathrm{LI}_{\mathrm{\_DEGRADATION\_LDLR\_Vmax\_f}} \cdot \mathrm{LI}_{\mathrm{\_ldlr}} \cdot \mathopen{}\left(1 + \frac{\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{LI}_{\mathrm{\_LDLR\_kr\_cho}}}\right) \\[1ex]
v_{\mathrm{GU\_\_PRAABS}} &= \mathrm{GU}_{\mathrm{\_F\_absorbed}} \cdot \mathrm{GU}_{\mathrm{\_absorption}} \\[1ex]
v_{\mathrm{GU\_\_PRAEXC}} &= \mathopen{}\left(1 - \mathrm{GU}_{\mathrm{\_F\_absorbed}}\right) \cdot \mathrm{GU}_{\mathrm{\_absorption}} \\[1ex]
v_{\mathrm{GU\_\_application\_pra}} &= \frac{\frac{\mathrm{GU}_{\mathrm{\_Ka\_application\_pra}}}{60} \cdot \mathrm{PODOSE}_{\mathrm{pra}}}{\mathrm{Mr}_{\mathrm{pra}}} \\[1ex]
v_{\mathrm{GU\_\_dissolution\_pra}} &= \frac{\frac{\mathrm{GU}_{\mathrm{\_f\_dissolution}} \cdot \mathrm{GU}_{\mathrm{\_Ka\_dis\_pra}}}{60} \cdot \mathrm{GU}_{\mathrm{\_POSTOMACH\_pra}}}{\mathrm{Mr}_{\mathrm{pra}}}
\end{aligned}
$$

## ODE system

The states change in time with the rates of the reactions and the rate rules:

$$
\begin{aligned}
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_pra}} - v_{\mathrm{Flow\_gu\_po\_pra}} + v_{\mathrm{GU\_\_PRAABS}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_pra}} - v_{\mathrm{Flow\_ki\_ve\_pra}} - v_{\mathrm{KI\_\_PRAEX}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_pra}} + v_{\mathrm{Flow\_po\_li\_pra}} - v_{\mathrm{Flow\_li\_hv\_pra}} - v_{\mathrm{LI\_\_PRAIM}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_pra}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_lu\_pra}} + v_{\mathrm{Flow\_ve\_lu\_pra}} - v_{\mathrm{Flow\_lu\_ar\_pra}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_pra}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{transport\_re\_pra}} + v_{\mathrm{Flow\_ar\_re\_pra}} - v_{\mathrm{Flow\_re\_ve\_pra}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{pra}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_gu\_pra}} - v_{\mathrm{Flow\_ar\_ki\_pra}} - v_{\mathrm{Flow\_arli\_li\_pra}} - v_{\mathrm{Flow\_arli\_hv\_pra}} \\
&\quad {} + v_{\mathrm{Flow\_lu\_ar\_pra}} - v_{\mathrm{Flow\_ar\_re\_pra}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{pra}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{iv\_pra}} + v_{\mathrm{Flow\_ki\_ve\_pra}} + v_{\mathrm{Flow\_hv\_ve\_pra}} - v_{\mathrm{Flow\_ve\_lu\_pra}} \\
&\quad {} + v_{\mathrm{Flow\_re\_ve\_pra}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_pra}} - v_{\mathrm{Flow\_po\_li\_pra}} - v_{\mathrm{Flow\_po\_hv\_pra}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_pra}} + v_{\mathrm{Flow\_po\_hv\_pra}} + v_{\mathrm{Flow\_li\_hv\_pra}} - v_{\mathrm{Flow\_hv\_ve\_pra}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_lu\_pra}}}{\mathrm{Vlu}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{transport\_re\_pra}} - v_{\mathrm{deep\_re\_pra}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{deep\_pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{deep\_re\_pra}}}{\mathrm{Vre}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Aurine}_{\mathrm{pra}}}{\mathrm{d} t} &= v_{\mathrm{KI\_\_PRAEX}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Afeces}_{\mathrm{pra}}}{\mathrm{d} t} &= v_{\mathrm{GU\_\_PRAEXC}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgulumen}_{\mathrm{pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_PRAEX}} - v_{\mathrm{GU\_\_PRAABS}} - v_{\mathrm{GU\_\_PRAEXC}} + v_{\mathrm{GU\_\_dissolution\_pra}}}{\mathrm{Vgulumen}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_ldlc}} - v_{\mathrm{Flow\_gu\_po\_ldlc}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_ldlc}} - v_{\mathrm{Flow\_ki\_ve\_ldlc}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_ldlc}} + v_{\mathrm{Flow\_po\_li\_ldlc}} - v_{\mathrm{Flow\_li\_hv\_ldlc}} - v_{\mathrm{LI\_\_LDLRLDLCIMP}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ve\_lu\_ldlc}} - v_{\mathrm{Flow\_lu\_ar\_ldlc}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_re\_ldlc}} - v_{\mathrm{Flow\_re\_ve\_ldlc}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_gu\_ldlc}} - v_{\mathrm{Flow\_ar\_ki\_ldlc}} - v_{\mathrm{Flow\_arli\_li\_ldlc}} - v_{\mathrm{Flow\_arli\_hv\_ldlc}} \\
&\quad {} + v_{\mathrm{Flow\_lu\_ar\_ldlc}} - v_{\mathrm{Flow\_ar\_re\_ldlc}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{Flow\_ki\_ve\_ldlc}} + v_{\mathrm{Flow\_hv\_ve\_ldlc}} - v_{\mathrm{Flow\_ve\_lu\_ldlc}} + v_{\mathrm{Flow\_re\_ve\_ldlc}} \\
&\quad {} - \mathrm{ldlc}_{\mathrm{net\_consumption}} + \mathrm{vldlc}_{\mathrm{conversion}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_ldlc}} - v_{\mathrm{Flow\_po\_li\_ldlc}} - v_{\mathrm{Flow\_po\_hv\_ldlc}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{ldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_ldlc}} + v_{\mathrm{Flow\_po\_hv\_ldlc}} + v_{\mathrm{Flow\_li\_hv\_ldlc}} - v_{\mathrm{Flow\_hv\_ve\_ldlc}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cgu}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_gu\_vldlc}} - v_{\mathrm{Flow\_gu\_po\_vldlc}}}{\mathrm{Vgu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cki}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_ki\_vldlc}} - v_{\mathrm{Flow\_ki\_ve\_vldlc}}}{\mathrm{Vki}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cli}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_li\_vldlc}} + v_{\mathrm{Flow\_po\_li\_vldlc}} - v_{\mathrm{Flow\_li\_hv\_vldlc}} + v_{\mathrm{LI\_\_VLDLCEXP}}}{\mathrm{Vli}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Clu}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ve\_lu\_vldlc}} - v_{\mathrm{Flow\_lu\_ar\_vldlc}}}{\mathrm{Vlu}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cre}_{\mathrm{plasma\_vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_ar\_re\_vldlc}} - v_{\mathrm{Flow\_re\_ve\_vldlc}}}{\mathrm{Vre}_{\mathrm{plasma}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Car}_{\mathrm{vldlc}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Var}} \Bigl( -v_{\mathrm{Flow\_ar\_gu\_vldlc}} - v_{\mathrm{Flow\_ar\_ki\_vldlc}} - v_{\mathrm{Flow\_arli\_li\_vldlc}} - v_{\mathrm{Flow\_arli\_hv\_vldlc}} \\
&\quad {} + v_{\mathrm{Flow\_lu\_ar\_vldlc}} - v_{\mathrm{Flow\_ar\_re\_vldlc}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cve}_{\mathrm{vldlc}}}{\mathrm{d} t} &= \frac{1}{\mathrm{Vve}} \Bigl( v_{\mathrm{Flow\_ki\_ve\_vldlc}} + v_{\mathrm{Flow\_hv\_ve\_vldlc}} - v_{\mathrm{Flow\_ve\_lu\_vldlc}} + v_{\mathrm{Flow\_re\_ve\_vldlc}} \\
&\quad {} - \mathrm{vldlc}_{\mathrm{conversion}} \Bigr) \\[1ex]
\frac{\mathrm{d} \,\mathrm{Cpo}_{\mathrm{vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_gu\_po\_vldlc}} - v_{\mathrm{Flow\_po\_li\_vldlc}} - v_{\mathrm{Flow\_po\_hv\_vldlc}}}{\mathrm{Vpo}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{Chv}_{\mathrm{vldlc}}}{\mathrm{d} t} &= \frac{v_{\mathrm{Flow\_arli\_hv\_vldlc}} + v_{\mathrm{Flow\_po\_hv\_vldlc}} + v_{\mathrm{Flow\_li\_hv\_vldlc}} - v_{\mathrm{Flow\_hv\_ve\_vldlc}}}{\mathrm{Vhv}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_pra}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_PRAIM}} - v_{\mathrm{LI\_\_PRAEX}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_hmgcoa}}}{\mathrm{d} t} &= \frac{v_{\mathrm{LI\_\_HMGCOASYNTHASE}} - 6 \cdot v_{\mathrm{LI\_\_HMGCOAREDUCTASE}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_cho}}}{\mathrm{d} t} &= \frac{-v_{\mathrm{LI\_\_VLDLCEXP}} + v_{\mathrm{LI\_\_LDLRRECYCLING}} + v_{\mathrm{LI\_\_HMGCOAREDUCTASE}}}{\mathrm{Vli}_{\mathrm{tissue}}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_hmgcoareductase}}}{\mathrm{d} t} &= \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOAREDUCTASE}} - \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_DEGRADATION\_HMGCOAREDUCTASE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_hmgcoasynthase}}}{\mathrm{d} t} &= \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_SYNTHESIS\_HMGCOASYNTHASE}} - \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_DEGRADATION\_HMGCOASYNTHASE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_ldlr}}}{\mathrm{d} t} &= -\mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLR\_TO\_MEMBRANE}} + \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLRRECYCLING}} + \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_SYNTHESIS\_LDLR}} - \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_DEGRADATION\_LDLR}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_ldlr\_membrane}}}{\mathrm{d} t} &= -\mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLRLDLCIMP}} + \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLR\_TO\_MEMBRANE}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_ldlr\_ldlc}}}{\mathrm{d} t} &= \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLRLDLCIMP}} - \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_LDLRRECYCLING}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{LI}_{\mathrm{\_ldlr\_degraded}}}{\mathrm{d} t} &= \mathrm{LI}_{\mathrm{\_cf\_units\_per\_mmole}} \cdot v_{\mathrm{LI\_\_DEGRADATION\_LDLR}} \\[1ex]
\frac{\mathrm{d} \,\mathrm{IVDOSE}_{\mathrm{pra}}}{\mathrm{d} t} &= -v_{\mathrm{iv\_pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} + \mathrm{Ri}_{\mathrm{pra}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{cum}_{\mathrm{dose\_pra}}}{\mathrm{d} t} &= \mathrm{Ri}_{\mathrm{pra}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{PODOSE}_{\mathrm{pra}}}{\mathrm{d} t} &= -v_{\mathrm{GU\_\_application\_pra}} \cdot \mathrm{Mr}_{\mathrm{pra}} \qquad \text{(rate rule)} \\[1ex]
\frac{\mathrm{d} \,\mathrm{GU}_{\mathrm{\_POSTOMACH\_pra}}}{\mathrm{d} t} &= \mathopen{}\left(v_{\mathrm{GU\_\_application\_pra}} - v_{\mathrm{GU\_\_dissolution\_pra}}\right) \cdot \mathrm{Mr}_{\mathrm{pra}} \qquad \text{(rate rule)}
\end{aligned}
$$
