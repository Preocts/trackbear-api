"""
Happy path tests for all client methods.

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

from . import test_parameters

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
    "provider,kwargs,url,api_response,query_string,model_type",
    (
        (
            "project",
            {},
            "https://trackbear.app/api/v1/project",
            test_parameters.PROJECT_RESPONSE,
            "",
            models.Project,
        ),
        (
            "tag",
            {},
            "https://trackbear.app/api/v1/tag",
            test_parameters.TAG_RESPONSE,
            "",
            models.Tag,
        ),
        (
            "stat",
            {"start_date": "2024-01-01", "end_date": "2025-01-01"},
            "https://trackbear.app/api/v1/stats/days",
            test_parameters.STAT_RESPONSE,
            "startDate=2024-01-01&endDate=2025-01-01",
            models.Stat,
        ),
        (
            "tally",
            {"works": [123, 456], "tags": [987, 654], "measure": enums.Measure.SCENE},
            "https://trackbear.app/api/v1/tally",
            test_parameters.TALLY_RESPONSE,
            "works[]=123&works[]=456&tags[]=987&tags[]=654&measure=scene",
            models.Tally,
        ),
        (
            "tally",
            {"measure": "scene", "start_date": "2025-01-01", "end_date": "2025-12-31"},
            "https://trackbear.app/api/v1/tally",
            test_parameters.TALLY_RESPONSE,
            "measure=scene&startDate=2025-01-01&endDate=2025-12-31",
            models.Tally,
        ),
    ),
)
@responses.activate(assert_all_requests_are_fired=True)
def test_client_list_success(
    client: TrackBearClient,
    provider: str,
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

    results = getattr(client, provider).list(**kwargs)

    assert len(results) == len(mock_data)

    for result in results:
        assert isinstance(result, model_type)
        assert dataclasses.is_dataclass(result)
        assert not isinstance(result, type)
        assert dataclasses.asdict(result) == keys_to_snake_case(api_response)


@pytest.mark.parametrize(
    "provider,kwargs,expected_payload,url,api_response,model_type",
    (
        (
            "project",
            test_parameters.PROJECT_SAVE_KWARGS,
            test_parameters.PROJECT_SAVE_PAYLOAD,
            "https://trackbear.app/api/v1/project",
            test_parameters.PROJECTSTUB_RESPONSE,
            models.ProjectStub,
        ),
        (
            "project",
            # replace enum with string while adding project_id
            test_parameters.PROJECT_SAVE_KWARGS | {"phase": "drafting", "project_id": 123},
            test_parameters.PROJECT_SAVE_PAYLOAD,
            "https://trackbear.app/api/v1/project/123",
            test_parameters.PROJECTSTUB_RESPONSE,
            models.ProjectStub,
        ),
        (
            "tag",
            test_parameters.TAG_SAVE_KWARGS,
            test_parameters.TAG_SAVE_PAYLOAD,
            "https://trackbear.app/api/v1/tag",
            test_parameters.TAG_RESPONSE,
            models.Tag,
        ),
        (
            "tag",
            # replace enum with string while adding tag_id
            test_parameters.TAG_SAVE_KWARGS | {"color": "blue", "tag_id": 123},
            test_parameters.TAG_SAVE_PAYLOAD,
            "https://trackbear.app/api/v1/tag/123",
            test_parameters.TAG_RESPONSE,
            models.Tag,
        ),
        (
            "tally",
            test_parameters.TALLY_SAVE_KWARGS,
            test_parameters.TALLY_SAVE_PAYLOAD,
            "https://trackbear.app/api/v1/tally",
            test_parameters.TALLY_RESPONSE,
            models.Tally,
        ),
        (
            "tally",
            # replace enum with string while adding tally_id
            test_parameters.TALLY_SAVE_KWARGS | {"measure": "scene", "tally_id": 123},
            test_parameters.TALLY_SAVE_PAYLOAD,
            "https://trackbear.app/api/v1/tally/123",
            test_parameters.TALLY_RESPONSE,
            models.Tally,
        ),
    ),
)
@responses.activate(assert_all_requests_are_fired=True)
def test_client_save_success(
    client: TrackBearClient,
    provider: str,
    kwargs: dict[str, Any],
    expected_payload: dict[str, Any],
    url: str,
    api_response: dict[str, Any],
    model_type: type[ModelType],
) -> None:
    """
    Assert a new create returns the expected model while asserting
    the payload is generated for the request correctly.

    NOTE: The response model is not reflective of the kwarg inputs.

    Accepts a Measure enum in the parameters
    """
    body_match = responses.matchers.body_matcher(json.dumps(expected_payload))

    responses.add(
        method="PATCH" if url.endswith("123") else "POST",
        url=url,
        status=200,
        match=[body_match],
        body=json.dumps({"success": True, "data": api_response}),
    )

    result = getattr(client, provider).save(**kwargs)

    assert isinstance(result, model_type)
    assert dataclasses.is_dataclass(result)
    assert not isinstance(result, type)
    assert dataclasses.asdict(result) == keys_to_snake_case(api_response)


@pytest.mark.parametrize(
    "provider,kwargs,url,api_response,model_type",
    (
        (
            "project",
            {"project_id": 123},
            "https://trackbear.app/api/v1/project/123",
            test_parameters.PROJECTSTUB_RESPONSE,
            models.ProjectStub,
        ),
        (
            "tag",
            {"tag_id": 123},
            "https://trackbear.app/api/v1/tag/123",
            test_parameters.TAG_RESPONSE,
            models.Tag,
        ),
        (
            "tally",
            {"tally_id": 123},
            "https://trackbear.app/api/v1/tally/123",
            test_parameters.TALLY_RESPONSE,
            models.Tally,
        ),
    ),
)
@responses.activate(assert_all_requests_are_fired=True)
def test_client_delete_success(
    client: TrackBearClient,
    provider: str,
    kwargs: dict[str, Any],
    url: str,
    api_response: dict[str, Any],
    model_type: type[ModelType],
) -> None:
    """Assert a delete request returns the expected model."""
    body = json.dumps({"success": True, "data": api_response})
    responses.add(method="DELETE", url=url, status=200, body=body)

    result = getattr(client, provider).delete(**kwargs)

    assert isinstance(result, model_type)
    assert dataclasses.is_dataclass(result)
    assert not isinstance(result, type)
    assert dataclasses.asdict(result) == keys_to_snake_case(api_response)
