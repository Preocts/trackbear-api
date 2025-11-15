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
    "GoalStub",
    "HabitParameter",
    "Leaderboard",
    "LeaderboardExtended",
    "LeaderboardMember",
    "Member",
    "Participant",
    "Project",
    "ProjectStub",
    "Stat",
    "Tag",
    "Tally",
    "TallyStub",
    "TargetParameter",
    "Team",
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
    """Tally model."""

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
        """Build a Tally model from the API response data."""
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
    """Project model."""

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
    """ProjectStub model."""

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
        """Build a ProjectStub model from the API response data."""
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
    """Goal model."""

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
    start_date: str | None
    end_date: str | None
    work_ids: list[int]
    tag_ids: list[int]
    starred: bool = False
    display_on_profile: bool = False

    @classmethod
    def build(cls, data: dict[str, Any]) -> Goal:
        """Build a Goal model from the API response data."""
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
    """Tag model."""

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
    """Stat model."""

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


@dataclasses.dataclass(frozen=True, slots=True)
class Member:
    """Member model."""

    id: int
    uuid: str
    state: enums.State
    display_name: str
    avatar: str | None
    color: str | None
    is_participant: bool
    is_owner: bool

    @classmethod
    def build(cls, data: dict[str, Any]) -> Member:
        """Build a Member model from the API response data."""
        try:
            return cls(
                id=data["id"],
                uuid=data["uuid"],
                state=data["state"],
                display_name=data["displayName"],
                avatar=data["avatar"],
                color=data["color"],
                is_participant=data["isParticipant"],
                is_owner=data["isOwner"],
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class Team:
    """Team model."""

    id: int
    uuid: str
    created_at: str
    updated_at: str
    board_id: str
    name: str
    color: str

    @classmethod
    def build(cls, data: dict[str, Any]) -> Team:
        """Build a Team model from the API response data."""
        try:
            return cls(
                id=data["id"],
                uuid=data["uuid"],
                created_at=data["createdAt"],
                updated_at=data["updatedAt"],
                board_id=data["boardId"],
                name=data["name"],
                color=data["color"],
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class LeaderboardMember:
    """Sub-model for LeaderboardExtended."""

    id: int
    display_name: str
    avatar: str
    is_participant: bool
    is_owner: bool
    user_uuid: str


@dataclasses.dataclass(frozen=True, slots=True)
class LeaderboardExtended:
    """LeaderboardExtended model."""

    id: int
    uuid: str
    created_at: str
    updated_at: str
    state: enums.State
    owner_id: int
    title: str
    description: str
    start_date: str | None
    end_date: str | None
    individual_goal_mode: bool
    fundraiser_mode: bool
    measures: list[enums.Measure]
    goal: Balance
    is_joinable: bool
    teams: list[Team]
    members: list[LeaderboardMember]
    starred: bool = False

    @classmethod
    def build(cls, data: dict[str, Any]) -> LeaderboardExtended:
        """Build a LeaderboardExtended model from the API response data."""
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
                start_date=data["startDate"],
                end_date=data["endDate"],
                individual_goal_mode=data["individualGoalMode"],
                fundraiser_mode=data["fundraiserMode"],
                measures=[enums.Measure(measure) for measure in data["measures"]],
                goal=Balance(
                    word=data["goal"].get("word", 0),
                    time=data["goal"].get("time", 0),
                    page=data["goal"].get("page", 0),
                    chapter=data["goal"].get("chapter", 0),
                    scene=data["goal"].get("scene", 0),
                    line=data["goal"].get("line", 0),
                ),
                is_joinable=data["isJoinable"],
                teams=[
                    Team(
                        id=team["id"],
                        uuid=team["uuid"],
                        created_at=team["createdAt"],
                        updated_at=team["updatedAt"],
                        board_id=team["boardId"],
                        name=team["name"],
                        color=team["color"],
                    )
                    for team in data["teams"]
                ],
                members=[
                    LeaderboardMember(
                        id=member["id"],
                        display_name=member["displayName"],
                        avatar=member["avatar"],
                        is_participant=member["isParticipant"],
                        is_owner=member["isOwner"],
                        user_uuid=member["userUuid"],
                    )
                    for member in data["members"]
                ],
                starred=data["starred"],
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class Leaderboard:
    """Leaderboard model."""

    id: int
    uuid: str
    created_at: str
    updated_at: str
    state: enums.State
    owner_id: int
    title: str
    description: str
    start_date: str | None
    end_date: str | None
    individual_goal_mode: bool
    fundraiser_mode: bool
    measures: list[enums.Measure]
    goal: Balance
    is_joinable: bool
    starred: bool = False

    @classmethod
    def build(cls, data: dict[str, Any]) -> Leaderboard:
        """Build a Leaderboard model from the API response data."""
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
                start_date=data["startDate"],
                end_date=data["endDate"],
                individual_goal_mode=data["individualGoalMode"],
                fundraiser_mode=data["fundraiserMode"],
                measures=[enums.Measure(measure) for measure in data["measures"]],
                goal=Balance(
                    word=data["goal"].get("word", 0),
                    time=data["goal"].get("time", 0),
                    page=data["goal"].get("page", 0),
                    chapter=data["goal"].get("chapter", 0),
                    scene=data["goal"].get("scene", 0),
                    line=data["goal"].get("line", 0),
                ),
                is_joinable=data["isJoinable"],
                starred=data["starred"],
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)


@dataclasses.dataclass(frozen=True, slots=True)
class TallyStub:
    """Sub-model of Participant."""

    uuid: str
    date: str
    measure: enums.Measure
    count: int


@dataclasses.dataclass(frozen=True, slots=True)
class GoalStub:
    """Sub-model of Participant."""

    measure: enums.Measure
    count: int


@dataclasses.dataclass(frozen=True, slots=True)
class Participant:
    """Participant model."""

    id: int
    uuid: str
    display_name: str
    avatar: str | None
    color: enums.Color | None
    goal: GoalStub | None
    tallies: Sequence[TallyStub]

    @classmethod
    def build(cls, data: dict[str, Any]) -> Participant:
        """Build a Participant model from the API response data."""
        try:

            return cls(
                id=data["id"],
                uuid=data["uuid"],
                display_name=data["displayName"],
                avatar=data["avatar"],
                color=enums.Color(data["color"]) if data["color"] is not None else None,
                goal=(
                    GoalStub(
                        measure=enums.Measure(data["goal"]["measure"]),
                        count=data["goal"]["count"],
                    )
                    if data["goal"] is not None
                    else None
                ),
                tallies=[
                    TallyStub(
                        uuid=tally["uuid"],
                        date=tally["date"],
                        measure=tally["measure"],
                        count=tally["count"],
                    )
                    for tally in data["tallies"]
                ],
            )

        except (KeyError, ValueError) as exc:
            _handle_build_error(exc, data, cls.__name__)
