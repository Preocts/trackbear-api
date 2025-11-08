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
from trackbear_api.models import ProjectStub
from trackbear_api.models import Tag
from trackbear_api.models import Tally

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


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_save_create_success(client: TrackBearClient) -> None:
    """
    Assert a new create returns the expected model (mocked) while asserting
    the payload is generated for the request correctly.

    Accepts a Measure enum in the parameters
    """
    expected_payload = {
        "date": "2025-01-01",
        "measure": "scene",
        "count": 69,
        "note": "Some Note",
        "workId": 123,
        "setTotal": True,
        "tags": ["New Tag"],
    }
    body_match = responses.matchers.body_matcher(json.dumps(expected_payload))

    responses.add(
        method="POST",
        url="https://trackbear.app/api/v1/tally",
        status=200,
        match=[body_match],
        body=json.dumps({"success": True, "data": TALLY_RESPONSE}),
    )

    tally = client.tally.save(
        work_id=123,
        date="2025-01-01",
        measure=Measure.SCENE,
        count=69,
        note="Some Note",
        tags=["New Tag"],
        set_total=True,
    )

    assert isinstance(tally, Tally)


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_save_update_success(client: TrackBearClient) -> None:
    """
    Assert an update returns the expected model (mocked) while asserting
    the payload is generated for the request correctly.

    Accepts a string in place of a Measure enum in parameters
    """
    expected_payload = {
        "date": "2025-01-01",
        "measure": "scene",
        "count": 69,
        "note": "Some Note",
        "workId": 123,
        "setTotal": True,
        "tags": ["New Tag"],
    }
    body_match = responses.matchers.body_matcher(json.dumps(expected_payload))

    responses.add(
        method="PATCH",
        url="https://trackbear.app/api/v1/tally/456",
        status=200,
        match=[body_match],
        body=json.dumps({"success": True, "data": TALLY_RESPONSE}),
    )

    tally = client.tally.save(
        work_id=123,
        date="2025-01-01",
        measure="scene",
        count=69,
        note="Some Note",
        tags=["New Tag"],
        tally_id=456,
        set_total=True,
    )

    assert isinstance(tally, Tally)


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_create_failure(client: TrackBearClient) -> None:
    """Assert a failure on the API side will raise the expected exception."""
    mock_body = {
        "success": False,
        "error": {
            "code": "SOME_ERROR_CODE",
            "message": "A human-readable error message",
        },
    }
    pattern = r"TrackBear API Failure \(400\) SOME_ERROR_CODE - A human-readable error message"

    responses.add(
        method="POST",
        status=400,
        url="https://trackbear.app/api/v1/tally",
        body=json.dumps(mock_body),
    )

    with pytest.raises(APIResponseError, match=pattern):
        client.tally.save(123, "2025-01-01", "scene", 69, "", [])


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_delete_success(client: TrackBearClient) -> None:
    """
    Assert a remove request returns the expected Tally
    """
    responses.add(
        method="DELETE",
        url="https://trackbear.app/api/v1/tally/123",
        status=200,
        body=json.dumps({"success": True, "data": TALLY_RESPONSE}),
    )

    project = client.tally.delete(tally_id=123)

    assert isinstance(project, Tally)


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_delete_failure(client: TrackBearClient) -> None:
    """Assert a failure on the API side will raise the expected exception."""
    mock_body = {
        "success": False,
        "error": {
            "code": "SOME_ERROR_CODE",
            "message": "A human-readable error message",
        },
    }
    pattern = r"TrackBear API Failure \(400\) SOME_ERROR_CODE - A human-readable error message"

    responses.add(
        method="DELETE",
        status=400,
        url="https://trackbear.app/api/v1/tally/123",
        body=json.dumps(mock_body),
    )

    with pytest.raises(APIResponseError, match=pattern):
        client.tally.delete(tally_id=123)
