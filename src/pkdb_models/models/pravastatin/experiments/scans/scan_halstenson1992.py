"""Scan of the renal function compared to the renal clearance of Halstenson1992."""

from typing import ClassVar, override

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure as FigureMPL
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
    ScanSpec,
)


class Halstenson1992Scan(PravastatinSimulationExperiment):
    """Scan the effect of renal function on pravastatin pharmacokinetics.

    In a run over the draws of the fitted parameters (`run_simulation
    pkdb_models.models.pravastatin --uncertainty`) the renal clearance is the
    median of the draws with the band of their quantiles.
    """

    scan_map: ClassVar[dict[str, ScanSpec]] = {
        "renal": {
            "parameter": "KI__f_renal_function",
            "range": np.linspace(0.1, 1.9, num=19),
            "units": "dimensionless",
            "label": "Renal function [-]",
        },
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        # Halstenson1992
        for fig_id in ["Fig2"]:
            df = self.load_dataframe(fig_id, study="Halstenson1992")
            for label, df_label in df.groupby("y_label"):
                label = str(label)
                dset = DataSet.from_df(df_label, self.ureg)
                dsets[f"Halstenson1992_{fig_id}_{label}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}

        # renal scans (Halstenson1992)
        scan_data = self.scan_map["renal"]
        tcscans["scan_pra_20_renal"] = Scan(
            simulation=Simulation(
                start=0,
                end=12 * 60 + 60,
                preinit_changes={
                    **self.default_changes(),
                    "PODOSE_pra": Q(20, "mg"),
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
            **self.figures_Halstenson1992_Fig2B(),
        }

    def figures_Halstenson1992_Fig2B(self) -> dict[str, FigureMPL]:
        """Dependency renal clearance on renal function.

        The renal function of the simulations is converted to the creatinine
        clearance with the creatinine clearance of normal renal function.
        """
        f, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 6))

        # lines and areas
        ax.axvspan(
            90,
            150,
            color="white",
            lw=0,
            label="Control",
        )
        ax.axvspan(
            50,
            90,
            color=self.renal_colors["Mild renal impairment"],
            lw=0,
            label="Mild renal impairment",
        )
        ax.axvspan(
            30,
            50,
            color=self.renal_colors["Moderate renal impairment"],
            lw=0,
            label="Moderate renal impairment",
        )
        ax.axvspan(
            0,
            30,
            color=self.renal_colors["Severe renal impairment"],
            lw=0,
            label="Severe renal impairment",
        )

        # --- data ---
        dset = self._datasets["Halstenson1992_Fig2_renal_clearance_pra"]
        ax.plot(
            dset["x_value"],
            dset["y_value"] / 60,  # [l/hr] -> [l/min]
            marker="o",
            linestyle="",
            color="black",
            markerfacecolor="darkgrey",
            label="Halstenson1992",
            markersize=10,
        )

        # --- simulation ---
        sim_key = "scan_pra_20_renal"
        xres = self.results[f"task_{sim_key}"]
        df = self.calculate_pravastatin_pk([sim_key])[sim_key]

        # the GFR of the model, `KI__f_renal_function * KI__GFR_base`, against
        # the measured creatinine clearance
        x = self.scan_values(xres, "KI__GFR").to("ml/min").magnitude
        unit = df["cl_renal_unit"].iloc[0]
        y, y_lower, y_upper = (
            Q(v, unit).to(self.pk_units["cl_renal"]).magnitude
            for v in self.pk_summary(df, "cl_renal")
        )
        if self.uncertainty is not None:
            ax.fill_between(
                x, y_lower, y_upper, color="black", alpha=self.band_alpha, linewidth=0
            )

        ax.plot(
            x,
            y,
            marker="o",
            linestyle="-",
            color="black",
            label="Simulation",
            markersize=6,
            markerfacecolor="black",
            markeredgecolor="white",
        )

        # data
        ax.errorbar(
            x=[101.0, 69.5, 32.5, 19.5],
            xerr=[9.2, 12.0, 2.4, 4.4],
            y=[25.86 / 60, 15.21 / 60, 6.23 / 60, 2.87 / 60],  # [l/hr] -> [l/min]
            # the SD of the groups (Tab2) [l/hr] -> [l/min]
            yerr=[9.24 / 60, 5.38 / 60, 1.49 / 60, 0.86 / 60],
            marker="s",
            linestyle="",
            color="black",
            markeredgecolor="white",
            label="Halstenson1992±SD (n=4)",
            markersize=8,
        )

        # plot styling
        ax.set_xlabel(
            "Creatinine clearance [ml/min/1.73 m²]",
            fontdict=self.font,
        )
        ax.set_ylabel(
            "Renal clearance [l/min]",
            fontdict=self.font,
        )
        ax.set_xlim(right=125)
        ax.tick_params(axis="x", labelsize=self.tick_font_size)
        ax.tick_params(axis="y", labelsize=self.tick_font_size)
        ax.set_ylim(bottom=0.0, top=0.7)
        ax.set_xlim(left=0.0)
        ax.legend(
            fontsize=self.legend_font_size - 3,
            loc="upper left",
        )

        return {"fig_Halstenson1992_Fig2": f}
