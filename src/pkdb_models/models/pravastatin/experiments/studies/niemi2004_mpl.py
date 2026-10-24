"""Simulation experiment of the study Niemi2004 with a matplotlib figure."""

from typing import override

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure as FigureMPL
from sbmlsim import Q
from sbmlsim.plot import Figure
from sbmlsim.result.timecourse import plot_times

from pkdb_models.models.pravastatin.experiments.base_experiment import FontKwargs
from pkdb_models.models.pravastatin.experiments.studies.niemi2004 import Niemi2004


class Niemi2004_mpl(Niemi2004):
    """Niemi2004 with a matplotlib figure of the c.521T>C genotypes (Fig1b).

    The data, the simulations and the fit mappings are those of `Niemi2004`
    (the experiment is not in a fit); only the figure differs.
    """

    @override
    def figures(self) -> dict[str, Figure]:
        return {}

    @override
    def figures_mpl(self) -> dict[str, FigureMPL]:
        kwargs: FontKwargs = {"weight": "bold", "size": 14}
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 4))
        ax.set_xlabel("Time [hr]", **kwargs)
        ax.set_ylabel("Plasma pravastatin [µM]", **kwargs)

        for group in self.panels["b"]:
            genotype = self.group_genotypes[group]
            color = self.slco1b1_colors[genotype]

            # simulation, the median over the draws of a run over them
            xres = self.results[self.task_id(group)]
            if self.uncertainty is not None:
                # the draws keep their own steps of the integrator: their
                # median on the time points of the figure
                xres = xres.interpolate(plot_times(xres.ds["time"].values))
            conc = xres["[Cve_pra]"]
            if self.uncertainty is not None:
                conc = conc.median(dim=self.uncertainty.id)
            time = Q(np.asarray(xres["time"].values), "min").to("hr").magnitude
            ax.plot(
                time,
                Q(np.asarray(conc.values), "mM").to("µM").magnitude,
                label=f"Sim {genotype}",
                color=color,
            )

            # data
            dataset = self._datasets[self.to_sid(f"Fig1_{group}")]
            count = int(dataset["count"].max())
            ax.errorbar(
                dataset["time"],
                dataset["mean"] * 1000,  # mM (mole/m³) to µM
                dataset["mean_sd"] * 1000,
                linestyle="",
                label=f"{self.labels_group[group]} (n={count})",
                color=color,
                marker=self.markers[genotype],
                markersize=4,
            )

        ax.legend(loc="best", prop={"size": 8})
        ax.set_ylim(bottom=0)
        return {"Fig1b": fig}
