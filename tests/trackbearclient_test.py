from __future__ import annotations

import importlib.metadata

import pytest

from trackbear_api import TrackBearClient


@pytest.mark.usefixtures("add_environ_token")
def test_init_client_providing_keyword_token() -> None:
    """
    Initialize the client, providing the API token directly.

    The set environ token should be ignored.
    """
    client = TrackBearClient(api_token="keyword_value")

    assert client.session.headers["Authorization"] == "Bearer keyword_value"


@pytest.mark.usefixtures("add_environ_token")
def test_init_client_providing_environ_token() -> None:
    """
    Initialize the client, providing the API token by the environment
    """
    client = TrackBearClient()

    assert client.session.headers["Authorization"] == "Bearer environ_value"


def test_init_client_providing_no_token() -> None:
    """
    Initialize the client without a token. Expect an exception raised.
    """
    expected_msg = "Missing api token. Either provide directly as a keyword arguement or as the environment variable 'TRACKBEAR_APP_TOKEN'."

    with pytest.raises(ValueError, match=expected_msg):
        TrackBearClient()


@pytest.mark.usefixtures("add_environ_token", "add_environ_useragent")
def test_init_client_user_agent_custom() -> None:
    """
    Initialize the client, providing a custom user-agent.

    Expected to override the environ user-agent.
    """
    expected_value = "test agent/1.0.0"

    client = TrackBearClient(user_agent=expected_value)

    assert client.session.headers["User-Agent"] == expected_value


@pytest.mark.usefixtures("add_environ_token", "add_environ_useragent")
def test_init_client_user_agent_environ() -> None:
    """
    Initialize the client, assert environment provided agent is used.
    """
    expected_value = "environ_value"

    client = TrackBearClient()

    assert client.session.headers["User-Agent"] == expected_value


@pytest.mark.usefixtures("add_environ_token")
def test_init_client_user_agent_default() -> None:
    """
    Initialize the client, assert default agent is used.
    """
    expected_value = f"trackbear-api/{importlib.metadata.version('trackbear-api')} (https://github.com/Preocts/trackbear-api) by Preocts"

    client = TrackBearClient()

    assert client.session.headers["User-Agent"] == expected_value


@pytest.mark.usefixtures("add_environ_token", "add_environ_useragent", "add_environ_url")
def test_init_client_api_url_custom() -> None:
    """
    Initialize the client, providing a custom api url.

    Expected to override the environ api url.
    """
    expected_value = "https://some.other.app"

    client = TrackBearClient(api_url=expected_value)

    assert client.api_url == expected_value


@pytest.mark.usefixtures("add_environ_token", "add_environ_useragent", "add_environ_url")
def test_init_client_api_url_environ() -> None:
    """
    Initialize the client, assert environment provided url is used.
    """
    expected_value = "environ_value"

    client = TrackBearClient()

    assert client.api_url == expected_value


@pytest.mark.usefixtures("add_environ_token")
def test_init_client_api_url_default() -> None:
    """
    Initialize the client, assert default url is used.
    """
    expected_value = "https://trackbear.app/api/v1/"

    client = TrackBearClient()

    assert client.api_url == expected_value
