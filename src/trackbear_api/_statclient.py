from __future__ import annotations

import re
from collections.abc import Sequence

from . import exceptions
from . import models
from ._apiclient import APIClient

_DATE_PATTERN = re.compile(r"[\d]{4}-[\d]{2}-[\d]{2}")


class StatClient:
    """Provides methods and models for Stat API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Sequence[models.Stat]:
        """
        List stats by a given date range. Pulls all stats by default.

        Args:
            start_date (str): Starting date to pull (YYYY-MM-DD)
            end_date (str): Ending date to pull (YYYY-MM-DD)

        Returns:
            A sequence of trackbear_api.models.Stat

        Raises:
            APIResponseError: On any failure message returned from TrackBear API
            ValueError: If `start_date` or `end_date` are not "YYYY-MM-DD"
        """
        if start_date is not None:
            if _DATE_PATTERN.match(start_date) is None:
                raise ValueError(f"Invalid start_date '{start_date}'. Must be YYYY-MM-DD")

        if end_date is not None:
            if _DATE_PATTERN.match(end_date) is None:
                raise ValueError(f"Invalid end_date '{end_date}'. Must be YYYY-MM-DD")

        params = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = self._api_client.get("/stats/days", params)

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [models.Stat.build(data) for data in response.data]
