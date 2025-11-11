"""All Models used by the library are frozen, slotted dataclasses."""

from __future__ import annotations

import dataclasses
import json
from collections.abc import Sequence
from typing import Any
from typing import NoReturn

from . import enums
from . import exceptions

__all__ = [
    "Balance",
    "Cadence",
    "Error",
    "Goal",
    "HabitParameter",
    "Project",
    "ProjectStub",
    "Stat",
    "Tag",
    "Tally",
    "TargetParameter",
    "Threshold",
]


def _handle_build_error(exc: Exception, data: dict[str, Any], name: str) -> NoReturn:
    """
    Helpful bug reporting output for model building errors.

    Raises:
        ModelBuildError
    """
    raise exceptions.ModelBuildError(
        data_string=json.dumps(data),
        model_name=name,
        exception_type=str(type(exc)),
        exception_str=str(exc),
    ) from exc


@dataclasses.dataclass(slots=True, frozen=True)
class TrackBearResponse:
    """
    TrackBear API response Model.

    Always check `success` before processing additional attributes.

    When `success` is True: `data` will be available for processing

    When `success` is False: `code` and `message` will be available for processing
    """

    success: bool
    data: Any
    error: Error
    status_code: int
    remaining_requests: int
    rate_reset: int

    @classmethod
    def build(
        cls,
        response: dict[str, Any],
        remaining_requests: int,
        rate_reset: int,
        status_code: int,
    ) -> TrackBearResponse:
        """Bulid a model from request response data."""
        success = response["success"]

        return cls(
            success=success,
            data=response["data"] if success else "",
            error=Error(
                code=response["error"]["code"] if not success else "",
                message=response["error"]["message"] if not success else "",
            ),
            status_code=status_code,
            remaining_requests=remaining_requests,
            rate_reset=rate_reset,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class Error:
    """Sub-model of TrackBearResponse"""

    code: str
    message: str


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
    state: enums.State
    owner_id: str
    date: str
    measure: enums.Measure
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
                state=enums.State(data["state"]),
                owner_id=data["ownerId"],
                date=data["date"],
                measure=enums.Measure(data["measure"]),
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
    state: enums.State
    owner_id: int
    title: str
    description: str
    phase: enums.Phase
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
                state=enums.State(data["state"]),
                owner_id=data["ownerId"],
                title=data["title"],
                description=data["description"],
                phase=enums.Phase(data["phase"]),
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
    state: enums.State
    owner_id: int
    title: str
    description: str
    phase: enums.Phase
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
                state=enums.State(data["state"]),
                owner_id=data["ownerId"],
                title=data["title"],
                description=data["description"],
                phase=enums.Phase(data["phase"]),
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
class Threshold:
    """Sub-model for TargetParameter and HabitParameter. Defines thresholds for a target goal."""

    measure: enums.Measure
    count: int


@dataclasses.dataclass(frozen=True, slots=True)
class Cadence:
    """Sub-model for TargetParameter and HabitParameter."""

    unit: enums.HabitUnit
    period: int


@dataclasses.dataclass(frozen=True, slots=True)
class TargetParameter:
    """Defines threshold for a target goal."""

    threshold: Threshold


@dataclasses.dataclass(frozen=True, slots=True)
class HabitParameter:
    """Defines cadence with optional threshold for a habit goal."""

    cadence: Cadence
    threshold: Threshold | None


@dataclasses.dataclass(frozen=True, slots=True)
class Goal:
    """Goal model built from API repsonse."""

    id: int
    uuid: str
    created_at: str
    updated_at: str
    state: enums.State
    owner_id: str
    title: str
    description: str
    type: enums.GoalType
    parameters: HabitParameter | TargetParameter
    start_date: str
    end_date: str
    work_ids: list[int]
    tag_ids: list[int]
    starred: bool = False
    display_on_profile: bool = False

    @classmethod
    def build(cls, data: dict[str, Any]) -> Goal:
        """Build a Project model from the API response data."""
        try:
            type = data["type"]
            parameters = data["parameters"]
            parameter_object: HabitParameter | TargetParameter

            if type == enums.GoalType.HABIT and parameters["threshold"] is not None:
                parameter_object = HabitParameter(
                    cadence=Cadence(
                        unit=enums.HabitUnit(parameters["cadence"]["unit"]),
                        period=parameters["cadence"]["period"],
                    ),
                    threshold=Threshold(
                        measure=enums.Measure(parameters["threshold"]["measure"]),
                        count=parameters["threshold"]["count"],
                    ),
                )

            elif type == enums.GoalType.HABIT and parameters["threshold"] is None:
                parameter_object = HabitParameter(
                    cadence=Cadence(
                        unit=enums.HabitUnit(parameters["cadence"]["unit"]),
                        period=parameters["cadence"]["period"],
                    ),
                    threshold=None,
                )

            else:
                parameter_object = TargetParameter(
                    threshold=Threshold(
                        measure=enums.Measure(parameters["threshold"]["measure"]),
                        count=parameters["threshold"]["count"],
                    )
                )

            return cls(
                id=data["id"],
                uuid=data["uuid"],
                created_at=data["createdAt"],
                updated_at=data["updatedAt"],
                state=enums.State(data["state"]),
                owner_id=data["ownerId"],
                title=data["title"],
                description=data["description"],
                type=enums.GoalType(data["type"]),
                parameters=parameter_object,
                start_date=data["startDate"],
                end_date=data["endDate"],
                work_ids=data["workIds"],
                tag_ids=data["tagIds"],
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
    state: enums.State
    owner_id: int
    name: str
    color: enums.Color

    @classmethod
    def build(cls, data: dict[str, Any]) -> Tag:
        """Build a Tag model from the API response data."""
        try:
            return cls(
                id=data["id"],
                uuid=data["uuid"],
                created_at=data["createdAt"],
                updated_at=data["updatedAt"],
                state=enums.State(data["state"]),
                owner_id=data["ownerId"],
                name=data["name"],
                color=enums.Color(data["color"]),
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
