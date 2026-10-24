"""Simulation experiment of the study Sugimoto2001."""

from typing import ClassVar, override

from pkpdsim.metadata import (
    ApplicationForm,
    Coadministration,
    DataType,
    Dosing,
    Fasting,
    Genotype,
    Health,
    PKPDMappingMetaData,
    Route,
    Tissue,
)
from sbmlsim import Q
from sbmlsim.data import DataSet
from sbmlsim.fit import FitData, FitMapping
from sbmlsim.plot import Axis, Figure
from sbmlsim.simulation import Simulation

from pkdb_models.models.pravastatin import MODEL
from pkdb_models.models.pravastatin.experiments.base_experiment import (
    PravastatinSimulationExperiment,
)


class Sugimoto2001(PravastatinSimulationExperiment):
    """Simulation experiment of Sugimoto2001 (study 2, pravastatin).

    8 healthy Japanese men (65 kg) took St John's wort (300 mg, 0.3 %
    hypericin) or placebo three times daily for 14 days in a randomized
    double-blind crossover; on day 14 they took 20 mg pravastatin sodium (two
    10 mg Mevalotin tablets) after an overnight fast, a meal 4 h later. Plasma
    by LC-MS/MS (detection limit 0.5 ng/ml) to 24 h (Fig2, mean and SE).

    St John's wort induces CYP3A4 and P-glycoprotein, which do not eliminate
    pravastatin: no interaction (AUC ratio 1.03 of the individual ratios), its
    arm is mapped to the simulation of the control (`F_NO_INTERACTION` of the
    base experiment). The means below the detection limit (12 and 24 h) are
    not fitted.
    """

    #: the detection limit of pravastatin [ng/ml]
    lloq: ClassVar[float] = 0.5

    #: the arms of Fig2 (dataset key: label of the data, coadministration)
    arms: ClassVar[dict[str, tuple[str, Coadministration]]] = {
        "PRA": ("SIM_pravastatin", Coadministration.NONE),
        "PRA_STJ": ("SIM+STJ_pravastatin", Coadministration.ST_JOHNS_WORT),
    }
    labels_arm: ClassVar[dict[str, str]] = {
        "PRA": "20 mg (placebo)",
        "PRA_STJ": "20 mg + St John's wort",
    }
    colors: ClassVar[dict[str, str]] = {
        "PRA": "black",
        "PRA_STJ": "tab:green",
    }
    markers: ClassVar[dict[str, str]] = {
        "PRA": "o",
        "PRA_STJ": "s",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig2")
        for key, (label, _) in self.arms.items():
            df_label = df[df.label == label]
            # all points for the figure, the predose value and the points
            # above the detection limit for the fit
            df_fit = df_label[(df_label.time == 0) | (df_label["mean"] >= self.lloq)]
            for suffix, df_data in [("", df_label), ("_lloq", df_fit)]:
                dset = DataSet.from_df(df_data, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.pra)
                dsets[f"Fig2_{key}{suffix}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "pra_20": Simulation(
                start=0,
                end=25 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # 20 mg pravastatin sodium, fasted
                    "PODOSE_pra": Q(20, "mg") * self.Mr.pra / self.Mr.pra_na,
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for key, (_, coadministration) in self.arms.items():
            mappings[f"fm_pra20po_Fig2_{key}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig2_{key}_lloq",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_pra_20", xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FASTED,
                    health=Health.HEALTHY,
                    coadministration=coadministration,
                    genotype=Genotype.NR,
                    data_type=DataType.MEAN,
                ),
            )
        return mappings

    @override
    def figures(self) -> dict[str, Figure]:
        fig = Figure(
            experiment=self,
            sid="Fig2",
            num_cols=2,
            name=f"{self.__class__.__name__} (healthy, fasted)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-3)

        for plot in plots:
            plot.add_data(
                task="task_pra_20",
                xid="time",
                yid="[Cve_pra]",
                label="Sim 20 mg",
                color="black",
            )
            for key in self.arms:
                plot.add_data(
                    dataset=f"Fig2_{key}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=self.labels_arm[key],
                    color=self.colors[key],
                    marker=self.markers[key],
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Sugimoto2001, output_dir=Sugimoto2001.__name__)
