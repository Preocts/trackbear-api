from __future__ import annotations

import importlib.metadata
import json

import pytest
import responses
import responses.matchers

from trackbear_api import TrackBearClient
from trackbear_api import TrackBearResponse


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

    assert client.session.headers["Authorization"] == f"Bearer {expected_api_token}"
    assert client.api_url == expected_url
    assert client.session.headers["User-Agent"] == expected_user_agent


@pytest.mark.usefixtures("add_environ_token", "add_environ_useragent", "add_environ_url")
def test_init_client_environ_values() -> None:
    """
    Initialize the client, assert environment values provided are used
    """
    expected_value = "environ_value"

    client = TrackBearClient()

    assert client.session.headers["Authorization"] == f"Bearer {expected_value}"
    assert client.api_url == expected_value
    assert client.session.headers["User-Agent"] == expected_value


@pytest.mark.usefixtures("add_environ_token")
def test_init_client_default_values() -> None:
    """
    Initialize the client, assert default values are used. Excludes API token.
    """
    expected_url = "https://trackbear.app/api/v1/"
    expected_user_agent = f"trackbear-api/{importlib.metadata.version('trackbear-api')} (https://github.com/Preocts/trackbear-api) by Preocts"

    client = TrackBearClient()

    assert client.api_url == expected_url
    assert client.session.headers["User-Agent"] == expected_user_agent


@pytest.fixture
def client(add_environ_token: None, add_environ_useragent: None) -> TrackBearClient:
    """Create a mock client."""
    return TrackBearClient()


def mock_valid_response() -> str:
    """Generate a mock valid response from the API."""
    return json.dumps(
        {
            "success": True,
            "data": "pong",
        }
    )


def mock_invalid_response() -> str:
    """Generate a mock invalid response from the API."""
    return json.dumps(
        {
            "success": False,
            "code": "SOME_ERROR_CODE",
            "message": "A human-readable error message",
        }
    )


@responses.activate(assert_all_requests_are_fired=True)
def test_get_valid_response(client: TrackBearClient) -> None:
    expected_headers = {
        "Authorization": "Bearer environ_value",
        "User-Agent": "environ_value",
    }
    expected_params = {"foo": "bar"}
    headers_match = responses.matchers.header_matcher(expected_headers)
    parames_match = responses.matchers.query_param_matcher(expected_params)

    responses.add(
        method="GET",
        url="https://trackbear.app/api/v1/ping",
        body=mock_valid_response(),
        match=[headers_match, parames_match],
    )

    response = client.get("/ping", params=expected_params)

    assert isinstance(response, TrackBearResponse)
    assert response.success is True
    assert response.data == "pong"


@responses.activate(assert_all_requests_are_fired=True)
def test_get_invalid_response(client: TrackBearClient) -> None:
    expected_headers = {
        "Authorization": "Bearer environ_value",
        "User-Agent": "environ_value",
    }
    expected_params = {"foo": "bar"}
    headers_match = responses.matchers.header_matcher(expected_headers)
    parames_match = responses.matchers.query_param_matcher(expected_params)

    responses.add(
        method="GET",
        url="https://trackbear.app/api/v1/ping",
        body=mock_invalid_response(),
        status=409,
        match=[headers_match, parames_match],
    )

    response = client.get("/ping", params=expected_params)

    assert isinstance(response, TrackBearResponse)
    assert response.success is False
    assert response.message == "A human-readable error message"
    assert response.code == "SOME_ERROR_CODE"
