"""Base classes of the pravastatin simulation experiments.

`PravastatinSimulationExperiment` simulates the pravastatin model,
`PravastatinCholesterolSimulationExperiment` the model of pravastatin and the
cholesterol.
"""

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import ClassVar, NamedTuple, TypedDict, override

import numpy as np
import pandas as pd
from pkpdsim.experiment import PKPDSimulationExperiment
from pkpdsim.impairment import RENAL_COLORS_END_STAGE, RENAL_FUNCTION_GFR
from pkpdsim.scan import point_band, point_timecourse, scan_dimensions, start_values
from pkpdsim.uncertainty import UncertaintyRun
from sbmlsim import Q
from sbmlsim.model import AbstractModel
from sbmlsim.result import ScanResult
from sbmlsim.units import Quantity

from pkdb_models.models.pravastatin import MODEL, MODEL_PATH_CHOLESTEROL
from pkdb_models.models.pravastatin.pravastatin_pk import (
    calculate_pravastatin_pk,
    summarize,
)

# the activity of OATP1B1 (`LI__f_OATP1B1`) of the SLCO1B1 alleles; the 521C
# allele (*5, *15, *17) lowers it: the pooled 521C/C and *15/*15 AUC ratio is
# about 2 (Niemi2006, Ho2007, Deng2008), which the adopted PK gives with an
# activity of 0.22 of the 521C/C genotype (the mean of its two alleles); the
# heterozygous genotypes (activity 0.61) get an AUC ratio of 1.3
F_SLCO1B1_WILDTYPE = 1.0
F_SLCO1B1_1B = 1.1
F_SLCO1B1_521C = 0.22

# The interactions are simulated with factors of the transporters, never
# fitted; the factors reproduce the observed ratios with the adopted PK
# (PK_20261019_164944__7b050).
#: gemfibrozil 600 mg b.i.d. (Kyrklund2003a): gemfibrozil and its glucuronide
#: inhibit OATP1B1 and the renal secretion by OAT3; the renal clearance falls
#: to 0.57 and the AUC rises 2.02 fold
F_OAT3_GEMFIBROZIL = 0.39
F_OATP1B1_GEMFIBROZIL = 0.52
#: rifampicin 600 mg daily for 5 days, pravastatin 17 hr after the last dose
#: (Kyrklund2004): the induction of OATP1B1 lowers the AUC to 0.69, the renal
#: clearance and the half-life are unchanged
F_OATP1B1_RIFAMPICIN = 1.7
#: quercetin 500 mg daily for 14 days, the last 1 hr before pravastatin
#: (Wu2012): inhibition of OATP1B1 (in vitro IC50 about 16 µM), AUC ratio 1.24
F_OATP1B1_QUERCETIN = 0.70
#: clarithromycin 500 mg b.i.d. (Jacobson2004 trial 4): inhibition of
#: OATP1B1/1B3 (Seithel2007), AUC ratio 2.10 and Cmax ratio 2.28
F_OATP1B1_CLARITHROMYCIN = 0.18
#: no interaction with pravastatin, which is not metabolized by CYP3A4:
#: itraconazole (Neuvonen1998, AUC ratio 1.71, not significant), St John's wort
#: (Sugimoto2001, 1.03), fenofibrate (Pan2000, 1.13-1.31), verapamil and
#: mibefradil (Jacobson2004, 1.31 and 1.20, not significant); their arms are
#: simulated as the control
F_NO_INTERACTION = 1.0


class FontKwargs(TypedDict):
    """Font of the labels of the matplotlib figures, keyword arguments of `Axes.set_xlabel`."""

    weight: str
    size: int


class ScanSpec(TypedDict):
    """Definition of the scan of a parameter."""

    parameter: str
    range: np.ndarray
    units: str
    label: str


class MolecularWeights(NamedTuple):
    """Molecular weights of the substances."""

    #: pravastatin (the acid), the substance of the model and of the data
    pra: Quantity
    #: pravastatin sodium, the salt of the tablets and solutions: a dose of
    #: the salt is the dose of the model `dose * Mr.pra / Mr.pra_na`
    pra_na: Quantity


class PravastatinSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the simulation experiments of the pravastatin model.

    The experiments change no parameter of every simulation (`default_changes`
    of the base). A dose of pravastatin sodium is converted to the acid
    (`Mr.pra / Mr.pra_na`), the renal function of a measured creatinine
    clearance of X ml/min is `X/101` (`renal_map`), a meal is `GU__fed` 1 and
    an interaction the factors of the transporters of this module.
    """

    pkpd_model = MODEL
    selections = (
        "time",
        "IVDOSE_pra",
        "PODOSE_pra",
        "[Cve_pra]",
        "[Car_pra]",
        "[Cgulumen_pra]",
        "Aurine_pra",
        "Afeces_pra",
        "[LI__pra]",
        "KI__GFR",
        # f factors
        "KI__f_renal_function",
        "KI__f_OAT3",
        "f_cirrhosis",
        "LI__f_MRP2",
        "LI__f_OATP1B1",
        "GU__f_OATP2B1",
        "GU__fed",
    )

    # the renal function by the limits of the classes of the GFR, relative to
    # the healthy GFR of 101 ml/min of the model
    renal_map = RENAL_FUNCTION_GFR
    renal_colors = RENAL_COLORS_END_STAGE

    font: ClassVar[dict[str, str | int]] = {"weight": "bold", "size": 18}
    tick_font_size: ClassVar[int] = 15
    legend_font_size: ClassVar[int] = 13

    suptitle_font_size: ClassVar[int] = 40
    #: the opacity of the bands of the draws of the fitted parameters in a run
    #: over them (`run_simulation pkdb_models.models.pravastatin --uncertainty`)
    band_alpha: ClassVar[float] = 0.2

    units: ClassVar[Mapping[str, str]] = {
        "time": "hr",
        "[Cve_pra]": "µM",
        "Cve_pra": "µmol",
        "Aurine_pra": "µmole",
        "Afeces_pra": "µmole",
        "[LI__pra]": "nM",
        "[Car_pra]": "µM",
        "[Cgulumen_pra]": "µM",
        "KI__GFR": "ml/min",
    }
    labels: ClassVar[Mapping[str, str]] = {
        "[Cve_pra]": "pravastatin plasma\n",
        "Aurine_pra": "pravastatin urine\n",
        "Afeces_pra": "pravastatin feces\n",
        "[LI__pra]": "pravastatin liver\n",
        "[Car_pra]": "pravastatin arterial\n",
        "[Cgulumen_pra]": "pravastatin intestinal lumen\n",
        "KI__GFR": "GFR\n",
    }
    label_pra: ClassVar[str] = "pravastatin"
    label_pra_urine: ClassVar[str] = "pravastatin urine"
    label_pra_feces: ClassVar[str] = "pravastatin feces"
    label_time: ClassVar[str] = "time"

    # the activity of OATP1B1 of the SLCO1B1 genotypes, the mean of the alleles
    slco1b1_map: ClassVar[dict[str, float]] = {
        # strong increase (dark blue)
        "*1b/*1b": (F_SLCO1B1_1B + F_SLCO1B1_1B) / 2,
        # mild increase (light blue)
        "(*1a+1b)/*1b": ((F_SLCO1B1_WILDTYPE + F_SLCO1B1_1B) / 2 + F_SLCO1B1_1B) / 2,
        "*1a/*1b": (F_SLCO1B1_WILDTYPE + F_SLCO1B1_1B) / 2,
        # wildtype (black)
        "*1a/*1a": (F_SLCO1B1_WILDTYPE + F_SLCO1B1_WILDTYPE) / 2,
        "521T/T": (F_SLCO1B1_WILDTYPE + F_SLCO1B1_WILDTYPE) / 2,
        # minor decrease (orange)
        "*1b/*15": (F_SLCO1B1_1B + F_SLCO1B1_521C) / 2,
        "*1b/*16": (F_SLCO1B1_1B + F_SLCO1B1_521C) / 2,
        # mild decrease (red)
        "521T/C": (F_SLCO1B1_WILDTYPE + F_SLCO1B1_521C) / 2,
        "*1a/*5": (F_SLCO1B1_WILDTYPE + F_SLCO1B1_521C) / 2,
        "*1a/*15": (F_SLCO1B1_WILDTYPE + F_SLCO1B1_521C) / 2,
        "*1a/*15b": (F_SLCO1B1_WILDTYPE + F_SLCO1B1_521C) / 2,
        "*1a/*17": (F_SLCO1B1_WILDTYPE + F_SLCO1B1_521C) / 2,
        # strong decrease (dark red)
        "521C/C": (F_SLCO1B1_521C + F_SLCO1B1_521C) / 2,
        "*5/*5": (F_SLCO1B1_521C + F_SLCO1B1_521C) / 2,
        "*15/*15": (F_SLCO1B1_521C + F_SLCO1B1_521C) / 2,
        "*17/*17": (F_SLCO1B1_521C + F_SLCO1B1_521C) / 2,
        "*15b/*15b": (F_SLCO1B1_521C + F_SLCO1B1_521C) / 2,
        "*16/*16": (F_SLCO1B1_521C + F_SLCO1B1_521C) / 2,
    }

    slco1b1_colors: ClassVar[dict[str, str]] = {
        # strong increase (dark blue)
        "*1b/*1b": "blue",
        # mild increase (light blue)
        "(*1a+1b)/*1b": "tab:blue",
        "*1a/*1b": "tab:blue",
        # wildtype (black)
        "*1a/*1a": "black",
        "521T/T": "black",
        # minor decrease (orange)
        "*1b/*15": "tab:orange",
        "*1b/*16": "tab:orange",
        # mild decrease (red)
        "521T/C": "tab:red",
        "*1a/*5": "tab:red",
        "*1a/*15": "tab:red",
        "*1a/*15b": "tab:red",
        "*15b/*15b": "tab:red",
        "*1a/*17": "tab:red",
        "*17/*17": "tab:red",
        # strong decrease (dark red)
        "521C/C": "red",
        "*5/*5": "red",
        "*15/*15": "red",
        "*16/*16": "tab:red",
    }

    # the ABCG2 (BCRP) c.421C>A genotypes (Keskitalo2009): 421A reduces the
    # transport by BCRP, which the model does not have
    abcg2_colors: ClassVar[dict[str, str]] = {
        # wildtype
        "421C/C": "black",
        # heterozygous
        "421C/A": "tab:blue",
        # homozygous
        "421A/A": "tab:red",
    }

    # molecular weights of the substances
    Mr: ClassVar[MolecularWeights] = MolecularWeights(
        pra=Q(424.53, "g/mole"), pra_na=Q(446.5, "g/mole")
    )

    # the pharmacokinetic parameters of `pravastatin_pk`; the scans show the
    # AUC in nmole/l⋅hr and the clearances in l/min
    pk_labels: ClassVar[Mapping[str, str]] = {
        "auc_last": "AUCend",
        "auc_inf_obs": "AUC",
        "cl_f": "Apparent clearance",
        "cl_renal": "Renal clearance",
        "cl_nonrenal": "Nonrenal clearance",
        "fe_urine": "Fraction excreted in urine",
        "cmax": "Cmax",
        "tmax": "tmax",
        "thalf": "Half-life",
        "lambda_z": "Elimination rate",
        "vz_f": "Apparent volume",
    }

    pk_units: ClassVar[Mapping[str, str]] = {
        "auc_last": "nmole/l⋅hr",
        "auc_inf_obs": "µmole/l⋅hr",
        "cl_f": "l/min",
        "cl_renal": "l/min",
        "cl_nonrenal": "l/min",
        "fe_urine": "dimensionless",
        "cmax": "nmole/l",
        "tmax": "hr",
        "thalf": "hr",
        "lambda_z": "1/hr",
        "vz_f": "l",
    }

    def calculate_pravastatin_pk(
        self, scans: Sequence[str] = ()
    ) -> dict[str, pd.DataFrame]:
        """Calculate the pharmacokinetic parameters of simulations (scans).

        Args:
            scans: keys of the simulations, all simulations of the experiment
                if empty.

        Returns:
            The parameters of `pravastatin_pk` by key of the simulation, per
            draw of the fitted parameters in a run over them (`uncertainty`).
        """
        across = None if self.uncertainty is None else self.uncertainty.id
        return {
            sim_key: calculate_pravastatin_pk(
                experiment=self,
                xres=self.results[f"task_{sim_key}"],
                across=across,
            )
            for sim_key in (scans or self._simulations.keys())
        }

    def pk_summary(
        self, df: pd.DataFrame, key: str
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get a pharmacokinetic parameter at the points of a scan.

        Args:
            df: the parameters of the scan (`calculate_pravastatin_pk`).
            key: the parameter.

        Returns:
            The value (the median of the draws in a run over them), the lower
            and the upper quantile of the draws (the value without draws), in
            the unit of the parameter in `df`.
        """
        run = self.uncertainty
        summary = summarize(df, key, None if run is None else run.quantiles)
        return (
            summary["median"].to_numpy(),
            summary["lower"].to_numpy(),
            summary["upper"].to_numpy(),
        )

    def scan_values(self, xres: ScanResult, parameter_id: str) -> Quantity:
        """Get the values of a scanned parameter at the points of a scan of one dimension.

        The values are those of the first draw in a run over the draws of the
        fitted parameters, which do not change them.
        """
        values = start_values(xres, parameter_id)
        run = self.uncertainty
        if run is not None:
            values = values.isel({run.id: 0})
        return Q(values.values, xres.units[parameter_id])

    def scanned_dimension(self, xres: ScanResult) -> str:
        """Get the dimension of a scan of one dimension, besides the draws.

        Raises:
            ValueError: if the scan has not one dimension besides the draws.
        """
        run = self.uncertainty
        dims = scan_dimensions(xres, None if run is None else run.id)
        if len(dims) != 1:
            raise ValueError(f"A scan of one dimension is required, not of {dims}.")
        return dims[0]

    def scan_timecourse(
        self, xres: ScanResult, sid: str, **point: int
    ) -> tuple[Quantity, Quantity, Quantity, Quantity]:
        """Get the timecourse of a point of a scan with the band of its draws.

        Args:
            xres: the result of the scan.
            sid: the variable, converted into its unit of `units`.
            **point: the position of the point along every dimension of the
                scan but the draws.

        Returns:
            The time (in the unit of the time of `units`), the values (the
            median of the draws in a run over them) and the lower and the upper
            quantile of the draws (the values without draws).
        """
        run = self.uncertainty
        if run is None:
            time, values = point_timecourse(xres, sid, **point)
            lower = upper = values
        else:
            time, lower, values, upper = point_band(
                xres, sid, across=run.id, quantiles=run.quantiles, **point
            )

        def convert(v: np.ndarray) -> Quantity:
            """Get the values in the unit of the figures."""
            return Q(v, xres.units[sid]).to(self.units[sid])

        return (
            Q(time, xres.units["time"]).to(self.units["time"]),
            convert(values),
            convert(lower),
            convert(upper),
        )


class PravastatinCholesterolSimulationExperiment(PKPDSimulationExperiment):
    """Base class of the simulation experiments of pravastatin and the cholesterol.

    The experiments change no parameter of every simulation (`default_changes`
    of the base): the fitted values of pravastatin, the initial LDL cholesterol
    for the change of the LDL cholesterol (`ldlc_init`, 3 mM) and the factors of
    the familial hypercholesterolemia types (1), which were the default changes
    of the experiments, are values of the model.
    """

    pkpd_model = MODEL
    selections = (
        "time",
        "IVDOSE_pra",
        "PODOSE_pra",
        "[Cve_pra]",
        "[Car_pra]",
        "[Cgulumen_pra]",
        "Aurine_pra",
        "Afeces_pra",
        "[LI__pra]",
        "LI__PRAIM_Vmax",
        "LI__PRAEX_k",
        "KI__f_renal_function",
        "f_cirrhosis",
        "LI__f_MRP2",
        "LI__f_OATP1B1",
        "GU__f_OATP2B1",
        # cholesterol selections
        "[Cve_ldlc]",
        "[Cve_vldlc]",
        "[LI__cho]",
        "[LI__hmgcoa]",
        "[LI__acoa]",
        "[LI__pra]",
        "ldlc_change",
        "ldlc_init",
        # cholesterol protein expression
        "LI__ldlr",
        "LI__ldlr_membrane",
        "LI__ldlr_ldlc",
        "LI__ldlr_total",
        "LI__ldlr_fraction",
        "LI__ldlr_membrane_fraction",
        "LI__ldlr_ldlc_fraction",
        "[LI__hmgcoareductase]",
        "[LI__hmgcoasynthase]",
        "LI__SYNTHESIS_LDLR",
        "LI__DEGRADATION_LDLR",
        # cholesterol rates
        "LI__TURNOVER_LDLR",
        "LI__LDLR_TO_MEMBRANE",
        "LI__LDLRRECYCLING",
        "LI__LDLRLDLCIMP",
        "LI__VLDLCEXP",
        "LI__HMGCOAREDUCTASE",
        "LI__v_synthesis",
        "LI__v_export",
        "LI__v_uptake",
        "LI__v_liver_balance",
        "LI__v_reference",
        "ldlc_utilization",
        "ldlc_loss",
        "ldlc_diet",
        "ldlc_net_consumption",
        "vldlc_conversion",
        "LI__v_net_export",  # [mg/day]
        "v_ldlc_net_consumption",  # [mg/day]
        "v_ldlc_utilization",  # [mg/day]
        "v_ldlc_loss",  # [mg/day]
        "v_ldlc_diet",  # [mg/day]
        "v_vldlc_conversion",  # [mg/day]
    )

    @property
    @override
    def uncertainty(self) -> UncertaintyRun | None:
        """No draws of the fitted parameters: the experiments run once.

        The fitted parameters are those of the pharmacokinetics of pravastatin
        and the experiments of the cholesterol give no pravastatin, so every
        draw would give the same result; in a run over the draws
        (`run_simulation pkdb_models.models.pravastatin --uncertainty`) they
        run with the fitted values, as without draws.
        """
        return None

    @override
    def models(self) -> dict[str, AbstractModel | Path]:
        return {
            "model": AbstractModel(
                source=MODEL_PATH_CHOLESTEROL,
                language_type=AbstractModel.LanguageType.SBML,
                changes={},
            )
        }

    @staticmethod
    def steady_state_times(
        weeks: int, steps: int = 10, last_day_steps: int = 100
    ) -> list[float]:
        """Output times [min] of a simulation of `weeks` weeks into the steady state.

        The times until the last day have `steps` equidistant steps, the last day
        `last_day_steps`.
        """
        end_steady_state = (weeks * 7 - 1) * 24 * 60
        return [end_steady_state * k / steps for k in range(steps + 1)] + [
            end_steady_state + 24 * 60 * k / last_day_steps
            for k in range(1, last_day_steps + 1)
        ]
