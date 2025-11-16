from __future__ import annotations

from collections.abc import Sequence

from . import _validator as validator
from . import models
from ._apiclient import APIClient


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
        validator.check_date(start_date)
        validator.check_date(end_date)

        params = {}
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = self._api_client.get("/stats/days", params)

        validator.check_response(response)

        return [models.Stat.build(data) for data in response.data]
