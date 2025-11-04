from __future__ import annotations

import importlib.metadata
import json

import pytest
import responses
import responses.matchers

from trackbear_api import TrackBearClient
from trackbear_api import TrackBearResponse


@pytest.fixture
def client(add_environ_token: None, add_environ_useragent: None) -> TrackBearClient:
    """Create a mock client."""
    return TrackBearClient()


def test_init_client_providing_no_token() -> None:
    """
    Initialize the client without a token. Expect an exception raised.
    """
    expected_msg = "Missing api token. Either provide directly as a keyword arguement or as the environment variable 'TRACKBEAR_APP_TOKEN'."

    with pytest.raises(ValueError, match=expected_msg):
        TrackBearClient()


@pytest.mark.usefixtures("add_environ_token", "add_environ_useragent", "add_environ_url")
def test_init_client_custom_values() -> None:
    """
    Initialize the client, providing a custom keyword values

    Expected to override the environ values
    """
    expected_api_token = "mock_api_key"
    expected_url = "https://some.other.app"
    expected_user_agent = "my custom app/1.0"

    client = TrackBearClient(
        api_token=expected_api_token,
        api_url=expected_url,
        user_agent=expected_user_agent,
    )

    assert client.bare.session.headers["Authorization"] == f"Bearer {expected_api_token}"
    assert client.bare.api_url == expected_url
    assert client.bare.session.headers["User-Agent"] == expected_user_agent


@pytest.mark.usefixtures("add_environ_token", "add_environ_useragent", "add_environ_url")
def test_init_client_environ_values() -> None:
    """
    Initialize the client, assert environment values provided are used
    """
    expected_value = "environ_value"

    client = TrackBearClient()

    assert client.bare.session.headers["Authorization"] == f"Bearer {expected_value}"
    assert client.bare.api_url == expected_value
    assert client.bare.session.headers["User-Agent"] == expected_value


@pytest.mark.usefixtures("add_environ_token")
def test_init_client_default_values() -> None:
    """
    Initialize the client, assert default values are used. Excludes API token.
    """
    expected_url = "https://trackbear.app/api/v1"
    expected_user_agent = f"trackbear-api/{importlib.metadata.version('trackbear-api')} (https://github.com/Preocts/trackbear-api) by Preocts"

    client = TrackBearClient()

    assert client.bare.api_url == expected_url
    assert client.bare.session.headers["User-Agent"] == expected_user_agent


@responses.activate(assert_all_requests_are_fired=True)
def test_get_valid_response(client: TrackBearClient) -> None:
    """GET request with expected valid response."""
    expected_headers = {
        "Authorization": "Bearer environ_value",
        "User-Agent": "environ_value",
    }
    expected_params = {"foo": "bar"}
    mock_response = json.dumps({"success": True, "data": "pong"})
    mock_headers = {
        "RateLimit-Policy": '"100-in-1min"; q=100; w=60; pk=:Nzg5ZmNjZGRmNDBk:',
        "RateLimit": '"100-in-1min"; r=98; t=58',
    }
    headers_match = responses.matchers.header_matcher(expected_headers)
    parames_match = responses.matchers.query_param_matcher(expected_params)

    responses.add(
        method="GET",
        url="https://trackbear.app/api/v1/ping",
        body=mock_response,
        headers=mock_headers,
        match=[headers_match, parames_match],
    )

    response = client.bare.get("/ping", params=expected_params)

    assert isinstance(response, TrackBearResponse)
    assert response.success is True
    assert response.data == "pong"
    assert response.remaining_requests == 98
    assert response.rate_reset == 58
    assert response.status_code == 200


@responses.activate(assert_all_requests_are_fired=True)
def test_get_invalid_response(client: TrackBearClient) -> None:
    """GET request with expected invalid response."""
    expected_headers = {
        "Authorization": "Bearer environ_value",
        "User-Agent": "environ_value",
    }
    expected_params = {"foo": "bar"}
    mock_response = json.dumps(
        {
            "success": False,
            "error": {
                "code": "SOME_ERROR_CODE",
                "message": "A human-readable error message",
            },
        }
    )
    headers_match = responses.matchers.header_matcher(expected_headers)
    parames_match = responses.matchers.query_param_matcher(expected_params)

    responses.add(
        method="GET",
        url="https://trackbear.app/api/v1/ping",
        body=mock_response,
        status=409,
        match=[headers_match, parames_match],
    )

    response = client.bare.get("/ping", params=expected_params)

    assert isinstance(response, TrackBearResponse)
    assert response.success is False
    assert response.error.message == "A human-readable error message"
    assert response.error.code == "SOME_ERROR_CODE"
    assert response.remaining_requests == 0
    assert response.rate_reset == 0
    assert response.status_code == 409


@responses.activate(assert_all_requests_are_fired=True)
def test_post_valid_response(client: TrackBearClient) -> None:
    """POST request with expected valid response."""
    mock_data = {
        "id": 123,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "string",
        "updatedAt": "string",
        "state": "string",
        "ownerId": 123,
        "title": "string",
        "description": "string",
        "type": "string",
        "parameters": {"threshold": {"measure": "string", "count": 0}},
        "startDate": "string",
        "endDate": "string",
        "workIds": [123],
        "tagIds": [123],
        "starred": False,
        "displayOnProfile": False,
    }

    expected_headers = {
        "Authorization": "Bearer environ_value",
        "User-Agent": "environ_value",
    }
    mock_response = json.dumps({"success": True, "data": mock_data})
    mock_headers = {
        "RateLimit-Policy": '"100-in-1min"; q=100; w=60; pk=:Nzg5ZmNjZGRmNDBk:',
        "RateLimit": '"100-in-1min"; r=98; t=58',
    }
    expected_payload = {"foo": "bar"}
    headers_match = responses.matchers.header_matcher(expected_headers)
    body_match = responses.matchers.body_matcher(json.dumps(expected_payload))

    responses.add(
        method="POST",
        url="https://trackbear.app/api/v1/goal",
        body=mock_response,
        headers=mock_headers,
        match=[headers_match, body_match],
    )

    response = client.bare.post("/goal", expected_payload)

    assert isinstance(response, TrackBearResponse)
    assert response.success is True
    assert response.data == mock_data


@responses.activate(assert_all_requests_are_fired=True)
def test_patch_valid_response(client: TrackBearClient) -> None:
    """PATCH request with expected valid response."""
    mock_data = {
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
    }

    expected_headers = {
        "Authorization": "Bearer environ_value",
        "User-Agent": "environ_value",
    }
    expected_payload = {
        "title": "string",
        "description": "string",
        "phase": "string",
        "startingBalance": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
        "starred": False,
        "displayOnProfile": False,
    }

    mock_response = json.dumps({"success": True, "data": mock_data})
    mock_headers = {
        "RateLimit-Policy": '"100-in-1min"; q=100; w=60; pk=:Nzg5ZmNjZGRmNDBk:',
        "RateLimit": '"100-in-1min"; r=98; t=58',
    }
    headers_match = responses.matchers.header_matcher(expected_headers)
    body_match = responses.matchers.body_matcher(json.dumps(expected_payload))

    responses.add(
        method="PATCH",
        url="https://trackbear.app/api/v1/project/123",
        body=mock_response,
        headers=mock_headers,
        match=[headers_match, body_match],
    )

    response = client.bare.patch("/project/123", expected_payload)

    assert isinstance(response, TrackBearResponse)
    assert response.success is True
    assert response.data == mock_data


@responses.activate(assert_all_requests_are_fired=True)
def test_delete_valid_response(client: TrackBearClient) -> None:
    """DELETE request with expected valid response."""
    mock_data = {
        "id": 123,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "string",
        "updatedAt": "string",
        "state": "string",
        "ownerId": 123,
        "date": "2021-03-23",
        "measure": "string",
        "count": 0,
        "note": "string",
        "workId": 123,
        "work": {
            "id": 123,
            "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
            "createdAt": "string",
            "updatedAt": "string",
            "state": "string",
            "ownerId": 123,
            "title": "string",
            "description": "string",
            "phase": "string",
            "startingBalance": {
                "word": 0,
                "time": 0,
                "page": 0,
                "chapter": 0,
                "scene": 0,
                "line": 0,
            },
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
                "state": "string",
                "ownerId": 123,
                "name": "string",
                "color": "string",
            }
        ],
    }

    expected_headers = {
        "Authorization": "Bearer environ_value",
        "User-Agent": "environ_value",
    }

    mock_response = json.dumps({"success": True, "data": mock_data})
    mock_headers = {
        "RateLimit-Policy": '"100-in-1min"; q=100; w=60; pk=:Nzg5ZmNjZGRmNDBk:',
        "RateLimit": '"100-in-1min"; r=98; t=58',
    }
    headers_match = responses.matchers.header_matcher(expected_headers)

    responses.add(
        method="DELETE",
        url="https://trackbear.app/api/v1/tally/123",
        body=mock_response,
        headers=mock_headers,
        match=[headers_match],
    )

    response = client.bare.delete("/tally/123")

    assert isinstance(response, TrackBearResponse)
    assert response.success is True
    assert response.data == mock_data
