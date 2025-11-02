from __future__ import annotations

import importlib.metadata
import logging
import os

import requests

_TOKEN_ENVIRON = "TRACKBEAR_APP_TOKEN"
_USER_AGENT_ENVIRON = "TRACKBEAR_USER_AGENT"
_DEFAULT_USER_AGENT = f"trackbear-api/{importlib.metadata.version('trackbear-api')} (https://github.com/Preocts/trackbear-api) by Preocts"


class TrackBearClient:
    """Primary CRUD client used to communite with the TrackBear API."""

    logger = logging.getLogger("trackbear-api")

    def __init__(
        self,
        *,
        api_token: str | None = None,
        user_agent: str | None = None,
    ) -> None:
        """
        Initialize the client.

        No log handler is defined by default. Logger is named "trackbear-api".

        Args:
            api_token (str): The API token for TrackBear. If not provided then the token
                is looked for in the loaded environment (TRACKBEAR_APP_TOKEN)
            user_agent (str): By default the User-Agent header value points to the
                trackbear-api repo. You can override this to identify your own app by
                providing directly or fro the environment (TRACKBEAR_USER_AGENT).
                https://help.trackbear.app/api/authentication#identifying-your-app

        Raises:
            ValueError: If API token is not provided or an empty string.
        """

        api_token = self._get_api_token(api_token)
        user_agent = self._get_user_agent(user_agent)

        self.session = self._get_request_session(api_token, user_agent)

        self.logger.debug("Initialized TrackBearClient with user-agent: %s", user_agent)
        self.logger.debug("Initialized TrackBearClient with token: %s", api_token[-4:])

    def _get_api_token(self, api_token: str | None) -> str:
        """Get the api token, preference to arguement over environment. Raise if missing."""
        if api_token is None:
            api_token = os.getenv(_TOKEN_ENVIRON, "")

        if not api_token:
            msg = "Missing api token. Either provide directly as a keyword arguement or as the environment variable 'TRACKBEAR_APP_TOKEN'."
            self.logger.error("%s", msg)
            raise ValueError(msg)

        return api_token

    def _get_user_agent(self, user_agent: str | None) -> str:
        """Get the user agent, preference to arguement over environment. Default if None."""
        environ_value = os.getenv(_USER_AGENT_ENVIRON, "")

        if user_agent:
            return user_agent

        if environ_value:
            return environ_value

        return _DEFAULT_USER_AGENT

    def _get_request_session(self, api_token: str, user_agent: str) -> requests.sessions.Session:
        """Build a Session with required headers for API calls."""
        session = requests.sessions.Session()

        session.headers = {
            "User-Agent": user_agent,
            "Authorization": f"Bearer {api_token}",
        }

        return session
