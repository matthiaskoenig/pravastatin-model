"""Templates of the pravastatin models: units, model units and creators."""

from pkpdsim.templates import creators as creators_generic
from sbmlutils.factory import Creator, ModelUnits, UnitDefinition, Units


class U(Units):
    """UnitDefinitions."""

    mmole = UnitDefinition("mmole")
    min = UnitDefinition("min")
    mg = UnitDefinition("mg")
    per_min = UnitDefinition("per_min", "1/min")
    per_min_l = UnitDefinition("per_min_l", "1/min/liter")
    m2 = UnitDefinition("m2", "meter^2")
    mM = UnitDefinition("mM", "mmole/liter")
    mmole_per_min = UnitDefinition("mmole_per_min", "mmole/min")
    mmole_per_min_l = UnitDefinition("mmole_per_min_l", "mmole/min/liter")
    g_per_mole = UnitDefinition("g_per_mole", "g/mole")
    l_per_min = UnitDefinition("l_per_min", "l/min")
    l_per_min_mmole = UnitDefinition("l_per_min_mmole", "l/min/mmole")
    ml_per_min = UnitDefinition("ml_per_min", "ml/min")
    ml_per_l = UnitDefinition("ml_per_l", "ml/l")
    l_per_ml = UnitDefinition("l_per_ml", "l/ml")


model_units = ModelUnits(
    time=U.min,
    extent=U.mmole,
    substance=U.mmole,
    length=U.meter,
    area=U.m2,
    volume=U.liter,
)

creators = [
    Creator(
        familyName="Leal Pujol",
        givenName="Helen",
        email="lepujolh@hu-berlin.de",
        organization="Humboldt-University Berlin, Institute for Theoretical Biology",
    ),
    *creators_generic,
]
