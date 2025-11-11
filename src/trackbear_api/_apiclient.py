from __future__ import annotations

import logging
import re
from collections.abc import Mapping
from typing import Any

import requests

from . import exceptions
from . import models


class APIClient:
    """Primary CRUD client used to communicate with the TrackBear API."""

    logger = logging.getLogger("trackbear-api")

    def __init__(self, session: requests.sessions.Session, api_url: str, timeout: int) -> None:
        """
        Initialize client with session built from TrackBearClient.

        Args:
            session (requests.sessions.Session): Configured requests Session
            api_url (str): Base url for the TrackBear API
            timeout (int): HTTP Timeout in seconds
        """
        self.session = session
        self.api_url = api_url
        self.timeout = timeout

    def get(
        self,
        route: str,
        params: Mapping[str, Any] | None = None,
    ) -> models.TrackBearResponse:
        """
        GET request to the TrackBear API.

        Args:
            route (str): Route to call from API; example: "/project"
            params (Mapping): key-value pairs of URL parameters for the call

        Returns:
            trackbear_api.models.TrackBearResponse

        Raises:
            exceptions.APITimeoutError: If the call exceeds defined time-out
        """
        return self._handle_request("GET", route, params=params)

    def post(
        self,
        route: str,
        payload: Mapping[str, Any] | None = None,
    ) -> models.TrackBearResponse:
        """
        POST request to the TrackBear API.

        Args:
            route (str): Route to call from API; example: "/project"
            payload (Mapping): key-value pairs of request body

        Returns:
            trackbear_api.models.TrackBearResponse

        Raises:
            exceptions.APITimeoutError: If the call exceeds defined time-out
        """
        return self._handle_request("POST", route, payload=payload)

    def patch(
        self,
        route: str,
        payload: Mapping[str, Any] | None = None,
    ) -> models.TrackBearResponse:
        """
        PATCH request to the TrackBear API.

        Args:
            route (str): Route to call from API; example: "/project"
            payload (Mapping): key-value pairs of request body

        Returns:
            trackbear_api.models.TrackBearResponse

        Raises:
            exceptions.APITimeoutError: If the call exceeds defined time-out
        """
        return self._handle_request("PATCH", route, payload=payload)

    def delete(self, route: str) -> models.TrackBearResponse:
        """
        DELETE request to the TrackBear API.

        Args:
            route (str): Route to call from API; example: "/project"

        Returns:
            trackbear_api.models.TrackBearResponse

        Raises:
            exceptions.APITimeoutError: If the call exceeds defined time-out

        """
        return self._handle_request("DELETE", route)

    def _handle_request(
        self,
        method: str,
        route: str,
        *,
        params: Mapping[str, Any] | None = None,
        payload: Mapping[str, Any] | None = None,
    ) -> models.TrackBearResponse:
        """Internal logic for making all API requests."""
        route = route.lstrip("/") if route.startswith("/") else route
        url = f"{self.api_url}/{route}"

        try:
            if params:
                response = self.session.request(method, url, params=params, timeout=self.timeout)
            else:
                response = self.session.request(method, url, json=payload, timeout=self.timeout)

        except requests.exceptions.Timeout as err:
            exc = exceptions.APITimeoutError(err, method, url, self.timeout)
            self.logger.error("%s", exc)
            raise exc from err

        if not response.ok:
            log_body = f"Code: {response.status_code} Route: {route} Parames: {params} Text: {response.text} Headers: {response.headers}"
            self.logger.error("Bad API response. %s", log_body)
        else:
            log_body = f"Code: {response.status_code} Route: {route} Parames: {params}"
            self.logger.debug("Good API response. %s", log_body)

        rheaders = response.headers.get("RateLimit", "Undefined")
        remaining, reset = self.parse_response_rate_limit(rheaders)

        self.logger.debug("%d requets remaining; resets in %s seconds", remaining, reset)

        return models.TrackBearResponse.build(
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
