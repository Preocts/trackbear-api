from __future__ import annotations

import logging
import os

_TOKEN_ENVIRON = "TRACKBEAR_APP_TOKEN"

class TrackBearClient:
    """Primary CRUD client used to communite with the TrackBear API."""

    logger = logging.getLogger("trackbear-api")

    def __init__(self, *, api_token: str | None = None) -> None:
        """
        Initialize the client.

        This client can be passed to each provider class, otherwise the provider
        class will create an instance of this client for themselves.

        No log handler is defined by default. Logger is named "trackbear-api".

        Args:
            api_token (str): The API token for TrackBear. If not provided then the token
                is looked for in the loaded environment (TRACKBEAR_APP_TOKEN)
        """

        if api_token is None:
            api_token = os.getenv(_TOKEN_ENVIRON, "")

        if not api_token:
            msg = "Missing api token. Either provide directly as a keyword arguement or as the environment variable 'TRACKBEAR_APP_TOKEN'."
            self.logger.error("%s", msg)
            raise ValueError(msg)

        self.api_token = api_token
