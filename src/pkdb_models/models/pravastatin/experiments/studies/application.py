"""Simulation experiment of the oral and intravenous application of pravastatin."""

from typing import override

from sbmlsim import Q
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
)


class ApplicationExperiment(PravastatinSimulationExperiment):
    """Tests oral and intravenous application of pravastatin."""

    @override
    def simulations(self) -> dict[str, Simulation]:
        simulations = {}
        tend = 60 * 5  # [min]
        simulations["pra_iv"] = Simulation(
            start=0,
            end=tend,
            preinit_changes={
                **self.default_changes(),
                "IVDOSE_pra": Q(40, "mg"),
            },
        )
        simulations["pra_po"] = Simulation(
            start=0,
            end=tend,
            preinit_changes={
                **self.default_changes(),
                "PODOSE_pra": Q(40, "mg"),
            },
        )

        return simulations

    @override
    def figures(self) -> dict[str, Figure]:
        name = "Oral vs. intravenous pravastatin application"
        fig = Figure(
            experiment=self,
            sid="Fig_application",
            num_rows=2,
            num_cols=3,
            name=name,
        )
        plots = fig.create_plots(xaxis=Axis("time", unit="hr"), legend=True)
        plots[0].set_yaxis("pravastatin\n", unit="µM")
        plots[1].set_yaxis("pravastatin intestinal\nlumen", unit="µM")
        plots[2].set_yaxis("pravastatin liver\n", unit="µM")
        plots[3].set_yaxis("pravastatin arterial\n", unit="µM")
        plots[4].set_yaxis("pravastatin urine\n", unit="µmole")
        plots[5].set_yaxis("pravastatin feces\n", unit="µmole")

        for application in ["iv", "po"]:
            task_id = f"task_pra_{application}"
            linestyle = "-" if application == "iv" else "--"

            # simulation
            plots[0].add_data(
                task=task_id,
                xid="time",
                yid="[Cve_pra]",
                label=f"pravastatin venous ({application})",
                linestyle=linestyle,
            )
            plots[1].add_data(
                task=task_id,
                xid="time",
                yid="[Cgulumen_pra]",
                label=f"pravastatin intestinal lumen ({application})",
                linestyle=linestyle,
            )
            plots[2].add_data(
                task=task_id,
                xid="time",
                yid="[LI__pra]",
                label=f"pravastatin liver ({application})",
                linestyle=linestyle,
            )
            plots[3].add_data(
                task=task_id,
                xid="time",
                yid="[Car_pra]",
                label=f"pravastatin arterial ({application})",
                linestyle=linestyle,
            )
            plots[4].add_data(
                task=task_id,
                xid="time",
                yid="Aurine_pra",
                label=f"pravastatin urine ({application})",
                linestyle=linestyle,
            )
            plots[5].add_data(
                task=task_id,
                xid="time",
                yid="Afeces_pra",
                label=f"pravastatin feces ({application})",
                linestyle=linestyle,
            )

        return self.figures_by_sid(fig)
