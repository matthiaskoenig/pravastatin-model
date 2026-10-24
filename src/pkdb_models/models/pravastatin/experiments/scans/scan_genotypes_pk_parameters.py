"""Scans of the pharmacokinetic parameters depending on the transporters MRP2 and OATP1B1."""

import itertools
from typing import ClassVar, override

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.figure import Figure as FigureMPL
from sbmlsim import Q
from sbmlsim.simulation import Dimension, Scan, Simulation

from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
    ScanSpec,
)
from pkdb_models.models.pravastatin.pravastatin_pk import (
    calculate_pravastatin_pk,
)


class DoseScanSpec(ScanSpec):
    """Definition of the scan of a parameter at several doses [mg]."""

    title: str
    dose: list[int]


class GenotypeScanPKParameters(PravastatinSimulationExperiment):
    """Scan the effect of genotypes on plasma pravastastatin pharmacokinetic parameters.

    In a run over the draws of the fitted parameters (`run_simulation
    pkdb_models.models.pravastatin --uncertainty`) the parameters are the
    median of the draws with the band of their quantiles.
    """

    # FIXME: BETTER SCANS: "range": np.sort(np.append(np.logspace(-1, 1, num=num_points), [1.0])),  # [10^-1=0.1, 10^1=10]
    # set up for the enzyme activity scan
    scan_map: ClassVar[dict[str, DoseScanSpec]] = {
        "mrp2": {
            "title": "MRP2",
            "parameter": "LI__f_MRP2",
            "range": np.logspace(-2, 1, num=10),
            "units": "dimensionless",
            "label": "MRP2 function [-]",
            "dose": [5, 10, 20, 40, 80],
        },
        "oatp1b1": {
            "title": "OATP1B1",
            "parameter": "LI__f_OATP1B1",
            "range": np.logspace(-2, 1, num=10),
            "units": "dimensionless",
            "label": "OATP1B1 function [-]",
            "dose": [5, 10, 20, 40, 80],
        },
    }

    # color mapping for pra dosing (done accordingly to simvastatin colors)
    colors_dose: ClassVar[dict[float, str]] = {
        0: "black",
        2.5: "yellow",
        5: "#ffeda0",
        10: "#fed976",
        20: "#fd8d3c",
        40: "#fc4e2a",
        80: "#e31a1c",
        160: "#b10026",
    }

    @override
    def simulations(self) -> dict[str, Scan]:
        tcscans = {}

        # MRP2 scans (Niemi2006), OATP1B1 scans
        for scan_key in ["mrp2", "oatp1b1"]:
            scan_data = self.scan_map[scan_key]
            for dose in scan_data["dose"]:
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
            **self.figures_genotypes(),
        }

    def figures_genotypes(self) -> dict[str, FigureMPL]:
        """Dependency plasma pravastatin pharmacokinetic parameters on MRP2 and OATP1B1 change."""
        figures: dict[str, FigureMPL] = {}
        for scan_key in ["mrp2", "oatp1b1"]:
            scan_data = self.scan_map[scan_key]

            f, axes = plt.subplots(
                nrows=2, ncols=1, figsize=(7, 11), squeeze=False, layout="constrained"
            )
            f.suptitle(
                "Pravastatin pharmacokinetic parameters\n"
                f"depending on {scan_data['title']} function",
                fontsize=20,
                fontweight="bold",
            )

            # --- simulation ---
            for dose in scan_data["dose"]:
                xres = self.results[f"task_scan_pra_{dose}_{scan_key}"]

                # scanned dimension
                par_vec = self.scan_values(xres, scan_data["parameter"])
                # the parameters normalized to a dose of 10 mg, per draw of the
                # fitted parameters in a run over them
                run = self.uncertainty
                df = calculate_pravastatin_pk(
                    experiment=self,
                    xres=xres,
                    normalization_dose=Q(10, "mg"),
                    across=None if run is None else run.id,
                )

                color = self.colors_dose[dose]

                # plot pk_parameters
                for row, pk_parameter in enumerate(["auc_last", "cl_f"]):
                    pk_unit = self.pk_units[pk_parameter]
                    unit = df[f"{pk_parameter}_unit"].iloc[0]
                    values, lower, upper = (
                        Q(v, unit).to(pk_unit)
                        for v in self.pk_summary(df, pk_parameter)
                    )
                    if run is not None:
                        axes[row, 0].fill_between(
                            par_vec.magnitude,
                            lower.magnitude,
                            upper.magnitude,
                            color=color,
                            alpha=self.band_alpha,
                            linewidth=0,
                        )

                    axes[row, 0].plot(
                        par_vec.magnitude,
                        values.magnitude,
                        color=color,
                        marker="s",
                        markeredgecolor="black",
                        linewidth=1.0,
                        markersize=8,
                        label=f"Dose {dose} mg",
                    )

                    axes[row, 0].set_ylabel(
                        f"{self.pk_labels[pk_parameter]}\n[{values.units:~P}]",
                        fontdict=self.font,
                    )

            # background on the logarithmic axis: red less function, blue more
            # function, symmetric around the reference function 1.0 (black line)
            xlim = (scan_data["range"].min() * 0.9, scan_data["range"].max() * 1.1)
            halfrange = np.max(np.abs(np.log10(xlim)))
            norm = LogNorm(vmin=10**-halfrange, vmax=10**halfrange)
            cmap = matplotlib.colormaps["coolwarm_r"]
            edges = np.logspace(np.log10(xlim[0]), np.log10(xlim[1]), num=101)
            for ax in axes[:, 0]:
                for lower, upper in itertools.pairwise(edges):
                    ax.axvspan(
                        lower,
                        upper,
                        color=cmap(norm(np.sqrt(lower * upper))),
                        lw=0,
                        alpha=0.5,
                        antialiased=False,
                        zorder=0,
                    )
                ax.axvline(1.0, color="black", linewidth=2, zorder=1)
                ax.set_xscale("log")
                ax.set_xlim(xlim)
                ax.tick_params(axis="x", labelsize=self.tick_font_size)
                ax.tick_params(axis="y", labelsize=self.tick_font_size)

            axes[1, 0].set_xlabel(scan_data["label"], fontdict=self.font)

            # the legend of the doses, with the markers of the curves
            handles, labels = axes[0, 0].get_legend_handles_labels()
            f.legend(
                handles,
                labels,
                ncol=3,
                loc="outside lower center",
                fontsize=self.legend_font_size,
            )

            figures[f"fig_{scan_key}"] = f
        return figures
