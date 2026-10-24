"""Scans and calibration curves for FH types.

The severity of a familial hypercholesterolemia (FH) type is the factor of the
parameter of the liver which the FH type changes. The scan of the factor gives
the plasma LDL-C in steady state; its interpolation gives the factor of a
plasma LDL-C. `FHCalibration` writes the factors of the plasma LDL-C 0.1 - 31 mM
(the calibration) into the output directory of its run. Nothing reads it since
the cholesterol experiments were removed (see TODO.md).
"""

from copy import deepcopy
from typing import Any, ClassVar, NamedTuple, TypedDict, override

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure as FigureMPL
from pkpdsim.scan import single_dimension
from sbmlsim import Q
from sbmlsim.experiment import ExperimentResult
from sbmlsim.simulation import Dimension, Scan, Simulation
from sbmlsim.simulator import Simulator
from scipy.interpolate import CubicSpline

from pkdb_models.models.pravastatin.experiments.base_experiment import (
    FontKwargs,
    PravastatinCholesterolSimulationExperiment,
)
from pkdb_models.models.pravastatin.experiments.model_calibration.readout_dict_FH_scans import (
    Readout,
    readout_dict,
    time_FH_steadystate,
)


class FHTypeInfo(TypedDict):
    """A FH type: the parameter it changes and its panel of the figure."""

    fh_parameter: str
    title: str
    x_label: str
    label: str
    n_column: int
    #: the factors of the impaired function (shaded), less or greater than 1
    root_cutoff: str


class SteadyStates(NamedTuple):
    """The steady states of the scan of a FH type and their interpolation.

    In the order of increasing plasma LDL-C, which the interpolation needs.
    """

    #: the factors of the parameter of the FH type
    factors: list[float]
    #: the plasma LDL-C in steady state [mM]
    ldlcs: list[float]
    #: the factor of a plasma LDL-C
    interpolation: CubicSpline


class FHCalibration(PravastatinCholesterolSimulationExperiment):
    """Scans and calibration curves for FH types."""

    #: the plasma LDL-C of the calibration [mM]
    ldlc_values: ClassVar[np.ndarray] = np.round(np.linspace(0.1, 31, 310), 1)
    #: the file of the calibration in the output directory of a run
    calibration_file: ClassVar[str] = "FHCalibration_calibration_results.csv"

    #: the time to the steady state of the FH type [weeks]
    time_FH_steadystate: ClassVar[int] = time_FH_steadystate
    #: the factors of the scan of a FH type
    scan_points: ClassVar[int] = 31
    start_log: ClassVar[int] = -3
    stop_log: ClassVar[int] = 3
    mutation_factors: ClassVar[np.ndarray] = np.logspace(
        start=start_log, stop=stop_log, num=scan_points
    )

    readout_dict: ClassVar[dict[str, Readout]] = deepcopy(readout_dict)
    #: the output steps of the last day of the steady state
    steps_last_day: ClassVar[int] = 100

    FH_type_dict: ClassVar[dict[str, FHTypeInfo]] = {
        "FH_type1": {
            "fh_parameter": "LI__SYNTHESIS_LDLR_Vmax_f",
            "title": "FH class 1\nLDLR synthesis",
            "x_label": "Class 1",
            "label": "LDLR synthesis",
            "n_column": 0,
            "root_cutoff": "less 1",
        },
        "FH_type2_6": {
            "fh_parameter": "LI__LDLRMEMBRANE_Kcat_f",
            "title": "FH class 2 & 6\nLDLR membrane transport",
            "label": "LDLR membrane transport",
            "x_label": "Class 2 & 6",
            "n_column": 1,
            "root_cutoff": "less 1",
        },
        "FH_type3": {
            "fh_parameter": "LI__LDLRLDLCIMP_Km_f",
            "title": "FH class 3\nLDLR-LDL binding",
            "label": "LDLR-LDL binding",
            "x_label": "Class 3",
            "n_column": 2,
            "root_cutoff": "greater 1",
        },
        "FH_type4": {
            "fh_parameter": "LI__LDLRLDLCIMP_Kcat_f",
            "title": "FH class 4\nLDLR-LDL internalization",
            "label": "LDLR-LDL internalization",
            "x_label": "Class 4",
            "n_column": 3,
            "root_cutoff": "less 1",
        },
        "FH_type5": {
            "fh_parameter": "LI__LDLRRECYCLING_Kcat_f",
            "title": "FH class 5\nLDLR recycling",
            "label": "LDLR recycling",
            "x_label": "Class 5",
            "n_column": 4,
            "root_cutoff": "less 1",
        },
        "PCSK9": {
            "fh_parameter": "LI__DEGRADATION_LDLR_Vmax_f",
            "title": "PCSK9 mutation\nLDLR degradation",
            "label": "LDLR degradation",
            "x_label": "PCSK9",
            "n_column": 5,
            "root_cutoff": "greater 1",
        },
    }

    @override
    def simulations(self) -> dict[str, Scan]:
        return {
            **self.simulation_cho(),
        }

    def simulation_cho(self) -> dict[str, Scan]:
        """Scan of the factor of every FH type into the steady state."""
        tcscans = {}
        # steady state of the FH type, the last day with a finer output
        times = self.steady_state_times(
            weeks=self.time_FH_steadystate, last_day_steps=self.steps_last_day
        )
        for fh_key, fh_value in self.FH_type_dict.items():
            tcscans[fh_key] = Scan(
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
                            fh_value["fh_parameter"]: Q(
                                self.mutation_factors, "dimensionless"
                            )
                        },
                    )
                ],
            )
        return tcscans

    def steady_states(self) -> dict[str, SteadyStates]:
        """The plasma LDL-C in steady state of the scan of every FH type.

        The plasma LDL-C falls with the factor of the FH types whose impaired
        function is a factor less than 1: their scan is reversed.
        """
        var_info = self.readout_dict["plasma ldlc"]
        steady_states = {}
        for key in self.FH_type_dict:
            xres = self.results[f"task_{key}"]
            factors = self.mutation_factors.tolist()

            # the plasma LDL-C in steady state, the last time of every simulation
            data = (
                xres[var_info["sid"]].transpose(single_dimension(xres), "time").values
            )
            ldlcs = [vec[-1] for vec in data]

            if key in ["FH_type1", "FH_type2_6", "FH_type4", "FH_type5"]:
                ldlcs = list(reversed(ldlcs))
                factors = list(reversed(factors))

            steady_states[key] = SteadyStates(
                factors=factors,
                ldlcs=ldlcs,
                interpolation=CubicSpline(ldlcs, factors),
            )
        return steady_states

    def calibration(self) -> pd.DataFrame:
        """The factor of every FH type for the plasma LDL-C 0.1 - 31 mM.

        Returns:
            The plasma LDL-C (`concentration` [mM]) and the interpolated factor
            of every FH type.
        """
        df = pd.DataFrame({"concentration": self.ldlc_values})
        for key, steady_states in self.steady_states().items():
            df[key] = steady_states.interpolation(df["concentration"])
        return df

    @override
    def run(
        self, simulator: Simulator | None, *args: Any, **kwargs: Any
    ) -> ExperimentResult:
        """Run the experiment and write the calibration with its outputs.

        The arguments are those of `SimulationExperiment.run`, which a runner
        passes by keyword, the figure settings of the run among them. The
        calibration is calculated from the results of the run, which are kept
        for it, and written into the output directory of the run
        (`calibration_file`), never into the model.
        """
        result = super().run(simulator, *args, **{**kwargs, "keep_results": True})
        if result.output_path is not None and result.error is None:
            self.calibration().to_csv(result.output_path / self.calibration_file)
        return result

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {**self.figure_mpl1()}

    def figure_mpl1(self) -> dict[str, FigureMPL]:
        """Plasma LDL-C versus the factor of every FH type and its interpolation."""
        kwargs: FontKwargs = {"weight": "bold", "size": 20}
        title_kwargs: FontKwargs = {"weight": "bold", "size": 24}

        fig, axs_fig = plt.subplots(
            nrows=1, ncols=6, figsize=(38, 6), sharex="col", sharey="row"
        )
        fig.subplots_adjust(
            bottom=0.15,
            top=0.88,
            left=0.05,
            right=0.92,
        )

        steady_states = self.steady_states()
        for key, value in self.FH_type_dict.items():
            n_column = value["n_column"]
            factors, ldlcs, interpolation = steady_states[key]

            axs_fig[n_column].plot(
                interpolation(self.ldlc_values),
                self.ldlc_values,
                label="Interpolation",
                color="tab:blue",
                linestyle="solid",
            )

            # plot results from simulation
            axs_fig[n_column].plot(
                factors,
                ldlcs,
                label="Scan",
                markeredgecolor="black",
                markerfacecolor="#070D0D",
                marker="o",
                linestyle="None",
            )

            # plot reference lines and points
            axs_fig[n_column].axhline(y=3, linestyle="-", color="black")
            axs_fig[n_column].axvline(x=1, linestyle="-", color="black")
            axs_fig[n_column].plot(
                [1],
                [3],
                markerfacecolor="tab:red",
                markeredgecolor="black",
                marker="o",
                linestyle="None",
                label="Reference",
                markersize=10,
            )

            axs_fig[n_column].set_xlim(0.001, 1000)
            axs_fig[n_column].set_ylim(-1, 35)
            axs_fig[n_column].set_xscale("log")
            axs_fig[n_column].grid()
            axs_fig[n_column].tick_params(labelsize=16)

            # set title and some xaxis adjustments
            axs_fig[n_column].set_title(value["title"], **title_kwargs)
            axs_fig[n_column].set_xlabel(f"{value['fh_parameter']} [-]", **kwargs)

        axs_fig[0].set_ylabel("Plasma LDL-C\n[mM]", **kwargs)

        axs_fig[5].legend(
            loc="center left", bbox_to_anchor=(1.03, 0.5), prop={"size": 18}
        )

        # add shaded areas
        shaded_area_color = "grey"
        shaded_area_alpha = 0.2
        # xlim is 0.001, 1000
        # ylim  is -1, 35
        for col in [2, 5]:
            axs_fig[col].fill(
                [1, 1000, 1000, 1],
                [-1, -1, 35, 35],
                shaded_area_color,
                alpha=shaded_area_alpha,
                edgecolor="None",
            )
        for col in [0, 1, 3, 4]:
            axs_fig[col].fill(
                [0.001, 1, 1, 0.001],
                [-1, -1, 35, 35],
                shaded_area_color,
                alpha=shaded_area_alpha,
                edgecolor="None",
            )

        return {"ldlc_calibration": fig}
