from __future__ import annotations

import importlib.metadata

import pytest

from trackbear_api import TrackBearClient


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
