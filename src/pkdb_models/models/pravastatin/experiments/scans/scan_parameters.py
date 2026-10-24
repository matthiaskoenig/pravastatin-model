"""Scans of the renal function and the transporters in cirrhosis."""

from typing import ClassVar, override

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LogNorm
from matplotlib.figure import Figure as FigureMPL
from sbmlsim import Q
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
    ScanSpec,
)


class ParametersScan(PravastatinSimulationExperiment):
    """Scan the effect of renal function and transporters on pravastatin.

    The renal function and the activity of MRP2, OATP1B1 and OATP2B1 are
    scanned in every stage of cirrhosis with normal renal function. In a run
    over the draws of the fitted parameters (`run_simulation
    pkdb_models.models.pravastatin --uncertainty`) every point of a scan is
    simulated for every draw; the figures draw the median of the draws and the
    band of their quantiles for the reference (1.0).
    """

    num_points: ClassVar[int] = 19
    scan_map: ClassVar[dict[str, ScanSpec]] = {
        "renal": {
            "parameter": "KI__f_renal_function",
            "range": np.logspace(-1, 1, num=num_points),
            "units": "dimensionless",
            "label": "Renal function [-]",
        },
        "mrp2": {
            "parameter": "LI__f_MRP2",
            "range": np.logspace(-1, 1, num=num_points),
            "units": "dimensionless",
            "label": "MRP2 (ABCC2) activity [-]",
        },
        "oatp1b1": {
            "parameter": "LI__f_OATP1B1",
            "range": np.logspace(-1, 1, num=num_points),
            "units": "dimensionless",
            "label": "OATP1B1 (SLCO1B1) activity [-]",
        },
        "oatp2b1": {
            "parameter": "GU__f_OATP2B1",
            "range": np.logspace(-1, 1, num=num_points),
            "units": "dimensionless",
            "label": "OATP2B1 (SLCO2B1) activity [-]",
        },
    }

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}

        for scan_key, scan_data in self.scan_map.items():
            for cirrhosis_key in self.cirrhosis_map:
                tcscans[self.to_sid(f"scan_{scan_key}_{cirrhosis_key}")] = Scan(
                    simulation=Simulation(
                        start=0,
                        end=24 * 60,
                        preinit_changes={
                            **self.default_changes(),
                            "PODOSE_pra": Q(20, "mg"),
                            "f_cirrhosis": Q(
                                self.cirrhosis_map[cirrhosis_key], "dimensionless"
                            ),
                        },
                    ),
                    dimensions=[
                        Dimension(
                            "dim_scan",
                            values={
                                scan_data["parameter"]: Q(
                                    scan_data["range"], scan_data["units"]
                                )
                            },
                        ),
                    ],
                )

        return tcscans

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        return {
            **self.figures_mpl_timecourses_cirrhosis(),
        }

    def figures_mpl_timecourses_cirrhosis(self) -> dict[str, FigureMPL]:
        """Timecourse plots for key variables depending on cirrhosis degree.

        A column per degree of cirrhosis with normal renal function.
        """
        sids = [
            "[Cve_pra]",
            "Aurine_pra",
            "[LI__pra]",
            "[Cgulumen_pra]",
            "Afeces_pra",
        ]
        # red less function, blue more function on the logarithmic scale of
        # the scans, the reference 1.0 is black
        cmap = matplotlib.colormaps["seismic_r"]
        figures: dict[str, FigureMPL] = {}
        for scan_key, scan_data in self.scan_map.items():
            f, axes = plt.subplots(
                nrows=len(sids),
                ncols=len(self.cirrhosis_map),
                figsize=(5 * len(self.cirrhosis_map), 5 * len(sids)),
                sharex="col",
                sharey="row",
            )
            f.subplots_adjust(wspace=0.05, hspace=0.05, top=0.94)
            f.suptitle(
                f"Scan {scan_data['label']} in cirrhosis",
                fontsize=self.suptitle_font_size,
            )

            norm = LogNorm(vmin=scan_data["range"].min(), vmax=scan_data["range"].max())
            ymax: dict[str, float] = {}
            for krow, sid in enumerate(sids):
                ymax[sid] = 0.0
                for kcol, cirrhosis_key in enumerate(self.cirrhosis_map):
                    ax = axes[krow, kcol]
                    # get data
                    xres = self.results[
                        self.to_sid(f"task_scan_{scan_key}_{cirrhosis_key}")
                    ]

                    # scanned dimension
                    scandim = self.scanned_dimension(xres)
                    par_vec = self.scan_values(xres, scan_data["parameter"])

                    # plot all curves for the scan
                    facecolor = self.cirrhosis_colors[cirrhosis_key]
                    if facecolor != "black":
                        for axis in ["top", "bottom", "left", "right"]:
                            ax.spines[axis].set_linewidth(4)
                            ax.spines[axis].set_color(facecolor)

                    # the reference (1.0) is drawn last, on top of the others
                    reference: int | None = None
                    for k_par, par in enumerate(par_vec):
                        if np.isclose(1.0, par.magnitude):
                            reference = k_par
                            continue
                        t_vec, c_vec, _, c_upper = self.scan_timecourse(
                            xres, sid, **{scandim: k_par}
                        )
                        ymax[sid] = max(ymax[sid], float(np.max(c_upper.magnitude)))
                        ax.plot(
                            t_vec.magnitude,
                            c_vec.magnitude,
                            color=cmap(norm(par.magnitude)),
                            linewidth=2.0,
                        )

                    if reference is not None:
                        t_vec, c_vec, c_lower, c_upper = self.scan_timecourse(
                            xres, sid, **{scandim: reference}
                        )
                        ymax[sid] = max(ymax[sid], float(np.max(c_upper.magnitude)))
                        # the band of the draws of the reference only, the
                        # bands of all points would cover each other
                        if self.uncertainty is not None:
                            ax.fill_between(
                                t_vec.magnitude,
                                c_lower.magnitude,
                                c_upper.magnitude,
                                color="black",
                                alpha=self.band_alpha,
                                linewidth=0,
                            )
                        ax.plot(
                            t_vec.magnitude,
                            c_vec.magnitude,
                            color="black",
                            linewidth=2.0,
                        )

                    if krow == 0:
                        ax.set_title(
                            cirrhosis_key,
                            fontdict={
                                "fontsize": self.tick_font_size,
                                "fontweight": "bold",
                            },
                        )

                    ax.tick_params(axis="x", labelsize=self.tick_font_size)
                    ax.tick_params(axis="y", labelsize=self.tick_font_size)

                    if krow == len(sids) - 1:
                        ax.set_xlabel(
                            f"{self.label_time} [{self.units['time']}]",
                            fontdict=self.font,
                        )
                    # the simulations are 24 hr
                    ax.set_xticks(np.linspace(0, 24, 5))

                    if kcol == 0:
                        ax.set_ylabel(
                            f"{self.labels[sid]} [{self.units[sid]}]",
                            fontdict=self.font,
                        )
                    ax.set_ylim(bottom=0.0)

            for krow, sid in enumerate(sids):
                for kcol in range(len(self.cirrhosis_map)):
                    # the amount in the bile is zero (the bile is passed on to
                    # the intestine at once), its axis is centered on zero
                    if ymax[sid] > 0:
                        axes[krow, kcol].set_ylim(bottom=0, top=1.05 * ymax[sid])
                    else:
                        axes[krow, kcol].set_ylim(bottom=-1, top=1)

            # add colorbar
            cb_ax = f.add_axes((0.92, 0.2, 0.02, 0.6))
            cbar = f.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cb_ax)
            # the gradient as vector cells: matplotlib rasterizes it into an
            # embedded image, which some SVG viewers do not show; the edges of
            # the cells in their color close the seams between them
            if cbar.solids is not None:
                cbar.solids.set_rasterized(False)
                cbar.solids.set_edgecolor("face")
            cbar.ax.axhline(1.0, color="black", linewidth=3)
            cb_ticks = [0.1, 0.2, 0.5, 1, 2, 5, 10]
            cbar.set_ticks(cb_ticks, labels=[f"{tick:g}" for tick in cb_ticks])
            cbar.ax.minorticks_off()
            cbar.ax.tick_params(labelsize=20)
            cbar.ax.set_ylabel(
                scan_data["label"], rotation=270, size=25, weight="bold", labelpad=30
            )

            figures[f"fig_timecourse_cirrhosis_{scan_key}"] = f
        return figures
