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
from trackbear_api.exceptions import APIResponseError
from trackbear_api.models import Balance
from trackbear_api.models import Project
from trackbear_api.models import ProjectStub

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
def test_project_get_success(client: TrackBearClient) -> None:
    """Assert the Project model is built correctly."""
    mock_data = copy.deepcopy(PROJECT_RESPONSE)
    mock_body = {"success": True, "data": mock_data}

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/project/123",
        body=json.dumps(mock_body),
    )

    project = client.project.get(123)

    assert isinstance(project, Project)
    assert isinstance(project.starting_balance, Balance)
    assert isinstance(project.totals, Balance)


@responses.activate(assert_all_requests_are_fired=True)
def test_project_get_failure(client: TrackBearClient) -> None:
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
        client.project.get(123)


@responses.activate(assert_all_requests_are_fired=True)
def test_project_save_create_success(client: TrackBearClient) -> None:
    """
    Assert a new create returns the expected model (mocked) while asserting
    the payload is generated for the request correctly.
    """
    expected_payload = {
        "title": "Mock Title",
        "description": "Some Description.",
        "phase": "drafting",
        "startingBalance": {
            "word": 1000,
            "time": 0,
            "page": 10,
            "chapter": 1,
            "scene": 3,
            "line": 0,
        },
        "starred": True,
        "displayOnProfile": True,
    }
    body_match = responses.matchers.body_matcher(json.dumps(expected_payload))

    responses.add(
        method="POST",
        url="https://trackbear.app/api/v1/project",
        status=200,
        match=[body_match],
        body=json.dumps({"success": True, "data": PROJECT_RESPONSE}),
    )

    project = client.project.save(
        title="Mock Title",
        description="Some Description.",
        phase="drafting",
        starred=True,
        display_on_profile=True,
        word=1000,
        page=10,
        chapter=1,
        scene=3,
    )

    assert isinstance(project, ProjectStub)


@responses.activate(assert_all_requests_are_fired=True)
def test_project_save_update_success(client: TrackBearClient) -> None:
    """
    Assert an update returns the expected model (mocked) while asserting
    the payload is generated for the request correctly.
    """
    expected_payload = {
        "title": "Mock Title",
        "description": "Some Description.",
        "phase": "drafting",
        "startingBalance": {
            "word": 1000,
            "time": 0,
            "page": 10,
            "chapter": 1,
            "scene": 3,
            "line": 0,
        },
        "starred": True,
        "displayOnProfile": True,
    }
    body_match = responses.matchers.body_matcher(json.dumps(expected_payload))

    responses.add(
        method="PATCH",
        url="https://trackbear.app/api/v1/project/123",
        status=200,
        match=[body_match],
        body=json.dumps({"success": True, "data": PROJECT_RESPONSE}),
    )

    project = client.project.save(
        title="Mock Title",
        description="Some Description.",
        phase="drafting",
        starred=True,
        display_on_profile=True,
        word=1000,
        page=10,
        chapter=1,
        scene=3,
        project_id=123,
    )

    assert isinstance(project, ProjectStub)


@responses.activate(assert_all_requests_are_fired=True)
def test_project_create_failure(client: TrackBearClient) -> None:
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
        url="https://trackbear.app/api/v1/project",
        body=json.dumps(mock_body),
    )

    with pytest.raises(APIResponseError, match=pattern):
        client.project.save(
            title="Mock Title",
            description="Some Description.",
            phase="drafting",
            starred=True,
            display_on_profile=True,
            word=1000,
            page=10,
            chapter=1,
            scene=3,
        )


@responses.activate(assert_all_requests_are_fired=True)
def test_project_delete_success(client: TrackBearClient) -> None:
    """
    Assert a remove request returns the expected ProjectStub
    """
    responses.add(
        method="DELETE",
        url="https://trackbear.app/api/v1/project/123",
        status=200,
        body=json.dumps({"success": True, "data": PROJECT_RESPONSE}),
    )

    project = client.project.delete(project_id=123)

    assert isinstance(project, ProjectStub)


@responses.activate(assert_all_requests_are_fired=True)
def test_project_delete_failure(client: TrackBearClient) -> None:
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
        url="https://trackbear.app/api/v1/project/123",
        body=json.dumps(mock_body),
    )

    with pytest.raises(APIResponseError, match=pattern):
        client.project.delete(project_id=123)
