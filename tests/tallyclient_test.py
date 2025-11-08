"""
All tests are run through the TrackBearClient which is the public API for the library.

Tests in this collection focus on the error handling and successful model building.
There is no focus on the underlying APIClient behavior as that is tested in the
trackbearclient_test.py collection.
"""

from __future__ import annotations

import copy
import json

import pytest
import responses
import responses.matchers

from trackbear_api import TrackBearClient
from trackbear_api.enums import Measure
from trackbear_api.exceptions import APIResponseError
from trackbear_api.models import Tally
from trackbear_api.models import Tag
from trackbear_api.models import ProjectStub

TALLY_RESPONSE = {
    "id": 123,
    "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
    "createdAt": "string",
    "updatedAt": "string",
    "state": "active",
    "ownerId": 123,
    "date": "2021-03-23",
    "measure": "word",
    "count": 1667,
    "note": "string",
    "workId": 123,
    "work": {
        "id": 123,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "string",
        "updatedAt": "string",
        "state": "active",
        "ownerId": 123,
        "title": "string",
        "description": "string",
        "phase": "planning",
        "startingBalance": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
        "cover": "string",
        "starred": False,
        "displayOnProfile": False,
    },
    "tags": [
        {
            "id": 123,
            "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
            "createdAt": "string",
            "updatedAt": "string",
            "state": "active",
            "ownerId": 123,
            "name": "string",
            "color": "default",
        }
    ],
}


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_list_success_no_params(client: TrackBearClient) -> None:
    """Assert the Tally model is built correctly."""
    mock_data = [copy.deepcopy(TALLY_RESPONSE)] * 3
    mock_body = {"success": True, "data": mock_data}

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/tally",
        body=json.dumps(mock_body),
    )

    projects = client.tally.list()

    assert len(projects) == len(mock_data)

    for project in projects:
        assert isinstance(project, Tally)


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_list_success_params_enum(client: TrackBearClient) -> None:
    """
    Assert params are parsed correctly.

    `measure` is provided as a Measure enum
    `work` and `tag` are array values

    All remaining parameter options are None and, thus, excluded from the query string.
    """
    mock_data = [copy.deepcopy(TALLY_RESPONSE)] * 3
    mock_body = {"success": True, "data": mock_data}

    query = "works[]=123&works[]=456&tags[]=987&tags[]=654&measure=scene"
    params_matcher = responses.matchers.query_string_matcher(query)

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/tally",
        body=json.dumps(mock_body),
        match=[params_matcher],
    )

    projects = client.tally.list(works=[123, 456], tags=[987, 654], measure=Measure.SCENE)

    assert len(projects) == len(mock_data)

    for project in projects:
        assert isinstance(project, Tally)


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_list_success_params_string(client: TrackBearClient) -> None:
    """
    Assert params are parsed correctly.

    `measure` is provided as a string (converted to an enum in implmentation)
    `start_date` and `end_date` are provided

    All remaining parameter options are None and, thus, excluded from the query string.
    """
    mock_data = [copy.deepcopy(TALLY_RESPONSE)] * 3
    mock_body = {"success": True, "data": mock_data}

    query = "measure=scene&startDate=2025-01-01&endDate=2025-12-31"
    params_matcher = responses.matchers.query_string_matcher(query)

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/tally",
        body=json.dumps(mock_body),
        match=[params_matcher],
    )

    projects = client.tally.list(measure="scene", start_date="2025-01-01", end_date="2025-12-31")

    assert len(projects) == len(mock_data)

    for project in projects:
        assert isinstance(project, Tally)


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_list_failure(client: TrackBearClient) -> None:
    """Assert a failure on the API side will raise the expected exception."""
    mock_body = {
        "success": False,
        "error": {
            "code": "SOME_ERROR_CODE",
            "message": "A human-readable error message",
        },
    }
    pattern = r"TrackBear API Failure \(409\) SOME_ERROR_CODE - A human-readable error message"

    responses.add(
        method="GET",
        status=409,
        url="https://trackbear.app/api/v1/tally",
        body=json.dumps(mock_body),
    )

    with pytest.raises(APIResponseError, match=pattern):
        client.tally.list()


def test_tally_list_raises_with_bad_start_date(client: TrackBearClient) -> None:
    """Assert the method raises ValueError with incorrect start date format."""
    pattern = "Invalid start_date 'foo'. Must be YYYY-MM-DD"

    with pytest.raises(ValueError, match=pattern):
        client.tally.list(start_date="foo")


def test_tally_list_raises_with_bad_end_date(client: TrackBearClient) -> None:
    """Assert the method raises ValueError with incorrect end date format."""
    pattern = "Invalid end_date 'bar'. Must be YYYY-MM-DD"

    with pytest.raises(ValueError, match=pattern):
        client.tally.list(end_date="bar")


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_get_success(client: TrackBearClient) -> None:
    """Assert the Project model is built correctly."""
    mock_data = copy.deepcopy(TALLY_RESPONSE)
    mock_body = {"success": True, "data": mock_data}

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/tally/123",
        body=json.dumps(mock_body),
    )

    project = client.tally.get(123)

    assert isinstance(project, Tally)
    assert isinstance(project.work, ProjectStub)
    for tag in project.tags:
        assert isinstance(tag, Tag)


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_get_failure(client: TrackBearClient) -> None:
    """Assert a failure on the API side will raise the expected exception."""
    mock_body = {
        "success": False,
        "error": {
            "code": "SOME_ERROR_CODE",
            "message": "A human-readable error message",
        },
    }
    pattern = r"TrackBear API Failure \(404\) SOME_ERROR_CODE - A human-readable error message"

    responses.add(
        method="GET",
        status=404,
        url="https://trackbear.app/api/v1/tally/123",
        body=json.dumps(mock_body),
    )

    with pytest.raises(APIResponseError, match=pattern):
        client.tally.get(123)
