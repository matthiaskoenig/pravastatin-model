"""Scan of the cirrhosis in renal impairment."""

from typing import ClassVar, override

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.figure import Figure as FigureMPL
from sbmlsim import Q
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
    ScanSpec,
)


class CirrhosisScan(PravastatinSimulationExperiment):
    """Scan the effect of hepatic function on pravastatin pharmacokinetics."""

    scan_map: ClassVar[dict[str, ScanSpec]] = {
        "hepatic": {
            "parameter": "f_cirrhosis",
            "range": np.linspace(0, 0.9, num=19),
            "units": "dimensionless",
            "label": "Cirrhosis [-]",
        },
    }

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}
        for scan_key, scan_data in self.scan_map.items():
            for renal_key in self.renal_map:
                tcscans[self.to_sid(f"scan_{scan_key}_{renal_key}")] = Scan(
                    simulation=Simulation(
                        start=0,
                        end=24 * 60,
                        preinit_changes={
                            **self.default_changes(),
                            "PODOSE_pra": Q(20, "mg"),
                            "KI__f_renal_function": Q(
                                self.renal_map[renal_key], "dimensionless"
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
            **self.figures_mpl_timecourses(),
        }

    def figures_mpl_timecourses(self) -> dict[str, FigureMPL]:
        """Timecourse plots for key variables depending on the cirrhosis.

        A column per degree of renal impairment.
        """
        sids = [
            "[Cve_pra]",
            "Aurine_pra",
            "[LI__pra]",
            "[Cgulumen_pra]",
            "Afeces_pra",
        ]
        cmap = matplotlib.colormaps["seismic"]
        # the colors of the curves for the colorbar: `seismic` from 0.5 (no
        # cirrhosis) to 0.0 (maximal cirrhosis 0.9)
        cmap_cirrhosis = ListedColormap(cmap(np.linspace(0.5, 0.0, num=256)))
        figures: dict[str, FigureMPL] = {}
        for scan_key, scan_data in self.scan_map.items():
            f, axes = plt.subplots(
                nrows=len(sids),
                ncols=len(self.renal_map),
                figsize=(5 * len(self.renal_map), 5 * len(sids)),
                sharey="row",
                sharex="col",
            )
            f.subplots_adjust(wspace=0.1, hspace=0.1, top=0.94)
            f.suptitle(f"Scan {scan_data['label']}", fontsize=self.suptitle_font_size)

            ymax: dict[str, float] = {}
            for krow, sid in enumerate(sids):
                ymax[sid] = 0.0
                for kcol, renal_key in enumerate(self.renal_map):
                    ax = axes[krow, kcol]
                    # get data
                    xres = self.results[
                        self.to_sid(f"task_scan_{scan_key}_{renal_key}")
                    ]

                    # scanned dimension
                    scandim = self.scanned_dimension(xres)
                    par_vec = self.scan_values(xres, scan_data["parameter"])

                    # plot all curves for the scan
                    facecolor = self.renal_colors[renal_key]
                    if facecolor != "black":
                        for axis in ["top", "bottom", "left", "right"]:
                            ax.spines[axis].set_linewidth(4)
                            ax.spines[axis].set_color(facecolor)

                    for k_par, par in enumerate(par_vec):
                        t_vec, c_vec, c_lower, c_upper = self.scan_timecourse(
                            xres, sid, **{scandim: k_par}
                        )
                        ymax[sid] = max(ymax[sid], float(np.max(c_upper.magnitude)))

                        # 0.0 - 0.9
                        linewidth = 2.0
                        reference = bool(np.isclose(0.0, par.magnitude))
                        if reference:
                            color = "black"
                        else:
                            cvalue = 0.5 - par.magnitude / 0.9 * 0.5
                            color = cmap(cvalue)

                        # the band of the draws of the reference only, the
                        # bands of all points would cover each other
                        if reference and self.uncertainty is not None:
                            ax.fill_between(
                                t_vec.magnitude,
                                c_lower.magnitude,
                                c_upper.magnitude,
                                color=color,
                                alpha=self.band_alpha,
                                linewidth=0,
                            )
                        ax.plot(
                            t_vec.magnitude,
                            c_vec.magnitude,
                            color=color,
                            linewidth=linewidth,
                        )

                    if krow == 0:
                        ax.set_title(
                            renal_key,
                            fontdict={
                                "fontsize": self.tick_font_size,
                                "fontweight": "bold",
                            },
                        )

                    if krow == len(sids) - 1:
                        ax.set_xlabel(
                            f"{self.label_time} [{self.units['time']}]",
                            fontdict=self.font,
                        )

                    ax.tick_params(axis="x", labelsize=self.tick_font_size)
                    ax.tick_params(axis="y", labelsize=self.tick_font_size)

                    if kcol == 0:
                        ax.set_ylabel(
                            f"{self.labels[sid]} [{self.units[sid]}]",
                            fontdict=self.font,
                        )

            for krow, sid in enumerate(sids):
                for kcol in range(len(self.renal_map)):
                    # the amount in the bile is zero (the bile is passed on to
                    # the intestine at once), its axis is centered on zero
                    if ymax[sid] > 0:
                        axes[krow, kcol].set_ylim(bottom=0, top=1.2 * ymax[sid])
                    else:
                        axes[krow, kcol].set_ylim(bottom=-1, top=1)

            # add colorbar of the cirrhosis
            cb_ax = f.add_axes((0.92, 0.2, 0.02, 0.6))
            norm = Normalize(
                vmin=scan_data["range"].min(), vmax=scan_data["range"].max()
            )
            cbar = f.colorbar(ScalarMappable(norm=norm, cmap=cmap_cirrhosis), cax=cb_ax)
            # the gradient as vector cells: matplotlib rasterizes it into an
            # embedded image, which some SVG viewers do not show; the edges of
            # the cells in their color close the seams between them
            if cbar.solids is not None:
                cbar.solids.set_rasterized(False)
                cbar.solids.set_edgecolor("face")
            cbar.set_ticks([0, 0.3, 0.6, 0.9])
            cbar.ax.tick_params(labelsize=20)
            cbar.ax.set_ylabel(
                scan_data["label"], rotation=270, size=25, weight="bold", labelpad=30
            )

            figures[f"fig_timecourse_{scan_key}"] = f
        return figures
