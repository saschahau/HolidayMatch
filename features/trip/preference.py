"""Person class that represents a person."""
from dataclasses import dataclass, field
from typing import ClassVar

from lib.enums import PreferenceType

@dataclass
class Preference:
    type: PreferenceType
    preference: tuple = field(default_factory=tuple)

@dataclass
class RegionPreference(Preference):
    """"""
    CHOICES: ClassVar[dict] = {
        0: "No preference",
        1: "Europe",
        2: "Middle East",
        3: "Asia",
        4: "North America",
        5: "South America",
        6: "Australia",
    }
    type: PreferenceType = PreferenceType.REGION

@dataclass
class BudgetPreference(Preference):
    """Contains the budget options that are presented and the selected preference."""
    CHOICES: ClassVar[dict] = {
        0: "No preference",
        1: "< 500",
        2: "500 < 1000",
        3: "1000 < 2500",
        4: "2500 < 5000",
        5: "< 5000",
    }
    type: PreferenceType = PreferenceType.BUDGET

@dataclass
class TransportationPreference(Preference):
    CHOICES: ClassVar[dict] = {
        0: "No preference",
        1: "Train",
        2: "Airplane"
    }
    type: PreferenceType = PreferenceType.TRANSPORTATION