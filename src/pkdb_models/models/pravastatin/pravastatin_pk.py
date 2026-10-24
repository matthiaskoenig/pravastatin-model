"""Pharmacokinetic parameters of pravastatin.

The pharmacokinetic parameters are the non-compartmental analysis of
`pkpdutils`, named like the variables of its `NCAResult` (e.g. `auc_last`,
`auc_inf_obs`, `cmax`, `tmax`, `thalf`, `lambda_z`, `cl_f`, `vz_f`), with the
unit of every parameter in `<name>_unit`, of pravastatin in venous plasma
(`[Cve_pra]`). The dose is the oral (`PODOSE_pra`) or the intravenous dose
(`IVDOSE_pra`) at the start of the simulation, the route the one of the dose
which is given; the clearance and the volume are the apparent ones (`cl_f`,
`vz_f`) after an oral dose and the true ones after an intravenous dose. The
concentrations below `LLOQ_FRACTION` of the maximum are below the limit of
quantification, so that the noise of the integrator is not the terminal phase.

Besides the analysis, the fraction of the dose excreted unchanged in the urine
until the end of the simulation is `fe_urine`, the renal clearance
(`cl_renal`) that amount over `auc_last`, and after an intravenous dose the
nonrenal clearance (`cl_nonrenal`) the total clearance minus the renal
clearance (after an oral dose the apparent clearance contains the
bioavailability, so it has no nonrenal part).

The parameters are calculated for every point of a scan of one dimension or for
the result of a single simulation; a run over the draws of the fitted
parameters (`run_simulation pkdb_models.models.pravastatin --uncertainty`) adds
the dimension of the draws, a row per point with its position along each
dimension (the columns `point` and, with draws, `draw`); `summarize` gives the
median and the quantiles of a parameter over the draws of every point.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from pkpdsim.pk import nca_frame
from pkpdsim.scan import end_values, scan_dimensions, start_values
from pkpdutils import Route, Timecourses, nca, ureg
from sbmlsim import Q
from sbmlsim.result import ScanResult
from sbmlsim.units import Quantity

if TYPE_CHECKING:
    from pkdb_models.models.pravastatin.experiments.base_experiment import (
        PravastatinSimulationExperiment,
    )

#: concentration of pravastatin in venous plasma
CONCENTRATION = "[Cve_pra]"
#: oral dose of pravastatin
DOSE_PO = "PODOSE_pra"
#: intravenous dose of pravastatin
DOSE_IV = "IVDOSE_pra"
#: cumulative amount of pravastatin in the urine
URINE = "Aurine_pra"
#: the limit of quantification relative to the maximal concentration
LLOQ_FRACTION = 1e-4


def pk_parameters(
    experiment: PravastatinSimulationExperiment,
    xres: ScanResult,
    normalization_dose: Quantity | None = None,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of pravastatin in every simulation of a result.

    The non-compartmental analysis of all simulations with a dose of one route
    at once (a batch of `pkpdutils`, the timecourses with the state after a
    change at its time and without the padding of a ragged result); the dose
    is the oral or intravenous dose at the start, the amount in the urine the
    one at the end.

    Args:
        experiment: experiment of the simulations, for the molecular weight.
        xres: result of the simulation or of the scan, of any number of
            dimensions.
        normalization_dose: the concentrations and amounts are normalized to
            this dose, which is the dose of the analysis, e.g. to compare the
            parameters of different doses.

    Returns:
        One row per simulation (in the order of the dimensions of the result),
        with its position along every dimension (a column named after the
        dimension), the dose (`dose`), its route (`route`) and the parameters
        with their units (`<name>_unit`).

    Raises:
        ValueError: if a simulation has no dose or an oral and an intravenous
            dose at once.
    """
    units = xres.units
    dose_po = Q(start_values(xres, DOSE_PO).values, units[DOSE_PO])
    dose_iv = Q(start_values(xres, DOSE_IV).values, units[DOSE_IV])
    oral = dose_po.magnitude > 0
    invalid = oral == (dose_iv.magnitude > 0)
    if invalid.any():
        index = np.unravel_index(np.flatnonzero(invalid)[0], invalid.shape)
        po, iv = (Q(d.magnitude[index], d.units) for d in [dose_po, dose_iv])
        raise ValueError(
            "The analysis needs either an oral or an intravenous dose, not "
            f"'{po}' and '{iv}'."
        )
    dose = Q(
        np.where(oral, dose_po.magnitude, dose_iv.to(dose_po.units).magnitude),
        dose_po.units,
    )
    urine = Q(end_values(xres, URINE).values, units[URINE])
    dose_analysis = dose
    factor = None
    if normalization_dose is not None:
        factor = (normalization_dose / dose).to("dimensionless").magnitude
        urine = urine * factor
        dose_analysis = normalization_dose
    # the dose in the substance unit of the concentration, which `cl_f` and
    # `vz_f` require
    amount = np.broadcast_to(
        (dose_analysis / experiment.Mr.pra).to("mmole").magnitude, oral.shape
    )
    routes = np.full(oral.shape, None, dtype=object)
    routes[oral] = Route.ORAL
    routes[~oral] = Route.IV_BOLUS
    # an analysis per route (in the order of the first simulation of a route),
    # of which the simulations of the route are taken
    labels = routes.ravel()
    frames = []
    for route in dict.fromkeys(labels):
        timecourses = xres.to_timecourses(
            CONCENTRATION,
            dose={"amount": amount, "unit": "mmol"},
            route=route,
            substance="pravastatin",
        )
        values = timecourses.ds["value"]
        if factor is not None:
            # the concentrations normalized to the dose of the analysis
            values = values.copy(data=values.values * factor[..., None])
        cmax = values.max(dim=[d for d in values.dims if d not in xres.dims])
        lloq = (LLOQ_FRACTION * cmax).where(cmax > 0)
        result = nca(Timecourses(timecourses.ds.assign(value=values, lloq=lloq)))
        df = nca_frame(result).drop(columns="nca_flags")[labels == route]
        position = tuple(df[dim].to_numpy() for dim in xres.dims)
        dose_mg = dose.to("mg")
        df.insert(len(xres.dims), "dose", dose_mg.magnitude[position])
        df.insert(len(xres.dims) + 1, "dose_unit", str(dose_mg.units))
        df.insert(len(xres.dims) + 2, "route", str(route.value))
        # the amounts in the unit registry of the analysis
        urine_pk = ureg.Quantity(urine.to("mmole").magnitude[position], "mmol")
        auc_last = ureg.Quantity(df["auc_last"].to_numpy(), df["auc_last_unit"].iloc[0])
        excretion = {
            "fe_urine": (urine_pk / ureg.Quantity(amount[position], "mmol")).to(
                "dimensionless"
            ),
            "cl_renal": (urine_pk / auc_last).to("l/min"),
        }
        if route == Route.IV_BOLUS:
            # the total clearance of an intravenous dose is `cl`
            cl = ureg.Quantity(df["cl"].to_numpy(), df["cl_unit"].iloc[0])
            excretion["cl_nonrenal"] = (cl - excretion["cl_renal"]).to("l/min")
        for key, value in excretion.items():
            df[key] = value.magnitude
            df[f"{key}_unit"] = str(value.units)
        frames.append(df)
    return pd.concat(frames).sort_index()


def calculate_pravastatin_pk(
    experiment: PravastatinSimulationExperiment,
    xres: ScanResult,
    normalization_dose: Quantity | None = None,
    across: str | None = None,
) -> pd.DataFrame:
    """Calculate the pharmacokinetic parameters of every simulation of a result.

    Args:
        experiment: experiment of the simulations, for the molecular weight.
        xres: result of a scan of one dimension or of a single simulation,
            with the dimension of the draws `across`.
        normalization_dose: the parameters are normalized to this dose, see
            `pk_parameters`.
        across: the dimension of the draws of the fitted parameters, `None`
            for a result without draws.

    Returns:
        One row per simulation, in the order of the scan (and of the draws),
        with its position (`point`, `draw`).

    Raises:
        ValueError: if the result has more than one dimension besides the
            draws.
    """
    dims = scan_dimensions(xres, across)
    if len(dims) > 1:
        raise ValueError(
            f"A scan of one dimension is required, not of {dims} (draws: {across})."
        )
    df = pk_parameters(experiment, xres, normalization_dose=normalization_dose)
    names = {
        **({dims[0]: "point"} if dims else {}),
        **({across: "draw"} if across is not None else {}),
    }
    df = df.rename(columns=names)
    if not dims:
        df.insert(0, "point", 0)
    return df


def summarize(
    df: pd.DataFrame, key: str, quantiles: tuple[float, float] | None = None
) -> pd.DataFrame:
    """Get the median and the quantiles of a parameter over the draws of every point.

    Args:
        df: the parameters with the column `point` and, in a run over the
            draws, `draw` (`calculate_pravastatin_pk`).
        key: the parameter.
        quantiles: the lower and the upper quantile, `None` for parameters
            without draws: the lower and the upper are the value.

    Returns:
        One row per point (the index, in the order of the scan), the columns
        `lower`, `median`, `upper`.
    """
    grouped = df.groupby("point")[key]
    if quantiles is None or "draw" not in df:
        values = grouped.median()
        return pd.DataFrame(
            {"lower": values, "median": values, "upper": values}
        ).astype(np.float64)
    low, high = quantiles
    return pd.DataFrame(
        {
            "lower": grouped.quantile(low),
            "median": grouped.median(),
            "upper": grouped.quantile(high),
        }
    ).astype(np.float64)
