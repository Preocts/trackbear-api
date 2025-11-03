from __future__ import annotations

import logging
import re
from typing import Any

import requests

from ._trackbearresponse import TrackBearResponse


class APIClient:
    """Primary CRUD client used to communicate with the TrackBear API."""

    logger = logging.getLogger("trackbear-api")

    def __init__(self, session: requests.sessions.Session, api_url: str) -> None:
        """Initialize client with session built from TrackBearClient."""
        self.session = session
        self.api_url = api_url

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
