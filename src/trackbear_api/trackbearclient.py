from __future__ import annotations

import importlib.metadata
import logging
import os
import re
from typing import Any

import requests

from ._trackbearresponse import TrackBearResponse

# Environment variable keys pulled for configuration if they exist
_TOKEN_ENVIRON = "TRACKBEAR_APP_TOKEN"
_USER_AGENT_ENVIRON = "TRACKBEAR_USER_AGENT"
_URL_ENVIRON = "TRACKBEAR_API_URL"

# Default values, can be overridden by user
_DEFAULT_USER_AGENT = f"trackbear-api/{importlib.metadata.version('trackbear-api')} (https://github.com/Preocts/trackbear-api) by Preocts"
_DEFAULT_API_URL = "https://trackbear.app/api/v1"


class TrackBearClient:
    """Primary CRUD client used to communite with the TrackBear API."""

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

        api_token = _pick_config_value(api_token, _TOKEN_ENVIRON, "")
        if not api_token:
            msg = "Missing api token. Either provide directly as a keyword arguement or as the environment variable 'TRACKBEAR_APP_TOKEN'."
            self.logger.error("%s", msg)
            raise ValueError(msg)

        user_agent = _pick_config_value(user_agent, _USER_AGENT_ENVIRON, _DEFAULT_USER_AGENT)

        api_url = _pick_config_value(api_url, _URL_ENVIRON, _DEFAULT_API_URL)
        self.api_url = api_url.rstrip("/") if api_url.endswith("/") else api_url

        self.session = self._get_request_session(api_token, user_agent)

        self.logger.debug("Initialized TrackBearClient with user-agent: %s", user_agent)
        self.logger.debug("Initialized TrackBearClient with token: %s", api_token[-4:])
        self.logger.debug("Initialized TrackBearClient with url: %s", self.api_url)

    def _get_request_session(self, api_token: str, user_agent: str) -> requests.sessions.Session:
        """Build a Session with required headers for API calls."""
        session = requests.sessions.Session()

        session.headers = {
            "User-Agent": user_agent,
            "Authorization": f"Bearer {api_token}",
        }

        return session

    def get(self, route: str, params: dict[str, Any] | None = None) -> TrackBearResponse:
        """GET request to the TrackBear API."""
        return self._handle_request("GET", route, params=params)

    def post(self, route: str, payload: dict[str, Any] | None = None) -> TrackBearResponse:
        """POST request to the TrackBear API."""
        return self._handle_request("POST", route, payload=payload)

    def patch(self, route: str, payload: dict[str, Any] | None = None) -> TrackBearResponse:
        """PATCH request to the TrackBear API."""
        return self._handle_request("PATCH", route, payload=payload)

    def delete(self, route: str, payload: dict[str, Any] | None = None) -> TrackBearResponse:
        """DELETE request to the TrackBear API."""
        return self._handle_request("DELETE", route, payload=payload)

    def _handle_request(
        self,
        method: str,
        route: str,
        *,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> TrackBearResponse:
        """Internal logic for making all API requests."""
        route = route.lstrip("/") if route.startswith("/") else route
        url = f"{self.api_url}/{route}"

        if params:
            response = self.session.request(method, url, params=params)
        else:
            response = self.session.request(method, url, json=payload)

        if not response.ok:
            log_body = f"Code: {response.status_code} Route: {route} Parames: {params} Text: {response.text} Headers: {response.headers}"
            self.logger.error("Bad API response. %s", log_body)
        else:
            log_body = f"Code: {response.status_code} Route: {route} Parames: {params}"
            self.logger.debug("Good API resposne. %s", log_body)

        rheaders = response.headers.get("RateLimit", "Undefined")
        remaining, reset = self.parse_response_rate_limit(rheaders)

        self.logger.debug("%d requets remaining; resets in %s seconds", remaining, reset)

        return TrackBearResponse.build(
            response=response.json(),
            remaining_requests=remaining,
            rate_reset=reset,
            status_code=response.status_code,
        )

    def parse_response_rate_limit(self, rate_limit: str) -> tuple[int, int]:
        """
        Process the RateLimit response header, returns Requests Remaining and Window Reset Time

        https://help.trackbear.app/api/rate-limits

        Args:
            rate_limit (str): The 'RateLimit' header of an API response.
        """
        remaining_search = re.search(r"r=(\d+)", rate_limit)
        reset_search = re.search(r"t=(\d+)", rate_limit)

        if remaining_search is None or reset_search is None:
            self.logger.error("Unexpected response header format, RateLimit:%s", rate_limit)
            return 0, 0

        return int(remaining_search.group(1)), int(reset_search.group(1))


def _pick_config_value(
    provided_value: str | None,
    environ_key: str,
    default: str,
) -> str:
    """
    Choose the preferred configuration value from the available values.

    Preference of provided value -> environ value -> default value
    """
    if provided_value:
        return provided_value

    if os.getenv(environ_key):
        return os.getenv(environ_key, "")

    return default
