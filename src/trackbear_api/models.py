"""All Models used by the library are frozen, slotted dataclasses."""

from __future__ import annotations

import dataclasses
import json
from typing import Any
from typing import Literal
from typing import NoReturn

from .exceptions import ModelBuildError

__all__ = [
    "Balance",
    "Project",
]


def _handle_build_error(exc: Exception, data: dict[str, Any], name: str) -> NoReturn:
    """
    Helpful bug reporting output for model building errors.

    Raises:
        ModelBuildError
    """
    raise ModelBuildError(json.dumps(data), name) from exc


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
class Project:
    """Project model built from the API response."""

    id: int
    uuid: str
    created_at: str
    updated_at: str
    state: Literal["active", "deleted"]
    owner_id: int
    title: str
    description: str
    phase: Literal[
        "planning",
        "outlining",
        "drafting",
        "revising",
        "on hold",
        "finished",
        "abandoned",
    ]
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
                state=data["state"],
                owner_id=data["ownerId"],
                title=data["title"],
                description=data["description"],
                phase=data["phase"],
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

        except KeyError as exc:
            _handle_build_error(exc, data, cls.__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class ProjectStub:
    """ProjectStub model built from the API response."""

    id: int
    uuid: str
    created_at: str
    updated_at: str
    state: Literal["active", "deleted"]
    owner_id: int
    title: str
    description: str
    phase: Literal[
        "planning",
        "outlining",
        "drafting",
        "revising",
        "on hold",
        "finished",
        "abandoned",
    ]
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
                state=data["state"],
                owner_id=data["ownerId"],
                title=data["title"],
                description=data["description"],
                phase=data["phase"],
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

        except KeyError as exc:
            _handle_build_error(exc, data, cls.__name__)
