"""All Models used by the library are frozen, slotted dataclasses."""

from __future__ import annotations

import dataclasses
import json
from collections.abc import Sequence
from typing import Any
from typing import NoReturn

from .enums import Color
from .enums import Measure
from .enums import Phase
from .enums import State
from .exceptions import ModelBuildError

__all__ = [
    "Balance",
    "Project",
    "Stat",
    "Tag",
    "Tally",
]


def _handle_build_error(exc: Exception, data: dict[str, Any], name: str) -> NoReturn:
    """
    Helpful bug reporting output for model building errors.

    Raises:
        ModelBuildError
    """
    raise ModelBuildError(
        data_string=json.dumps(data),
        model_name=name,
        exception_type=str(type(exc)),
        exception_str=str(exc),
    ) from exc


@dataclasses.dataclass(frozen=True, slots=True)
class Balance:
    """Balance values for Project models. These are **optional** values when building."""

    word: int
    time: int
    page: int
    chapter: int
    scene: int
    line: int


@dataclasses.dataclass(frozen=True, slots=True)
class Tally:
    """Tally model built from the API response."""

    id: int
    uuid: int
    created_at: str
    updated_at: str
    state: State
    owner_id: str
    date: str
    measure: Measure
    count: int
    note: str
    work_id: int
    work: ProjectStub
    tags: Sequence[Tag]

    @classmethod
    def build(cls, data: dict[str, Any]) -> Tally:
        """Build a Project model from the API response data."""
        try:
            return cls(
                id=data["id"],
                uuid=data["uuid"],
                created_at=data["createdAt"],
                updated_at=data["updatedAt"],
                state=State(data["state"]),
                owner_id=data["ownerId"],
                date=data["date"],
                measure=Measure(data["measure"]),
                count=data["count"],
                note=data["note"],
                work_id=data["workId"],
                work=ProjectStub.build(data["work"]),
                tags=[Tag.build(tag) for tag in data["tags"]],
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class Project:
    """Project model built from the API response."""

    id: int
    uuid: str
    created_at: str
    updated_at: str
    state: State
    owner_id: int
    title: str
    description: str
    phase: Phase
    starting_balance: Balance
    cover: str | None
    starred: bool
    display_on_profile: bool
    totals: Balance
    last_updated: str | None

    @classmethod
    def build(cls, data: dict[str, Any]) -> Project:
        """Build a Project model from the API response data."""
        try:
            return cls(
                id=data["id"],
                uuid=data["uuid"],
                created_at=data["createdAt"],
                updated_at=data["updatedAt"],
                state=State(data["state"]),
                owner_id=data["ownerId"],
                title=data["title"],
                description=data["description"],
                phase=Phase(data["phase"]),
                starting_balance=Balance(
                    word=data["startingBalance"].get("word", 0),
                    time=data["startingBalance"].get("time", 0),
                    page=data["startingBalance"].get("page", 0),
                    chapter=data["startingBalance"].get("chapter", 0),
                    scene=data["startingBalance"].get("scene", 0),
                    line=data["startingBalance"].get("line", 0),
                ),
                cover=data["cover"],
                starred=data.get("starred", False),
                display_on_profile=data.get("displayOnProfile", False),
                totals=Balance(
                    word=data["totals"].get("word", 0),
                    time=data["totals"].get("time", 0),
                    page=data["totals"].get("page", 0),
                    chapter=data["totals"].get("chapter", 0),
                    scene=data["totals"].get("scene", 0),
                    line=data["totals"].get("line", 0),
                ),
                last_updated=data["lastUpdated"],
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class ProjectStub:
    """ProjectStub model built from the API response."""

    id: int
    uuid: str
    created_at: str
    updated_at: str
    state: State
    owner_id: int
    title: str
    description: str
    phase: Phase
    starting_balance: Balance
    cover: str | None
    starred: bool
    display_on_profile: bool

    @classmethod
    def build(cls, data: dict[str, Any]) -> ProjectStub:
        """Build a Project model from the API response data."""
        try:
            return cls(
                id=data["id"],
                uuid=data["uuid"],
                created_at=data["createdAt"],
                updated_at=data["updatedAt"],
                state=State(data["state"]),
                owner_id=data["ownerId"],
                title=data["title"],
                description=data["description"],
                phase=Phase(data["phase"]),
                starting_balance=Balance(
                    word=data["startingBalance"].get("word", 0),
                    time=data["startingBalance"].get("time", 0),
                    page=data["startingBalance"].get("page", 0),
                    chapter=data["startingBalance"].get("chapter", 0),
                    scene=data["startingBalance"].get("scene", 0),
                    line=data["startingBalance"].get("line", 0),
                ),
                cover=data["cover"],
                starred=data.get("starred", False),
                display_on_profile=data.get("displayOnProfile", False),
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class Tag:
    """Tag model build from API response."""

    id: int
    uuid: str
    created_at: str
    updated_at: str
    state: State
    owner_id: int
    name: str
    color: Color

    @classmethod
    def build(cls, data: dict[str, Any]) -> Tag:
        """Build a Tag model from the API response data."""
        try:
            return cls(
                id=data["id"],
                uuid=data["uuid"],
                created_at=data["createdAt"],
                updated_at=data["updatedAt"],
                state=State(data["state"]),
                owner_id=data["ownerId"],
                name=data["name"],
                color=Color(data["color"]),
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class Stat:
    """Stat model build from API response."""

    date: str
    counts: Balance

    @classmethod
    def build(cls, data: dict[str, Any]) -> Stat:
        """Build a Stat model from the API response data."""
        try:
            return cls(
                date=data["date"],
                counts=Balance(
                    word=data["counts"].get("word", 0),
                    time=data["counts"].get("time", 0),
                    page=data["counts"].get("page", 0),
                    chapter=data["counts"].get("chapter", 0),
                    scene=data["counts"].get("scene", 0),
                    line=data["counts"].get("line", 0),
                ),
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)
