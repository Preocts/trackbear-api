from __future__ import annotations

import importlib.metadata
import logging
import os

import requests

from ._apiclient import APIClient
from ._projectclient import ProjectClient

__all__ = ["TrackBearClient"]

# Environment variable keys pulled for configuration if they exist
_TOKEN_ENVIRON = "TRACKBEAR_API_TOKEN"
_USER_AGENT_ENVIRON = "TRACKBEAR_API_AGENT"
_URL_ENVIRON = "TRACKBEAR_API_URL"

# Default values, can be overridden by user
_DEFAULT_USER_AGENT = f"trackbear-api/{importlib.metadata.version('trackbear-api')} (https://github.com/Preocts/trackbear-api) by Preocts"
_DEFAULT_API_URL = "https://trackbear.app/api/v1"


class TrackBearClient:
    """Client used to communite with the TrackBear API."""

    logger = logging.getLogger("trackbear-api")

    def __init__(
        self,
        *,
        api_token: str | None = None,
        api_url: str | None = None,
        user_agent: str | None = None,
    ) -> None:
        """
        Initialize the client.

        No log handler is defined by default. Logger is named "trackbear-api".

        Args:
            api_token (str): The API token for TrackBear. If not provided then the token
                is looked for in the loaded environment (TRACKBEAR_APP_TOKEN)
            api_url (str): Defaults to "https://trackbear.app/api/v1/", can also be set
                in environment (TRACKBEAR_API_URL)
            user_agent (str): By default the User-Agent header value points to the
                trackbear-api repo. You can override this to identify your own app by
                providing directly or fro the environment (TRACKBEAR_USER_AGENT).
                https://help.trackbear.app/api/authentication#identifying-your-app

        Raises:
            ValueError: If API token is not provided or an empty string.
        """

        api_token = self._pick_config_value(api_token, _TOKEN_ENVIRON, "")
        if not api_token:
            msg = "Missing api token. Either provide directly as a keyword arguement or as the environment variable 'TRACKBEAR_APP_TOKEN'."
            self.logger.error("%s", msg)
            raise ValueError(msg)

        user_agent = self._pick_config_value(user_agent, _USER_AGENT_ENVIRON, _DEFAULT_USER_AGENT)

        api_url = self._pick_config_value(api_url, _URL_ENVIRON, _DEFAULT_API_URL)
        api_url = api_url.rstrip("/") if api_url.endswith("/") else api_url

        self.logger.debug("Initialized TrackBearClient with user-agent: %s", user_agent)
        self.logger.debug("Initialized TrackBearClient with token: ***%s", api_token[-4:])
        self.logger.debug("Initialized TrackBearClient with url: %s", api_url)

        session = self._get_request_session(api_token, user_agent)
        self._api_client = APIClient(session, api_url)

        # Define all client providers
        self.bare = self._api_client
        self.project = ProjectClient(self._api_client)

    def _pick_config_value(
        self,
        provided_value: str | None,
        environ_key: str,
        default: str,
    ) -> str:
        """
        Choose the preferred configuration value from the available values.

        Preference of provided value -> environ value -> default value
        """
        if provided_value:
            self.logger.debug("Using provided value for %s", environ_key)
            return provided_value

        if os.getenv(environ_key):
            self.logger.debug("Using environment value for %s", environ_key)
            return os.getenv(environ_key, "")

        self.logger.debug("Using default value for %s", environ_key)
        return default

    def _get_request_session(self, api_token: str, user_agent: str) -> requests.sessions.Session:
        """Build a Session with required headers for API calls."""
        session = requests.sessions.Session()

        session.headers = {
            "User-Agent": user_agent,
            "Authorization": f"Bearer {api_token}",
        }

        return session
