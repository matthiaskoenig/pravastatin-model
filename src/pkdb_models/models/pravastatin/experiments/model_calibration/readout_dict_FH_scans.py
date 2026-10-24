"""The time to the steady state and the quantities of the calibrations.

The calibrations of the cholesterol part of the model (`FHCalibration`,
`LDLCUtilizationCalibration`) simulate into the steady state; a quantity of
`readout_dict` is read from the results with its selection.
"""

from typing import TypedDict


class Readout(TypedDict):
    """A quantity of the figures: its selection, labels, color and units."""

    sid: str
    y_label: str
    label: str
    color: str
    #: unit of the figures
    unit: str
    #: unit of the selection in the model
    model_unit: str


#: the time to the steady state of a FH type [weeks]
time_FH_steadystate: int = 52

#: the quantities of the figures
readout_dict: dict[str, Readout] = {
    "plasma ldlc": {
        "sid": "[Cve_ldlc]",
        "y_label": "Plasma LDL-C",
        "label": "Plasma LDL-C",
        "color": "black",
        "unit": "nM",
        "model_unit": "nmol/l",
    },
}
