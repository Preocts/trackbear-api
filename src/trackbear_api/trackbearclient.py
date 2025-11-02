from __future__ import annotations

import importlib.metadata
import logging
import os

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

        if api_token is None:
            api_token = os.getenv(_TOKEN_ENVIRON, "")

        if not api_token:
            msg = "Missing api token. Either provide directly as a keyword arguement or as the environment variable 'TRACKBEAR_APP_TOKEN'."
            self.logger.error("%s", msg)
            raise ValueError(msg)

        self.api_token = api_token
        self.user_agent = self._get_user_agent(user_agent)

    def _get_user_agent(self, user_agent: str | None) -> str:
        """Get the user agent, preference to arguement over environment. Default if None."""
        environ_value = os.getenv(_USER_AGENT_ENVIRON, "")

        if user_agent:
            return user_agent

        if environ_value:
            return environ_value

        return _DEFAULT_USER_AGENT
