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

from trackbear_api import TrackBearClient
from trackbear_api.exceptions import APIResponseError
from trackbear_api.exceptions import ModelBuildError
from trackbear_api.models import Balance
from trackbear_api.models import Project

PROJECT_RESPONSE = {
    "id": 123,
    "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
    "createdAt": "string",
    "updatedAt": "string",
    "state": "string",
    "ownerId": 123,
    "title": "string",
    "description": "string",
    "phase": "string",
    "startingBalance": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
    "cover": "string",
    "starred": False,
    "displayOnProfile": False,
    "totals": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
    "lastUpdated": "string",
}


@pytest.fixture
def client(add_environ_token: None) -> TrackBearClient:
    """Create a mock client."""
    return TrackBearClient()


@responses.activate(assert_all_requests_are_fired=True)
def test_project_list_success(client: TrackBearClient) -> None:
    """Assert the Project model is built correctly."""
    mock_data = [copy.deepcopy(PROJECT_RESPONSE)] * 3
    mock_body = {"success": True, "data": mock_data}

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/project",
        body=json.dumps(mock_body),
    )

    projects = client.project.list()

    assert len(projects) == len(mock_data)

    for project in projects:
        assert isinstance(project, Project)
        assert isinstance(project.starting_balance, Balance)
        assert isinstance(project.totals, Balance)


@responses.activate(assert_all_requests_are_fired=True)
def test_project_list_model_failure(client: TrackBearClient) -> None:
    """Assert expected exception when Project model is built incorrectly."""
    mock_data = copy.deepcopy(PROJECT_RESPONSE)
    del mock_data["id"]
    mock_body = {"success": True, "data": [mock_data]}

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/project",
        body=json.dumps(mock_body),
    )
    pattern = "Failure to build the Project model from the provided data"

    with pytest.raises(ModelBuildError, match=pattern):
        client.project.list()


@responses.activate(assert_all_requests_are_fired=True)
def test_project_list_failure(client: TrackBearClient) -> None:
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
        url="https://trackbear.app/api/v1/project",
        body=json.dumps(mock_body),
    )

    with pytest.raises(APIResponseError, match=pattern):
        client.project.list()


@responses.activate(assert_all_requests_are_fired=True)
def test_project_get_by_id_success(client: TrackBearClient) -> None:
    """Assert the Project model is built correctly."""
    mock_data = copy.deepcopy(PROJECT_RESPONSE)
    mock_body = {"success": True, "data": mock_data}

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/project/123",
        body=json.dumps(mock_body),
    )

    project = client.project.get_by_id("123")

    assert isinstance(project, Project)
    assert isinstance(project.starting_balance, Balance)
    assert isinstance(project.totals, Balance)


@responses.activate(assert_all_requests_are_fired=True)
def test_project_get_by_id_failure(client: TrackBearClient) -> None:
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
        url="https://trackbear.app/api/v1/project/123",
        body=json.dumps(mock_body),
    )

    with pytest.raises(APIResponseError, match=pattern):
        client.project.get_by_id("123")
