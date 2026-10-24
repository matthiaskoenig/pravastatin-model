"""Simulation experiment of the study Pan2000."""

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


class Pan2000(PravastatinSimulationExperiment):
    """Simulation experiment of Pan2000.

    23 healthy Caucasian adults (16 men, 7 women, 76 kg) took a single 40 mg
    tablet of pravastatin sodium with 180 ml water 30 min after the start of a
    standard breakfast (fed), alone (regimen C) and with 201 mg fenofibrate
    (regimen B) in a three-period crossover. Plasma by LC-MS/MS (limit of
    quantification 0.5 ng/ml) to 12 h (Fig2, mean and SE: the caption says SD,
    but the bars are SE by the coefficient of variation of Cmax in Table II).

    Fenofibrate does not change the pharmacokinetics of pravastatin (AUC ratio
    1.13, 90 % CI 0.91-1.40): its arm is mapped to the simulation of the
    control (`F_NO_INTERACTION` of the base experiment). The
    3alpha-isopravastatin (SQ 31906) is not in the model and not shown.
    """

    #: the limit of quantification of pravastatin [ng/ml]; the means below it
    #: (10 and 12 h) average values below the limit and are not fitted
    lloq: ClassVar[float] = 0.5

    #: the arms of Fig2 with their coadministered drug
    coadministrations: ClassVar[dict[str, Coadministration]] = {
        "PRA40_RegC": Coadministration.NONE,
        "PRA40_RegB": Coadministration.FENOFIBRATE,
    }
    labels_arm: ClassVar[dict[str, str]] = {
        "PRA40_RegC": "40 mg (control)",
        "PRA40_RegB": "40 mg + fenofibrate 201 mg",
    }
    colors: ClassVar[dict[str, str]] = {
        "PRA40_RegC": "black",
        "PRA40_RegB": "tab:orange",
    }
    markers: ClassVar[dict[str, str]] = {
        "PRA40_RegC": "s",
        "PRA40_RegB": "o",
    }

    @override
    def datasets(self) -> dict[str, DataSet]:
        dsets = {}
        df = self.load_dataframe("Fig2")
        for label in self.coadministrations:
            df_label = df[df.label == label]
            # all points for the figure, the points above the limit of
            # quantification for the fit
            for suffix, df_data in [
                ("", df_label),
                ("_lloq", df_label[df_label["mean"] >= self.lloq]),
            ]:
                dset = DataSet.from_df(df_data, self.ureg)
                dset.unit_conversion("mean", 1 / self.Mr.pra)
                dsets[f"Fig2_{label}{suffix}"] = dset

        return dsets

    @override
    def simulations(self) -> dict[str, Simulation]:
        return {
            "pra_40": Simulation(
                start=0,
                end=13 * 60,
                preinit_changes={
                    **self.default_changes(),
                    # 40 mg pravastatin sodium
                    "PODOSE_pra": Q(40, "mg") * self.Mr.pra / self.Mr.pra_na,
                    # 30 min after the start of a standard breakfast
                    "GU__fed": Q(1, "dimensionless"),
                },
            )
        }

    @override
    def fit_mappings(self) -> dict[str, FitMapping]:
        mappings = {}
        for label, coadministration in self.coadministrations.items():
            mappings[f"fm_pra40po_Fig2_{label}"] = FitMapping(
                self,
                reference=FitData(
                    self,
                    dataset=f"Fig2_{label}_lloq",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                ),
                observable=FitData(
                    self, task="task_pra_40", xid="time", yid="[Cve_pra]"
                ),
                metadata=PKPDMappingMetaData(
                    tissue=Tissue.PLASMA,
                    route=Route.PO,
                    application_form=ApplicationForm.TABLET,
                    dosing=Dosing.SINGLE,
                    fasting=Fasting.FED,
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
            name=f"{self.__class__.__name__} (healthy, fed)",
            # one legend per row, the panels share their curves
            settings={"legend_scope": "row"},
        )
        plots = fig.create_plots(xaxis=Axis(self.label_time, unit="hr"), legend=True)
        plots[0].set_yaxis(self.label_pra, unit="µM")
        plots[1].set_yaxis(self.label_pra, unit="µM", scale="log", min=1e-4)

        for plot in plots:
            plot.add_data(
                task="task_pra_40",
                xid="time",
                yid="[Cve_pra]",
                label="Sim 40 mg (fed)",
                color="black",
            )
            for label in self.coadministrations:
                plot.add_data(
                    dataset=f"Fig2_{label}",
                    xid="time",
                    yid="mean",
                    yid_sd="mean_sd",
                    count="count",
                    label=self.labels_arm[label],
                    color=self.colors[label],
                    marker=self.markers[label],
                )

        return self.figures_by_sid(fig)


if __name__ == "__main__":
    MODEL.run_experiments(Pan2000, output_dir=Pan2000.__name__)
