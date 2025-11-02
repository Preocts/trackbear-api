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

    assert client.api_token == "keyword_value"


@pytest.mark.usefixtures("add_environ_token")
def test_init_client_providing_environ_token() -> None:
    """
    Initialize the client, providing the API token by the environment
    """
    client = TrackBearClient()

    assert client.api_token == "environ_value"


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

    assert client.user_agent == expected_value


@pytest.mark.usefixtures("add_environ_token", "add_environ_useragent")
def test_init_client_user_agent_environ() -> None:
    """
    Initialize the client, assert environment provided agent is used.
    """
    expected_value = "environ_value"

    client = TrackBearClient()

    assert client.user_agent == expected_value


@pytest.mark.usefixtures("add_environ_token")
def test_init_client_user_agent_default() -> None:
    """
    Initialize the client, assert default agent is used.
    """
    expected_value = f"trackbear-api/{importlib.metadata.version('trackbear-api')} (https://github.com/Preocts/trackbear-api) by Preocts"

    client = TrackBearClient()

    assert client.user_agent == expected_value
