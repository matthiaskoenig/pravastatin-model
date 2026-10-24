"""LDL-C plasma calibration.

The baseline LDL-C reference value was adjusted using the LDL-C utilization.
"""

import logging
from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.scan import single_dimension
from sbmlsim import Q
from sbmlsim.simulation import Dimension, Scan, Simulation
from scipy.interpolate import CubicSpline

from pkdb_models.models.pravastatin.experiments.base_experiment import (
    FontKwargs,
    PravastatinCholesterolSimulationExperiment,
)
from pkdb_models.models.pravastatin.experiments.model_calibration.readout_dict_FH_scans import (
    time_FH_steadystate,
)

logger = logging.getLogger(__name__)


class LDLCUtilizationCalibration(PravastatinCholesterolSimulationExperiment):
    """Varying LDL-C utilization to adjust plasma LDL-C levels.

    The value of `ldlc_utilization_Vmax` of the reference plasma LDL-C (3 mM)
    is interpolated from the plasma LDL-C in steady state of the scan; the
    figure shows it, and it is logged.
    """

    #: the time to the steady state [weeks]
    time_FH_steadystate: ClassVar[int] = time_FH_steadystate
    #: the output steps of the last day of the steady state
    steps_last_day: ClassVar[int] = 100
    #: the values of `ldlc_utilization_Vmax` of the scan
    change_factors: ClassVar[np.ndarray] = np.linspace(0.5, 1, num=25)

    @override
    def simulations(self) -> dict[str, Scan]:
        return {
            **self.simulation_cho(),
        }

    def simulation_cho(self) -> dict[str, Scan]:
        """Scan of the LDL-C utilization into the steady state."""
        tcscans = {}
        # steady state, the last day with a finer output
        times = self.steady_state_times(
            weeks=self.time_FH_steadystate, last_day_steps=self.steps_last_day
        )
        tcscans["ldlc_utilization_vmax_scan"] = Scan(
            simulation=Simulation(
                start=0,
                end=times[-1],
                times=times,
                preinit_changes=self.default_changes(),
            ),
            dimensions=[
                Dimension(
                    "dim_fh",
                    values={
                        "ldlc_utilization_Vmax": Q(self.change_factors, "dimensionless")
                    },
                )
            ],
        )
        return tcscans

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {**self.figure_mpl1()}

    def figure_mpl1(self) -> dict[str, FigureMPL]:
        """Timecourses of the scan and the plasma LDL-C in steady state."""
        task_id = "task_ldlc_utilization_vmax_scan"
        xres = self.results[task_id]
        # a row per simulation of the scan
        ldlc_data = xres["[Cve_ldlc]"].transpose(single_dimension(xres), "time").values

        # spline interpolation
        change_factors = list(reversed(self.change_factors))
        ss_ldlcs = list(reversed([ldlc[-1] for ldlc in ldlc_data]))
        cs = CubicSpline(ss_ldlcs, change_factors)

        # figure timecourse
        label_kwargs: FontKwargs = {"weight": "bold", "size": 20}
        fig_tc, ax_tc = plt.subplots(
            nrows=1,
            ncols=1,
            figsize=(9, 6),
        )
        ax_tc.set_ylabel("Plasma LDL-C [mM]", **label_kwargs)
        ax_tc.set_xlabel("Time [min]", **label_kwargs)
        for single_dim_data in ldlc_data:
            ax_tc.plot(
                xres.quantity("time").magnitude,
                single_dim_data,
                color="black",
                linestyle="solid",
            )

        # figure scan
        fig_scan, ax_scan = plt.subplots(
            nrows=1,
            ncols=1,
            figsize=(9, 6),
        )
        ax_scan.set_ylabel("Plasma LDL-C [mM]", **label_kwargs)
        ax_scan.set_xlabel(
            "LDL-C utilization\n(ldlc_utilization_Vmax) [-]", **label_kwargs
        )

        # plot interpolation
        test_ldlcs = np.linspace(ss_ldlcs[0], ss_ldlcs[-1], num=50)
        ax_scan.plot(
            cs(test_ldlcs),
            test_ldlcs,
            label="Interpolation",
            color="tab:blue",
            linestyle="solid",
        )

        # plot simulations
        ax_scan.plot(
            change_factors,
            ss_ldlcs,
            markeredgecolor="black",
            markerfacecolor="#070D0D",
            marker="o",
            label="Simulation",
            linestyle="None",
        )

        # plot reference point
        ax_scan.axvline(x=cs(3), color="black")
        ax_scan.axhline(y=3, color="black")
        ax_scan.plot(
            [cs(3)],
            [3],
            markerfacecolor="tab:red",
            markeredgecolor="black",
            marker="o",
            label="Reference",
            linestyle="None",
            markersize=10,
        )
        ax_scan.set_ylim(0, 6.1)
        ax_scan.set_xlim(0.48)

        shaded_area_color = "grey"
        shaded_area_alpha = 0.2
        ax_scan.fill(
            [0.48, cs(3), cs(3), 0.48],
            [0, 0, 6.1, 6.1],
            shaded_area_color,
            alpha=shaded_area_alpha,
            edgecolor="None",
        )

        ax_scan.legend()
        ax_scan.grid()

        logger.info(
            "Calibrated 'ldlc_utilization_Vmax' of the plasma LDL-C 3 mM: %s "
            "dimensionless",
            cs(3),
        )
        return {"ldlc_calibration_timecourse": fig_tc, "ldlc_calibration": fig_scan}
