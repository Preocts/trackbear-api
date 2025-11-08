"""
All tests are run through the TrackBearClient which is the public API for the library.

Tests in this collection focus on the error handling and successful model building.
There is no focus on the underlying APIClient behavior as that is tested in the
trackbearclient_test.py collection.
"""

from __future__ import annotations

import copy
import json

import responses
import responses.matchers

from trackbear_api import Color
from trackbear_api import TrackBearClient
from trackbear_api.models import Tag

from .api_responses import TAG_RESPONSE


@responses.activate(assert_all_requests_are_fired=True)
def test_tag_get_success(client: TrackBearClient) -> None:
    """Assert the Tag model is built correctly."""
    mock_data = copy.deepcopy(TAG_RESPONSE)
    mock_body = {"success": True, "data": mock_data}

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/tag/123",
        body=json.dumps(mock_body),
    )

    project = client.tag.get(123)

    assert isinstance(project, Tag)


@responses.activate(assert_all_requests_are_fired=True)
def test_tag_save_create_success(client: TrackBearClient) -> None:
    """
    Assert a new create returns the expected model (mocked) while asserting
    the payload is generated for the request correctly.

    Accepts a Color enum in the parameters
    """
    expected_payload = {"name": "Mock Tag", "color": "default"}
    body_match = responses.matchers.body_matcher(json.dumps(expected_payload))

    responses.add(
        method="POST",
        url="https://trackbear.app/api/v1/tag",
        status=200,
        match=[body_match],
        body=json.dumps({"success": True, "data": TAG_RESPONSE}),
    )

    project = client.tag.save("Mock Tag", Color.DEFAULT)

    assert isinstance(project, Tag)


@responses.activate(assert_all_requests_are_fired=True)
def test_tag_save_update_success(client: TrackBearClient) -> None:
    """
    Assert an update returns the expected model (mocked) while asserting
    the payload is generated for the request correctly.

    Accepts a string in place of a Color enum in parameters
    """
    expected_payload = {"name": "Mock Tag", "color": "default"}
    body_match = responses.matchers.body_matcher(json.dumps(expected_payload))

    responses.add(
        method="PATCH",
        url="https://trackbear.app/api/v1/tag/123",
        status=200,
        match=[body_match],
        body=json.dumps({"success": True, "data": TAG_RESPONSE}),
    )

    project = client.tag.save("Mock Tag", "default", 123)

    assert isinstance(project, Tag)


@responses.activate(assert_all_requests_are_fired=True)
def test_tag_delete_success(client: TrackBearClient) -> None:
    """
    Assert a delete request returns the expected Tag
    """
    responses.add(
        method="DELETE",
        url="https://trackbear.app/api/v1/tag/123",
        status=200,
        body=json.dumps({"success": True, "data": TAG_RESPONSE}),
    )

    project = client.tag.delete(tag_id=123)

    assert isinstance(project, Tag)
