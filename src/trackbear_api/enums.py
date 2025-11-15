"""All Enums used by the library."""

from __future__ import annotations

import enum

__all__ = [
    "Phase",
    "State",
    "TagColor",
    "Measure",
    "MemberColor",
    "HabitUnit",
    "GoalType",
]


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


class TagColor(str, enum.Enum):
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


class MemberColor(str, enum.Enum):
    AUTO = "auto"
    RED = "red"
    ORANGE = "orange"
    AMBER = "amber"
    YELLOW = "yellow"
    LIME = "lime"
    GREEN = "green"
    TEAL = "teal"
    CYAN = "cyan"
    SKY = "sky"
    BLUE = "blue"
    VIOLET = "violet"
    PURPLE = "purple"
    FUCHIA = "fuchia"
    PINK = "pink"
    ROSE = "rose"
    GRAY = "gray"


class Measure(str, enum.Enum):
    WORD = "word"
    TIME = "time"
    PAGE = "page"
    CHAPTER = "chapter"
    SCENE = "scene"
    LINE = "line"


class HabitUnit(str, enum.Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class GoalType(str, enum.Enum):
    TARGET = "target"
    HABIT = "habit"
