"""The tolerances of the integrator for the pravastatin model."""

from sbmlsim.model.tolerances import AbsoluteTolerance


def absolute_tolerance(value: float, species: float) -> AbsoluteTolerance:
    """Get the absolute tolerance of the integrator for the pravastatin model.

    Pravastatin is dosed in mg, about 0.1 mmole: its plasma concentrations are
    1e-5 mM and below, the concentrations of the cholesterol part 1e-3 - 10 mM.
    The species get an absolute tolerance of the scale of the
    pharmacokinetics, the other states (the oral and intravenous dose and the
    cumulative dose, which are rate rules in mg) `value`. With the tolerance of
    the simulations (1e-10) for all states the plasma concentrations of
    pravastatin differed by 8e-6 from the tight integration, with 1e-12 for
    the species by 2e-7; with the tolerance of the fits (1e-6) for all states
    by 6e-3, with 1e-10 for the species by 2e-5.

    Args:
        value: tolerance of every other state.
        species: tolerance of the amounts and concentrations of the species.

    Returns:
        The absolute tolerance per kind of state.
    """
    return AbsoluteTolerance(amount=species, concentration=species, other=value)


#: the absolute tolerance of the simulation experiments
ABSOLUTE_TOLERANCE = absolute_tolerance(1e-10, species=1e-12)
