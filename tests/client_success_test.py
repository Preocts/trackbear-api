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
from typing import Any
from typing import TypeVar

import pytest
import responses
import responses.matchers

from trackbear_api import TrackBearClient
from trackbear_api import enums
from trackbear_api import models

from . import api_responses

ModelType = TypeVar("ModelType")


@pytest.mark.parametrize(
    "provider,kwargs,url,api_response,query_string,model_type",
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
        assert dataclasses.asdict(result) == api_responses.keys_to_snake_case(api_response)


@pytest.mark.parametrize(
    "provider,kwargs,url,api_response,model_type",
    (
        (
            "project",
            {"project_id": 123},
            "https://trackbear.app/api/v1/project/123",
            api_responses.PROJECTSTUB_RESPONSE,
            models.ProjectStub,
        ),
        (
            "tag",
            {"tag_id": 123},
            "https://trackbear.app/api/v1/tag/123",
            api_responses.TAG_RESPONSE,
            models.Tag,
        ),
        (
            "tally",
            {"tally_id": 123},
            "https://trackbear.app/api/v1/tally/123",
            api_responses.TALLY_RESPONSE,
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
    assert dataclasses.asdict(result) == api_responses.keys_to_snake_case(api_response)
