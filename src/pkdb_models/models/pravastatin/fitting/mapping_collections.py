"""Parameter fit problems for pravastatin.

The data of a fit is selected from the fit mappings of the studies in three
steps, see `sbmlsim.fit.helpers`: the filters on the metadata of the mappings
select the training data of the fit and exclude the rest, the outliers are
named once for all mappings and are the training data which is not usable, and
the validation data is the part of the data a fit is evaluated on but not
fitted to. The metadata of a mapping describes its curve, what a fit does with
the curve is decided here.

The training data are the single doses of pravastatin without an interacting
drug in healthy subjects (or subjects with primary hypercholesterolemia) with
the SLCO1B1 wildtype or a genotype which is not reported (`filter_training`).
The validation data has four parts, each a different question: the
interactions (`INTERACTION_VALIDATION`, the arms with a coadministered drug,
simulated with factors of the transporters which are not fitted), the doses
(`DOSE_VALIDATION`, the repeated doses, which the single doses of the training
predict), the populations (`POPULATION_VALIDATION`, the SLCO1B1 genotypes and
the renal impairment, simulated with the activities and the renal function of
the experiments) and the limitations (`LIMITATION_VALIDATION`, data of a
population, a formulation or a process the model does not describe). The
summaries of data which is fitted one by one are excluded
(`AGGREGATE_MAPPINGS`).
"""

from pkpdsim.fit import mapping_metadata
from pkpdsim.metadata import Coadministration, Dosing, Genotype, Health
from sbmlsim.console import console
from sbmlsim.experiment import SimulationExperiment
from sbmlsim.fit import FitMapping, FitMappingCollection, MappingKind
from sbmlsim.fit.helpers import FitMappings, MappingFilter

from pkdb_models.models.pravastatin import DATA_PATHS, PRAVASTATIN_PATH
from pkdb_models.models.pravastatin.experiments.studies import (
    Becquemont1999,
    Deng2008,
    Gustavson2005,
    Halstenson1992,
    Ho2007,
    Jacobson2004,
    Keskitalo2009,
    Kyrklund2003a,
    Kyrklund2004,
    Maeda2006,
    Mwinyi2004,
    Neuvonen1998,
    Niemi2004,
    Niemi2006,
    Nishizato2003,
    Pan1990,
    Pan1990a,
    Pan1993a,
    Pan2000,
    Sigurbjoernsson1998,
    Singhvi1990,
    Sugimoto2001,
    Wu2012,
)

#: the experiments with fit mappings
EXPERIMENT_CLASSES: list[type[SimulationExperiment]] = [
    Becquemont1999,
    Deng2008,
    Gustavson2005,
    Halstenson1992,
    Ho2007,
    Jacobson2004,
    Keskitalo2009,
    Kyrklund2003a,
    Kyrklund2004,
    Maeda2006,
    Mwinyi2004,
    Neuvonen1998,
    Niemi2004,
    Niemi2006,
    Nishizato2003,
    Pan1990,
    Pan1990a,
    Pan1993a,
    Pan2000,
    Sigurbjoernsson1998,
    Singhvi1990,
    Sugimoto2001,
    Wu2012,
]

#: the keys of fit mappings by study: the keys of the mappings are SIds of their
#: experiment, which two studies can share, so a named mapping is named with
#: its study
type NamedMappings = dict[str, set[str]]

#: mappings which are not fitted, the data is not usable
OUTLIER_MAPPINGS: NamedMappings = {}

#: the validation of the interactions: the arms with a coadministered drug,
#: simulated with the factors of the transporters of `base_experiment` which
#: are not fitted
INTERACTION_VALIDATION: NamedMappings = {
    # fenofibrate, no mechanism in the model (AUC ratio 1.13 in Pan2000)
    "Gustavson2005": {
        "fm_pra40po_Fig1_pra40_fen160_d1",
        "fm_pra40po_Fig1_pra40_fen160_d10",
    },
    "Pan2000": {"fm_pra40po_Fig2_PRA40_RegB"},
    # verapamil and clarithromycin
    "Jacobson2004": {"fm_pra40po_pra_PRA1_VER", "fm_pra40po_pra_PRA4_CLA"},
    # gemfibrozil: OATP1B1 and OAT3
    "Kyrklund2003a": {"fm_pra40po_gem", "fm_pra40po_gem_urine"},
    # rifampicin: OATP1B1
    "Kyrklund2004": {"fm_pra40po_rif", "fm_pra40po_rif_urine"},
    # itraconazole, no effect (pravastatin is no CYP3A4 substrate)
    "Neuvonen1998": {"fm_pra40po_Fig3_itr"},
    # oral contraceptives, no effect in the study
    "Pan1993a": {"fm_pra20po_women_oc"},
    # St John's wort, no effect (AUC ratio 1.03)
    "Sugimoto2001": {"fm_pra20po_Fig2_PRA_STJ"},
    # quercetin: OATP1B1
    "Wu2012": {"fm_pra40po_Fig4_pra40_quercetin"},
}

#: the validation of the doses: the repeated doses, which the single doses of
#: the training predict
DOSE_VALIDATION: NamedMappings = {
    # 5th daily dose after a breakfast, the check of the fixed food effect
    "Gustavson2005": {"fm_pra40po_Fig1_pra40_d5"},
    # day 7 of daily doses (trial 4 after a breakfast)
    "Jacobson2004": {"fm_pra40po_pra_PRA2", "fm_pra40po_pra_PRA4"},
    # twice daily doses, week 4
    "Pan1990": {"fm_pra5po_pra", "fm_pra10po_pra", "fm_pra20po_pra"},
    # 40 mg once daily, day 7
    "Pan1990a": {"fm_pra40po_pra"},
}

#: the validation of the populations: the SLCO1B1 genotypes (`slco1b1_map`)
#: and the renal impairment (`KI__f_renal_function`)
POPULATION_VALIDATION: NamedMappings = {
    # SLCO1B1 *15/*15
    "Deng2008": {"fm_pra40po_Fig2_1515_pra"},
    # renal impairment, the measured creatinine clearance
    "Halstenson1992": {
        "fm_pra20po_Fig1_pra_gr2",
        "fm_pra20po_Fig1_pra_gr3",
        "fm_pra20po_Fig1_pra_gr4",
        "fm_pra20po_Tab2B_pra_gr2_urine",
        "fm_pra20po_Tab2B_pra_gr3_urine",
        "fm_pra20po_Tab2B_pra_gr4_urine",
    },
    # SLCO1B1 c.521 genotypes
    "Ho2007": {"fm_pra40po_Fig1_TC", "fm_pra40po_Fig1_CC"},
    # ABCG2 421CA and AA (enriched in SLCO1B1 521TC), small groups
    "Keskitalo2009": {"fm_pra40po_Fig1_CA", "fm_pra40po_Fig1_AA"},
    # SLCO1B1 haplotypes
    "Mwinyi2004": {
        "fm_pra40po_1a1b_1b1b",
        "fm_pra40po_1a1b_1b1b_urine",
        "fm_pra40po_1a5",
        "fm_pra40po_1a5_urine",
    },
    "Niemi2004": {
        "fm_pra40po_521TC",
        "fm_pra40po_521CC",
        "fm_pra40po_HC15B",
        "fm_pra40po_HC17",
        "fm_pra40po_11187GA",
    },
    # the Japanese cohort: *1b/*1b with the assumed activity of *1b
    "Nishizato2003": {
        "fm_pra10po_Fig1_slco1b1_1b_1b",
        "fm_pra10po_Fig1_slco1b1_1b_15",
        "fm_pra10po_Fig1_slco1b1_15_15",
    },
    # elderly subjects
    "Pan1993a": {"fm_pra20po_elderly_men", "fm_pra20po_elderly_women"},
    # elderly patients with hypercholesterolemia, individual curves
    "Sigurbjoernsson1998": {
        "fm_pra20po_pra_elderly1",
        "fm_pra40po_pra_elderly1",
        "fm_pra40po_pra_elderly2",
    },
}

#: the validation of the limitations of the model: valid data of a population,
#: a formulation or a process the model does not describe, which would distort
#: the fitted parameters of the processes it does describe
LIMITATION_VALIDATION: NamedMappings = {
    # radioenzymatic assay of all active HMG-CoA reductase inhibitors
    "Jacobson2004": {"fm_pra40po_pra_PRA3", "fm_pra40po_pra_PRA3_ITR"},
    # the haplotype ranking of the Japanese cohort (*1b/*15 lowest) contradicts
    # the activities of `slco1b1_map`
    "Maeda2006": {
        "fm_pra10po_Fig1AB_1b1b",
        "fm_pra10po_Fig1AB_1a15",
        "fm_pra10po_Fig1AB_1b15",
    },
    # ABCC2 c.1446CG: the model cannot lower the AUC through MRP2
    "Niemi2006": {"fm_pra40_Fig1_c1446CG"},
    # derived urinary amounts (Ae = CLr * BW * AUC with an assumed weight)
    "Nishizato2003": {
        "fm_pra10po_Tab6b_slco1b1_1a_1a",
        "fm_pra10po_Tab6b_slco1b1_1a_1b",
        "fm_pra10po_Tab6b_slco1b1_1b_1b",
        "fm_pra10po_Tab6b_slco1b1_1b_15",
        "fm_pra10po_Tab6b_slco1b1_15_15",
        "fm_pra10po_Tab6b_slco1b1_1b_16",
    },
    # total 14C in urine and feces, the model has no metabolites
    "Singhvi1990": {
        "fm_pra10iv_total14c_urine",
        "fm_pra10iv_total14c_feces",
        "fm_pra20po_total14c_urine",
        "fm_pra20po_total14c_feces",
    },
}

#: the summaries of data which the fits use one by one, excluded from every
#: fit: a mean of subjects would count the subjects twice
AGGREGATE_MAPPINGS: NamedMappings = {
    # the ethnicities are the subjects of the genotype groups
    "Ho2007": {"fm_pra40po_Fig1_EuropeanAmericans", "fm_pra40po_Fig1_AfricanAmericans"},
    # the non-carriers of a haplotype are the cohort of the genotype groups
    "Niemi2004": {"fm_pra40po_11187GG", "fm_pra40po_NC15B", "fm_pra40po_NC17"},
    # the cohort of Niemi2004 again
    "Niemi2006": {
        "fm_pra40_Fig1_no_SLCO1B1_17_c1446CC",
        "fm_pra40_Fig1_SLCO1B1_17",
    },
}

#: the validation data by the question it answers
VALIDATION_QUESTIONS: dict[str, NamedMappings] = {
    "interactions": INTERACTION_VALIDATION,
    "doses": DOSE_VALIDATION,
    "populations": POPULATION_VALIDATION,
    "limitations": LIMITATION_VALIDATION,
}

#: the validation data
VALIDATION_MAPPINGS: NamedMappings = {
    study: set().union(
        *(mappings.get(study, set()) for mappings in VALIDATION_QUESTIONS.values())
    )
    for mappings in VALIDATION_QUESTIONS.values()
    for study in mappings
}

#: health of the training data
TRAINING_HEALTH: frozenset[Health] = frozenset(
    {Health.HEALTHY, Health.NR, Health.PRIMARY_HYPERCHOLESTEROLEMIA}
)

#: genotypes of the training data: not reported, the SLCO1B1 wildtype or the
#: wildtype of a transporter the model does not have (ABCG2)
TRAINING_GENOTYPES: frozenset[Genotype] = frozenset(
    {
        Genotype.NR,
        Genotype.SLCO1B1_WILD_TYPE,
        Genotype.SLCO1B1_521TT,
        Genotype.ABCG2_421CC,
    }
)


def study(fit_mapping: FitMapping) -> str:
    """Get the study of a fit mapping, the id of its experiment."""
    return fit_mapping.reference.experiment.sid


def named(
    mappings: NamedMappings, fit_mapping_key: str, fit_mapping: FitMapping
) -> bool:
    """Check whether a fit mapping is one of the named mappings of its study."""
    return fit_mapping_key in mappings.get(study(fit_mapping), set())


def check_named(mappings: NamedMappings, fit_mappings: FitMappings) -> None:
    """Check that the named mappings are fit mappings of their studies.

    Raises:
        ValueError: for a study which is no experiment, or a key which is no fit
            mapping of its study.
    """
    for sid, keys in mappings.items():
        experiment = fit_mappings.experiments.get(sid)
        if experiment is None:
            raise ValueError(f"'{sid}' is no experiment of the fits.")
        if unknown := sorted(keys - set(experiment._fit_mappings)):
            raise ValueError(f"'{unknown}' are no fit mappings of '{sid}'.")


def filter_aggregates(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """No summaries of data which is fitted one by one, see `AGGREGATE_MAPPINGS`."""
    return not named(AGGREGATE_MAPPINGS, fit_mapping_key, fit_mapping)


def filter_training(fit_mapping_key: str, fit_mapping: FitMapping) -> bool:
    """The training data and the named validation data.

    Single doses without an interacting drug in healthy subjects (or subjects
    with primary hypercholesterolemia) with the wildtype or a genotype which is
    not reported; the named validation data passes, every other mapping is
    excluded.
    """
    if named(VALIDATION_MAPPINGS, fit_mapping_key, fit_mapping):
        return True
    metadata = mapping_metadata(fit_mapping)
    return (
        metadata.dosing == Dosing.SINGLE
        and metadata.coadministration == Coadministration.NONE
        and metadata.health in TRAINING_HEALTH
        and metadata.genotype in TRAINING_GENOTYPES
    )


def mapping_collections(
    filters: MappingFilter | list[MappingFilter],
    validation: NamedMappings = VALIDATION_MAPPINGS,
) -> dict[str, list[FitMappingCollection]]:
    """Select the data of a fit from the fit mappings of the studies.

    The filters select the training data, the mappings which fail them are
    excluded, and so are the summaries of data which is fitted one by one
    (`AGGREGATE_MAPPINGS`). The outliers are `OUTLIER_MAPPINGS`, the validation
    data is `VALIDATION_MAPPINGS`. Neither kind enters the cost; both are
    simulated and evaluated with the training data, so a report says how the
    fitted parameters describe data they were not fitted on.

    Args:
        filters: filters of the training data.
        validation: the keys of the validation data by study.

    Returns:
        The fit mapping collections of all kinds by experiment id.

    Raises:
        ValueError: if an outlier is a mapping of no study or of several.
    """
    fit_mappings = FitMappings(
        experiment_classes=EXPERIMENT_CLASSES,
        base_path=PRAVASTATIN_PATH,
        data_path=DATA_PATHS,
    )
    for mappings in [OUTLIER_MAPPINGS, AGGREGATE_MAPPINGS, validation]:
        check_named(mappings, fit_mappings)
    # sbmlsim selects the outliers by their keys alone, which must name one
    # mapping of all studies
    outliers = {key for keys in OUTLIER_MAPPINGS.values() for key in keys}
    for key in outliers:
        studies = [
            sid
            for sid, experiment in fit_mappings.experiments.items()
            if key in experiment._fit_mappings
        ]
        if len(studies) != 1:
            raise ValueError(f"The outlier '{key}' is a mapping of {studies}.")
    selection = fit_mappings.select(
        filters=[
            *(filters if isinstance(filters, list) else [filters]),
            filter_aggregates,
        ],
        outliers=outliers,
        validation=lambda key, fit_mapping: named(validation, key, fit_mapping),
        print_info=False,
    )
    # the counts per experiment and kind, not the single mappings
    selection.print(detail=False)
    # the validation mappings by the question they answer
    selected = {
        (sid, key)
        for sid, kinds in selection.kinds.items()
        for key, kind in kinds.items()
        if kind is MappingKind.VALIDATION
    }

    def pairs(mappings: NamedMappings) -> set[tuple[str, str]]:
        return {(sid, key) for sid, keys in mappings.items() for key in keys}

    console.print(
        "validation: "
        + ", ".join(
            f"{len(selected & pairs(mappings))} {question}"
            for question, mappings in VALIDATION_QUESTIONS.items()
        )
    )
    return selection.collections


def f_collections_pk() -> dict[str, list[FitMappingCollection]]:
    """Pharmacokinetic data: the training data and the validation data."""
    return mapping_collections([filter_training])


if __name__ == "__main__":
    console.rule(title=f_collections_pk.__name__, align="left", style="white")
    f_collections_pk()
