"""Scans of the transporters MRP2 and OATP1B1 compared to the data of the genotypes."""

from typing import ClassVar, TypedDict, override

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.figure import Figure as FigureMPL
from matplotlib.typing import ColorType, MarkerType
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.result import ScanResult
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
    ScanSpec,
)


class DataStyle(TypedDict):
    """A dataset of a genotype in the figures: its label and color."""

    label: str
    color: str


class GenotypeDataStyle(DataStyle):
    """A dataset of a SLCO1B1 genotype: its dose [mg], label, color and marker."""

    dose: int
    marker: MarkerType


class GenotypeScan(PravastatinSimulationExperiment):
    """Scan the effect of genotypes on plasma pravastastatin."""

    # FIXME: BETTER SCANS: "range": np.sort(np.append(np.logspace(-1, 1, num=num_points), [1.0])),  # [10^-1=0.1, 10^1=10]
    scan_map: ClassVar[dict[str, ScanSpec]] = {
        "mrp2": {
            "parameter": "LI__f_MRP2",
            "range": np.linspace(0.2, 1.8, num=9),
            "units": "dimensionless",
            "label": "MRP2 function [-]",
        },
        "oatp1b1": {
            "parameter": "LI__f_OATP1B1",
            "range": np.linspace(0.2, 1.8, num=9),
            "units": "dimensionless",
            "label": "OATP1B1 function [-]",
        },
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}

        # the concentrations of the genotypes (Keskitalo2009, MRP2 variants, is
        # not used)
        for study, fig_id in [
            ("Deng2008", "Fig2"),
            ("Ho2007", "Fig1"),
            ("Maeda2006", "Fig1AB"),
            ("Mwinyi2004", "Fig1"),
            ("Mwinyi2004", "Fig2_Ae_Mean"),
            ("Niemi2004", "Fig1"),
            ("Niemi2006", "Fig1"),
            ("Nishizato2003", "Fig1"),
        ]:
            df = self.load_dataframe(fig_id, study=study)
            if fig_id == "Fig2_Ae_Mean":
                df = df[df.measurement_type == "cumulative amount"]

            for label, df_label in df.groupby("label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.pra)
                dsets[f"{study}_{fig_id}_{label}"] = dset

        # Nishizato2003, the cumulative amount in the urine by group
        df = self.load_dataframe("Tab6b", study="Nishizato2003")
        for group, df_group in df.groupby("group"):
            group = str(group)
            df_group_cum_amount = df_group[
                df_group["measurement_type"] == "cumulative amount"
            ]
            dset = DataSet.from_df(df_group_cum_amount, self.ureg)
            # convert to micro mole
            dset.unit_conversion("mean", 1 / self.Mr.pra)
            dsets[f"Nishizato2003_Tab6b_{group}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}

        # MRP2 scans (Niemi2006), OATP1B1 scans
        for scan_key, doses in [("mrp2", [40]), ("oatp1b1", [10, 40])]:
            scan_data = self.scan_map[scan_key]
            for dose in doses:
                tcscans[f"scan_pra_{dose}_{scan_key}"] = Scan(
                    simulation=Simulation(
                        start=0,
                        end=12 * 60 + 60,
                        preinit_changes={
                            **self.default_changes(),
                            "PODOSE_pra": Q(dose, "mg"),
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
            **self.figures_MRP2(),
            **self.figures_OATP1B1(),
        }

    @staticmethod
    def add_function_colorbar(f: FigureMPL, axes: np.ndarray, label: str) -> None:
        """Add the colorbar of the scanned transporter function to the figure.

        The simulations are colored `seismic` with
        `1 - (function - 0.1) / 1.8`, red less function, blue more function,
        the reference function 1.0 is black.

        Args:
            f: the figure.
            axes: the axes of the figure, the colorbar is right of them.
            label: the label of the scanned function.
        """
        norm = Normalize(vmin=0.1, vmax=1.9)
        cb = f.colorbar(
            ScalarMappable(norm=norm, cmap="seismic_r"), ax=axes, fraction=0.03
        )
        # the gradient as vector cells: matplotlib rasterizes it into an
        # embedded image, which some SVG viewers do not show; the edges of
        # the cells in their color close the seams between them
        if cb.solids is not None:
            cb.solids.set_rasterized(False)
            cb.solids.set_edgecolor("face")
        cb.ax.axhline(1.0, color="black", linewidth=3)
        cb.set_ticks([0.2, 0.6, 1.0, 1.4, 1.8])
        cb.ax.tick_params(labelsize=PravastatinSimulationExperiment.tick_font_size)
        cb.set_label(label, fontdict=PravastatinSimulationExperiment.font)

    def plot_scan_point(
        self,
        ax: Axes,
        xres: ScanResult,
        sid: str,
        scandim: str,
        k_par: int,
        value: float,
        color: ColorType,
    ) -> None:
        """Draw the timecourse of a point of a scan.

        In a run over the draws of the fitted parameters the curve is the
        median of the draws; the reference (1.0) has the band of their
        quantiles, the bands of all points would cover each other. The
        reference is drawn on top of the other curves.
        """
        t_vec, c_vec, c_lower, c_upper = self.scan_timecourse(
            xres, sid, **{scandim: k_par}
        )
        reference = bool(np.isclose(1.0, value))
        if self.uncertainty is not None and reference:
            ax.fill_between(
                t_vec.magnitude,
                c_lower.magnitude,
                c_upper.magnitude,
                color=color,
                alpha=self.band_alpha,
                linewidth=0,
            )
        # the reference on top of the other curves
        ax.plot(
            t_vec.magnitude,
            c_vec.magnitude,
            color=color,
            linewidth=3.0,
            zorder=3 if reference else 2,
        )

    def figures_MRP2(self) -> dict[str, FigureMPL]:
        """Dependency plasma pravastatin on MRP2 change."""
        scan_key = "mrp2"
        scan_data = self.scan_map[scan_key]

        # Figure for multiple plots
        f, axes = plt.subplots(
            nrows=1, ncols=2, figsize=(6 * 2 + 1, 6), layout="constrained"
        )

        cmap = matplotlib.colormaps["seismic"]

        # --- simulation ---
        ax0 = axes[0]
        ax0.set_title(
            "Simulation MRP2 function\nplasma (40 mg)",
            fontdict={
                "fontsize": self.tick_font_size,
                "fontweight": "bold",
            },
        )

        xres = self.results["task_scan_pra_40_mrp2"]

        # scanned dimension
        scandim = self.scanned_dimension(xres)
        par_vec = self.scan_values(xres, scan_data["parameter"])

        # plot plasma concentrations
        sid = "[Cve_pra]"
        for k_par, par in enumerate(par_vec):
            # 0.1 - 1.9
            if np.isclose(1.0, par.magnitude):
                color = "black"
            else:
                # red less function, blue more function
                cvalue = 1 - ((par.magnitude - 0.1) / 1.8)
                color = cmap(cvalue)
            self.plot_scan_point(ax0, xres, sid, scandim, k_par, par.magnitude, color)

        # --- data ---
        ax1 = axes[1]
        ax1.set_title(
            "Data MRP2 genotypes\nplasma (40 mg)",
            fontdict={
                "fontsize": self.tick_font_size,
                "fontweight": "bold",
            },
        )

        dsets: dict[str, DataStyle] = {
            "Niemi2006_Fig1_no_SLCO1B1_17_c1446CC": {
                "label": "Niemi2006 No ABCC2 c.1446CG (n=35)",
                "color": "black",
            },
            "Niemi2006_Fig1_c1446CG": {
                "label": "Niemi2006 ABCC2 c.1446CG (n=3)",
                "color": "tab:red",
            },
        }
        for dset_id, data in dsets.items():
            dset = self._datasets[dset_id]

            x = dset["time"]
            y = Q(dset["mean"], dset["mean_unit"].values[0]).to("µM").magnitude

            ax1.errorbar(
                x,
                y,
                yerr=Q(dset["mean_sd"], dset["mean_unit"].values[0]).to("µM").magnitude,
                label=data["label"],
                color=data["color"],
                linestyle="--",
                marker="s",
                markeredgecolor="black",
            )

        ax1.legend()
        self.add_function_colorbar(f, axes, label=scan_data["label"])

        # the axes are scaled separately: the standard deviations of the data
        # are much larger than the concentrations
        for ax in axes:
            ax.tick_params(axis="x", labelsize=self.tick_font_size)
            ax.tick_params(axis="y", labelsize=self.tick_font_size)

            ax.set_xlabel(
                f"{self.label_time} [{self.units['time']}]",
                fontdict=self.font,
            )
            ax.set_ylabel(
                f"{self.labels[sid]} [{self.units[sid]}]",
                fontdict=self.font,
            )
            ax.set_ylim(bottom=0.0)
            ax.set_xlim(right=13.0)

        return {"fig_MRP2": f}

    def figures_OATP1B1(self) -> dict[str, FigureMPL]:
        """Dependency plasma pravastatin on OATP1B1 change."""
        scan_key = "oatp1b1"
        scan_data = self.scan_map[scan_key]

        # Figure for multiple plots
        # a row per dose: simulated plasma, data plasma, simulated urine
        f, axes = plt.subplots(
            nrows=2, ncols=3, figsize=(6 * 3 + 1, 6 * 2), layout="constrained"
        )
        # the simulations and the data of the plasma on the same scale
        for k in [0, 1]:
            axes[k, 1].sharey(axes[k, 0])

        cmap = matplotlib.colormaps["seismic"]

        for k, dose in enumerate([10, 40]):
            # scanned dimension
            xres = self.results[f"task_scan_pra_{dose}_oatp1b1"]
            scandim = self.scanned_dimension(xres)
            par_vec = self.scan_values(xres, scan_data["parameter"])

            # simulation plasma
            ax0 = axes[k, 0]
            ax0.set_title(
                f"Simulation OATP1B1 function\nplasma ({dose} mg)",
                fontdict={
                    "fontsize": self.tick_font_size,
                    "fontweight": "bold",
                },
            )
            # simulation urine
            ax2 = axes[k, 2]
            ax2.set_title(
                f"Simulation OATP1B1 function\nurine ({dose} mg)",
                fontdict={
                    "fontsize": self.tick_font_size,
                    "fontweight": "bold",
                },
            )

            for k_par, par in enumerate(par_vec):
                # 0.1 - 1.9
                if np.isclose(1.0, par.magnitude):
                    color = "black"
                else:
                    # red less function, blue more function
                    cvalue = 1 - ((par.magnitude - 0.1) / 1.8)
                    color = cmap(cvalue)

                # plasma concentration and urine amount
                for ax, sid in [(ax0, "[Cve_pra]"), (ax2, "Aurine_pra")]:
                    self.plot_scan_point(
                        ax, xres, sid, scandim, k_par, par.magnitude, color
                    )

        # --- data ---
        for k, dose in enumerate([10, 40]):
            ax = axes[k, 1]
            ax.set_title(
                f"Data OATP1B1 genotypes\nplasma ({dose} mg)",
                fontdict={
                    "fontsize": self.tick_font_size,
                    "fontweight": "bold",
                },
            )

        # FIXME: add Deng, check other data
        # FIXME: add urinary recovery data
        dsets: dict[str, GenotypeDataStyle] = {
            "Ho2007_Fig1_TT": {
                "dose": 40,
                "label": "Ho2007 521 T/T (n=88)",
                "color": "black",
                "marker": "s",
            },
            "Ho2007_Fig1_TC": {
                "dose": 40,
                "label": "Ho2007 521 T/C (n=17)",
                "color": "tab:red",
                "marker": "s",
            },
            "Ho2007_Fig1_CC": {
                "dose": 40,
                "label": "Ho2007 521 C/C (n=2)",
                "color": "darkred",
                "marker": "s",
            },
            "Maeda2006_Fig1AB_Fig1AB_1a1a": {
                "dose": 10,
                "label": "Maeda2006 *1a/*1a (n=5)",
                "color": "black",
                "marker": "s",
            },
            "Maeda2006_Fig1AB_Fig1AB_1b1b": {
                "dose": 10,
                "label": "Maeda2006 *1b/*1b (n=7)",
                "color": "tab:blue",
                "marker": "s",
            },
            "Maeda2006_Fig1AB_Fig1AB_1a15": {
                "dose": 10,
                "label": "Maeda2006 *1a/*15 (n=6)",
                "color": "tab:red",
                "marker": "s",
            },
            "Maeda2006_Fig1AB_Fig1AB_1b15": {
                "dose": 10,
                "label": "Maeda2006 *1b/*15 (n=5)",
                "color": "tab:orange",
                "marker": "s",
            },
            "Mwinyi2004_Fig1_Fig1_1a1a": {
                "dose": 40,
                "label": "Mwinyi2004 *1a/*1a (n=10)",
                "color": "black",
                "marker": "o",
            },
            "Mwinyi2004_Fig1_Fig1_1a1b_1b1b": {
                "dose": 40,
                "label": "Mwinyi2004 *1a/*1b & *1b/*1b (n=10)",
                "color": "tab:blue",
                "marker": "o",
            },
            "Mwinyi2004_Fig1_Fig1_1a5": {
                "dose": 40,
                "label": "Mwinyi2004 *1a/*5 (n=10)",
                "color": "tab:red",
                "marker": "o",
            },
            "Nishizato2003_Fig1_slco1b1_15_15": {
                "dose": 10,
                "label": "Nishizato2003 *15/*15 (n=1)",
                "color": "tab:red",
                "marker": "o",
            },
            "Nishizato2003_Fig1_slco1b1_1b_15": {
                "dose": 10,
                "label": "Nishizato2003 *1b/*15 (n=9)",
                "color": "tab:orange",
                "marker": "o",
            },
            "Nishizato2003_Fig1_slco1b1_1b_1b": {
                "dose": 10,
                "label": "Nishizato2003 *1b/*1b (n=4)",
                "color": "tab:blue",
                "marker": "o",
            },
            "Niemi2004_Fig1_521TT": {
                "dose": 40,
                "label": "Niemi2004 521 T/T (n=28)",
                "color": "black",
                "marker": "^",
            },
            "Niemi2004_Fig1_521TC": {
                "dose": 40,
                "label": "Niemi2004 521 T/C (n=11)",
                "color": "tab:red",
                "marker": "^",
            },
            "Niemi2004_Fig1_521CC": {
                "dose": 40,
                "label": "Niemi2004 521 C/C (n=2)",
                "color": "darkred",
                "marker": "^",
            },
        }
        # the panel and the line style of the data of a dose
        dose_panels = {10: (axes[0, 1], "solid"), 40: (axes[1, 1], "dotted")}
        for dset_id, data in dsets.items():
            dset = self._datasets[dset_id]
            ax, linestyle = dose_panels[data["dose"]]

            x = Q(dset["time"], dset["time_unit"].values[0]).to("hr").magnitude
            y = Q(dset["mean"], dset["mean_unit"].values[0]).to("µM").magnitude

            ax.plot(
                x,
                y,
                label=data["label"],
                color=data["color"],
                linestyle=linestyle,
                marker=data["marker"],
            )

        axes[0, 1].legend()
        axes[1, 1].legend()
        self.add_function_colorbar(f, axes, label=scan_data["label"])

        # the plasma concentrations in the first two columns, the urine amount
        # in the last
        for col, sid in enumerate(["[Cve_pra]", "[Cve_pra]", "Aurine_pra"]):
            for ax in axes[:, col]:
                ax.tick_params(axis="x", labelsize=self.tick_font_size)
                ax.tick_params(axis="y", labelsize=self.tick_font_size)

                ax.set_xlabel(
                    f"{self.label_time} [{self.units['time']}]",
                    fontdict=self.font,
                )
                ax.set_ylabel(
                    f"{self.labels[sid]} [{self.units[sid]}]",
                    fontdict=self.font,
                )
                ax.set_ylim(bottom=0.0)
                ax.set_xlim(right=14.0)
                ax.set_xticks(np.arange(0, 15, 2))

        return {"fig_OATP1B1": f}
