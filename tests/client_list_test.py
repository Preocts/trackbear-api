"""
Test the .list() method of all clients that support the operation.

All tests are run through the TrackBearClient which is the public API for the library.

Tests in this collection focus on the error handling and successful model building.
There is no focus on the underlying APIClient behavior as that is tested in the
trackbearclient_test.py collection.
"""

from __future__ import annotations

import copy
import dataclasses
import json
import re
from typing import Any
from typing import TypeVar

import pytest
import responses
import responses.matchers

from trackbear_api import TrackBearClient
from trackbear_api import enums
from trackbear_api import models
from trackbear_api.exceptions import APIResponseError

from . import api_responses

ModelType = TypeVar("ModelType")


def keys_to_snake_case(response: dict[str, Any]) -> dict[str, Any]:
    """Translate camelCase keys of response into snake_case."""
    result = {}
    new_value: Any

    for key, value in response.items():
        new_key = re.sub("([A-Z])", r"_\1", key).lower()

        if isinstance(value, list):
            new_value = [keys_to_snake_case(val) for val in value]

        elif isinstance(value, dict):
            new_value = keys_to_snake_case(value)

        else:
            new_value = value

        result[new_key] = new_value

    return result


@pytest.mark.parametrize(
    "client_attribute,kwargs,url,api_response,query_string,model_type",
    (
        (
            "project",
            {},
            "https://trackbear.app/api/v1/project",
            api_responses.PROJECT_RESPONSE,
            "",
            models.Project,
        ),
        (
            "tag",
            {},
            "https://trackbear.app/api/v1/tag",
            api_responses.TAG_RESPONSE,
            "",
            models.Tag,
        ),
        (
            "stat",
            {"start_date": "2024-01-01", "end_date": "2025-01-01"},
            "https://trackbear.app/api/v1/stats/days",
            api_responses.STAT_RESPONSE,
            "startDate=2024-01-01&endDate=2025-01-01",
            models.Stat,
        ),
        (
            "tally",
            {"works": [123, 456], "tags": [987, 654], "measure": enums.Measure.SCENE},
            "https://trackbear.app/api/v1/tally",
            api_responses.TALLY_RESPONSE,
            "works[]=123&works[]=456&tags[]=987&tags[]=654&measure=scene",
            models.Tally,
        ),
        (
            "tally",
            {"measure": "scene", "start_date": "2025-01-01", "end_date": "2025-12-31"},
            "https://trackbear.app/api/v1/tally",
            api_responses.TALLY_RESPONSE,
            "measure=scene&startDate=2025-01-01&endDate=2025-12-31",
            models.Tally,
        ),
    ),
)
@responses.activate(assert_all_requests_are_fired=True)
def test_client_list_success(
    client: TrackBearClient,
    client_attribute: str,
    kwargs: dict[str, Any],
    api_response: dict[str, Any],
    query_string: str,
    url: str,
    model_type: type[ModelType],
) -> None:
    """Assert the list method has success and that the models are correct."""
    mock_data = [copy.deepcopy(api_response)] * 3
    mock_body = {"success": True, "data": mock_data}

    query_matcher = responses.matchers.query_string_matcher(query_string)

    responses.add(
        method="GET",
        status=200,
        url=url,
        body=json.dumps(mock_body),
        match=[query_matcher],
    )

    results = getattr(client, client_attribute).list(**kwargs)

    assert len(results) == len(mock_data)

    for result in results:
        assert isinstance(result, model_type)
        assert dataclasses.is_dataclass(result)
        assert not isinstance(result, type)
        assert dataclasses.asdict(result) == keys_to_snake_case(api_response)


@pytest.mark.parametrize(
    "client_attribute,kwargs,url,exception,pattern",
    (
        (
            "project",
            {},
            "https://trackbear.app/api/v1/project",
            APIResponseError,
            r"TrackBear API Failure \(409\) SOME_ERROR_CODE - A human-readable error message",
        ),
        (
            "stat",
            {},
            "https://trackbear.app/api/v1/stats/days",
            APIResponseError,
            r"TrackBear API Failure \(409\) SOME_ERROR_CODE - A human-readable error message",
        ),
        (
            "stat",
            {"start_date": "foo"},
            "https://trackbear.app/api/v1/stats/days",
            ValueError,
            "Invalid start_date 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "stat",
            {"end_date": "bar"},
            "https://trackbear.app/api/v1/stats/days",
            ValueError,
            "Invalid end_date 'bar'. Must be YYYY-MM-DD",
        ),
        (
            "tag",
            {},
            "https://trackbear.app/api/v1/tag",
            APIResponseError,
            r"TrackBear API Failure \(409\) SOME_ERROR_CODE - A human-readable error message",
        ),
        (
            "tally",
            {},
            "https://trackbear.app/api/v1/tally",
            APIResponseError,
            r"TrackBear API Failure \(409\) SOME_ERROR_CODE - A human-readable error message",
        ),
        (
            "tally",
            {"start_date": "foo"},
            "https://trackbear.app/api/v1/tally",
            ValueError,
            "Invalid start_date 'foo'. Must be YYYY-MM-DD",
        ),
        (
            "tally",
            {"end_date": "bar"},
            "https://trackbear.app/api/v1/tally",
            ValueError,
            "Invalid end_date 'bar'. Must be YYYY-MM-DD",
        ),
    ),
)
@responses.activate()
def test_client_list_failure(
    client: TrackBearClient,
    client_attribute: str,
    kwargs: dict[str, Any],
    url: str,
    exception: type[Exception],
    pattern: str,
) -> None:
    """Assert a failure on the API side will raise the expected exception."""
    mock_body = {
        "success": False,
        "error": {
            "code": "SOME_ERROR_CODE",
            "message": "A human-readable error message",
        },
    }
    # pattern = r"TrackBear API Failure \(409\) SOME_ERROR_CODE - A human-readable error message"

    responses.add(
        method="GET",
        status=409,
        url=url,
        body=json.dumps(mock_body),
    )

    with pytest.raises(exception, match=pattern):
        getattr(client, client_attribute).list(**kwargs)
