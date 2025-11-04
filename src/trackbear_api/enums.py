"""All Enums used by the library."""

from __future__ import annotations

import enum


class Phase(str, enum.Enum):
    PLANNING = "planning"
    OUTLINING = "outlining"
    DRAFTING = "drafting"
    REVISING = "revising"
    ON_HOLD = "on hold"
    FINISHED = "finished"
    ABANDONED = "abandoned"


class State(str, enum.Enum):
    ACTIVE = "active"
    DELETED = "deleted"


class Color(str, enum.Enum):
    DEFAULT = "default"
    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    BROWN = "brown"
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"
