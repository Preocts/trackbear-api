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


@pytest.mark.parametrize(
    "provider_method,kwargs,url",
    (
        (
            "project.list",
            {},
            "https://trackbear.app/api/v1/project",
        ),
        (
            "project.get",
            {"project_id": 123},
            "https://trackbear.app/api/v1/project/123",
        ),
        (
            "project.save",
            {"title": "mock", "description": "mock", "phase": "planning"},
            "https://trackbear.app/api/v1/project",
        ),
        (
            "project.delete",
            {"project_id": 123},
            "https://trackbear.app/api/v1/project/123",
        ),
        (
            "goal.list",
            {},
            "https://trackbear.app/api/v1/goal",
        ),
        (
            "goal.get",
            {"goal_id": 123},
            "https://trackbear.app/api/v1/goal/123",
        ),
        (
            "goal.save_target",
            test_parameters.GOAL_SAVE_TARGET_KWARGS,
            "https://trackbear.app/api/v1/goal",
        ),
        (
            "goal.save_habit",
            test_parameters.GOAL_SAVE_HABIT_KWARGS,
            "https://trackbear.app/api/v1/goal",
        ),
        (
            "goal.delete",
            {"goal_id": 123},
            "https://trackbear.app/api/v1/goal/123",
        ),
        (
            "stat.list",
            {},
            "https://trackbear.app/api/v1/stats/days",
        ),
        (
            "tag.list",
            {},
            "https://trackbear.app/api/v1/tag",
        ),
        (
            "tag.get",
            {"tag_id": 123},
            "https://trackbear.app/api/v1/tag/123",
        ),
        (
            "tag.save",
            {"name": "mock", "color": "blue"},
            "https://trackbear.app/api/v1/tag",
        ),
        (
            "tag.delete",
            {"tag_id": 123},
            "https://trackbear.app/api/v1/tag/123",
        ),
        (
            "tally.list",
            {},
            "https://trackbear.app/api/v1/tally",
        ),
        (
            "tally.get",
            {"tally_id": 123},
            "https://trackbear.app/api/v1/tally/123",
        ),
        (
            "tally.save",
            {"work_id": 123, "date": "2025-01-01", "measure": "word", "count": 0},
            "https://trackbear.app/api/v1/tally",
        ),
        (
            "tally.delete",
            {"tally_id": 123},
            "https://trackbear.app/api/v1/tally/123",
        ),
    ),
)
@responses.activate()
def test_api_response_error(
    client: TrackBearClient,
    provider_method: str,
    kwargs: dict[str, Any],
    url: str,
) -> None:
    """Assert a failure on the API side will raise the expected exception."""
    methods = {"list": "GET", "get": "GET", "save": "POST", "delete": "DELETE"}
    fragments = provider_method.split(".", 1)
    provider = fragments[0]
    route = fragments[1]
    pattern = r"TrackBear API Failure \(409\) SOME_ERROR_CODE - A human-readable error message"

    responses.add(
        method=methods[route.split("_", 1)[0]],
        status=409,
        url=url,
        body=json.dumps(FAILURE_RESPONSE),
    )

    with pytest.raises(exceptions.APIResponseError, match=pattern):
        getattr(getattr(client, provider), route)(**kwargs)


@pytest.mark.parametrize(
    "provider_method,kwargs,pattern",
    (
        (
            "stat.list",
            {"start_date": "foo"},
            "Invalid start_date 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "stat.list",
            {"end_date": "bar"},
            "Invalid end_date 'bar'. Must be YYYY-MM-DD",
        ),
        (
            "tally.list",
            {"start_date": "foo"},
            "Invalid start_date 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "tally.list",
            {"end_date": "bar"},
            "Invalid end_date 'bar'. Must be YYYY-MM-DD",
        ),
        (
            "goal.save_target",
            test_parameters.GOAL_SAVE_TARGET_KWARGS | {"start_date": "foo"},
            "Invalid start_date 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "goal.save_target",
            test_parameters.GOAL_SAVE_TARGET_KWARGS | {"end_date": "bar"},
            "Invalid end_date 'bar'. Must be YYYY-MM-DD",
        ),
        (
            "goal.save_habit",
            test_parameters.GOAL_SAVE_HABIT_KWARGS | {"start_date": "foo"},
            "Invalid start_date 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "goal.save_habit",
            test_parameters.GOAL_SAVE_HABIT_KWARGS | {"end_date": "bar"},
            "Invalid end_date 'bar'. Must be YYYY-MM-DD",
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
