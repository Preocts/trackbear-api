"""
Unhappy path tests for all client methods. Includes all raised exception failures.

All tests are run through the TrackBearClient which is the public API for the library.

Tests in this collection focus on the error handling and successful model building.
There is no focus on the underlying APIClient behavior as that is tested in the
trackbearclient_test.py collection.
"""

from __future__ import annotations

import json
from typing import Any
from typing import TypeVar

import pytest
import responses

from trackbear_api import TrackBearClient
from trackbear_api import exceptions

from . import test_parameters

ModelType = TypeVar("ModelType")


FAILURE_RESPONSE = {
    "success": False,
    "error": {
        "code": "SOME_ERROR_CODE",
        "message": "A human-readable error message",
    },
}


def get_client_attribute(client: TrackBearClient, provider_method: str) -> Any:
    """Return the attribute given through dot-notation of the client."""
    method_to_call = getattr(client, provider_method.split(".")[0])
    for attribute in provider_method.split(".")[1:]:
        method_to_call = getattr(method_to_call, attribute)

    return method_to_call


@pytest.mark.parametrize(
    "provider_method,kwargs,url,http_method",
    (
        (
            "project.list",
            {},
            "https://trackbear.app/api/v1/project",
            "GET",
        ),
        ("project.get", {"project_id": 123}, "https://trackbear.app/api/v1/project/123", "GET"),
        (
            "project.save",
            {"title": "mock", "description": "mock", "phase": "planning"},
            "https://trackbear.app/api/v1/project",
            "POST",
        ),
        (
            "project.delete",
            {"project_id": 123},
            "https://trackbear.app/api/v1/project/123",
            "DELETE",
        ),
        ("goal.list", {}, "https://trackbear.app/api/v1/goal", "GET"),
        ("goal.get", {"goal_id": 123}, "https://trackbear.app/api/v1/goal/123", "GET"),
        (
            "goal.save_target",
            test_parameters.GOAL_SAVE_TARGET_KWARGS,
            "https://trackbear.app/api/v1/goal",
            "POST",
        ),
        (
            "goal.save_habit",
            test_parameters.GOAL_SAVE_HABIT_KWARGS,
            "https://trackbear.app/api/v1/goal",
            "POST",
        ),
        ("goal.delete", {"goal_id": 123}, "https://trackbear.app/api/v1/goal/123", "DELETE"),
        ("stat.list", {}, "https://trackbear.app/api/v1/stats/days", "GET"),
        ("tag.list", {}, "https://trackbear.app/api/v1/tag", "GET"),
        ("tag.get", {"tag_id": 123}, "https://trackbear.app/api/v1/tag/123", "GET"),
        ("tag.save", {"name": "mock", "color": "blue"}, "https://trackbear.app/api/v1/tag", "POST"),
        ("tag.delete", {"tag_id": 123}, "https://trackbear.app/api/v1/tag/123", "DELETE"),
        ("tally.list", {}, "https://trackbear.app/api/v1/tally", "GET"),
        ("tally.get", {"tally_id": 123}, "https://trackbear.app/api/v1/tally/123", "GET"),
        (
            "tally.save",
            {"work_id": 123, "date": "2025-01-01", "measure": "word", "count": 0},
            "https://trackbear.app/api/v1/tally",
            "POST",
        ),
        ("tally.delete", {"tally_id": 123}, "https://trackbear.app/api/v1/tally/123", "DELETE"),
        ("leaderboard.list", {}, "https://trackbear.app/api/v1/leaderboard", "GET"),
        (
            "leaderboard.list_participants",
            {"board_uuid": "uuid1234"},
            "https://trackbear.app/api/v1/leaderboard/uuid1234/participants",
            "GET",
        ),
        (
            "leaderboard.get",
            {"board_uuid": "uuid1234"},
            "https://trackbear.app/api/v1/leaderboard/uuid1234",
            "GET",
        ),
        (
            "leaderboard.save",
            test_parameters.LEADERBOARD_SAVE_SIMPLE_KWARGS,
            "https://trackbear.app/api/v1/leaderboard",
            "POST",
        ),
        (
            "leaderboard.save_star",
            {"board_uuid": "uuid1234", "starred": True},
            "https://trackbear.app/api/v1/leaderboard/uuid1234/star",
            "PATCH",
        ),
        (
            "leaderboard.delete",
            {"board_uuid": "uuid1234"},
            "https://trackbear.app/api/v1/leaderboard/uuid1234",
            "DELETE",
        ),
        (
            "leaderboard.team.list",
            {"board_uuid": "uuid1234"},
            "https://trackbear.app/api/v1/leaderboard/uuid1234/teams",
            "GET",
        ),
        (
            "leaderboard.team.get",
            {"board_uuid": "uuid1234", "team_id": 123},
            "https://trackbear.app/api/v1/leaderboard/uuid1234/teams/123",
            "GET",
        ),
        (
            "leaderboard.team.save",
            test_parameters.TEAM_SAVE_KWARGS,
            "https://trackbear.app/api/v1/leaderboard/uuid1234/teams",
            "POST",
        ),
        (
            "leaderboard.team.delete",
            {"board_uuid": "uuid1234", "team_id": 123},
            "https://trackbear.app/api/v1/leaderboard/uuid1234/teams/123",
            "DELETE",
        ),
    ),
)
@responses.activate(assert_all_requests_are_fired=True)
def test_api_response_error(
    client: TrackBearClient,
    provider_method: str,
    kwargs: dict[str, Any],
    url: str,
    http_method: str,
) -> None:
    """Assert a failure on the API side will raise the expected exception."""
    method_to_call = get_client_attribute(client, provider_method)
    pattern = r"TrackBear API Failure \(409\) SOME_ERROR_CODE - A human-readable error message"

    responses.add(
        method=http_method,
        status=409,
        url=url,
        body=json.dumps(FAILURE_RESPONSE),
    )

    with pytest.raises(exceptions.APIResponseError, match=pattern):
        method_to_call(**kwargs)


@pytest.mark.parametrize(
    "provider_method,kwargs,pattern",
    (
        (
            "stat.list",
            {"start_date": "foo"},
            "Invalid date value: 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "stat.list",
            {"end_date": "bar"},
            "Invalid date value: 'bar'. Must be YYYY-MM-DD",
        ),
        (
            "tally.list",
            {"start_date": "foo"},
            "Invalid date value: 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "tally.list",
            {"end_date": "bar"},
            "Invalid date value: 'bar'. Must be YYYY-MM-DD",
        ),
        (
            "goal.save_target",
            test_parameters.GOAL_SAVE_TARGET_KWARGS | {"start_date": "foo"},
            "Invalid date value: 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "goal.save_target",
            test_parameters.GOAL_SAVE_TARGET_KWARGS | {"end_date": "bar"},
            "Invalid date value: 'bar'. Must be YYYY-MM-DD",
        ),
        (
            "goal.save_habit",
            test_parameters.GOAL_SAVE_HABIT_KWARGS | {"start_date": "foo"},
            "Invalid date value: 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "goal.save_habit",
            test_parameters.GOAL_SAVE_HABIT_KWARGS | {"end_date": "bar"},
            "Invalid date value: 'bar'. Must be YYYY-MM-DD",
        ),
        (
            "leaderboard.save",
            test_parameters.LEADERBOARD_SAVE_SIMPLE_KWARGS | {"start_date": "foo"},
            "Invalid date value: 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "leaderboard.save",
            test_parameters.LEADERBOARD_SAVE_SIMPLE_KWARGS | {"end_date": "bar"},
            "Invalid date value: 'bar'. Must be YYYY-MM-DD",
        ),
    ),
)
@responses.activate()
def test_parameter_value_error_failure(
    client: TrackBearClient,
    provider_method: str,
    kwargs: dict[str, Any],
    pattern: str,
) -> None:
    """Assert a failure to validate input parameters result in ValueError."""
    fragments = provider_method.split(".", 1)
    provider = fragments[0]
    route = fragments[1]

    with pytest.raises(ValueError, match=pattern):
        getattr(getattr(client, provider), route)(**kwargs)
