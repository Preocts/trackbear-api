from __future__ import annotations

import re
from collections.abc import Sequence

from ._apiclient import APIClient
from .enums import Measure
from .exceptions import APIResponseError
from .models import Tally

_DATE_PATTERN = re.compile(r"[\d]{4}-[\d]{2}-[\d]{2}")


class TallyClient:
    """Provides methods and models for Tally API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(
        self,
        works: Sequence[int] | None = None,
        tags: Sequence[int] | None = None,
        measure: Measure | str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Sequence[Tally]:
        """
        List all tallies by default or use provided filters.

        Args:
            works (Sequence[int]): List of project ids to filter results by
            tags: (Sequence[int]): List of tag ids to filter results by
            measure (Measure | str): Measure enum of the following: `word`, `time`,
                `page`, `chapter`, `scene`, or `line`.
            start_date (str): Starting date to pull (YYYY-MM-DD)
            end_date (str): Ending date to pull (YYYY-MM-DD)

        Returns:
            A sequence of Tally models, can be empty

        Raises:
            APIResponseError: On any failure message returned from TrackBear API
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        if measure is not None:
            measure = measure if isinstance(measure, Measure) else Measure(measure)

        if start_date is not None:
            if _DATE_PATTERN.match(start_date) is None:
                raise ValueError(f"Invalid start_date '{start_date}'. Must be YYYY-MM-DD")

        if end_date is not None:
            if _DATE_PATTERN.match(end_date) is None:
                raise ValueError(f"Invalid end_date '{end_date}'. Must be YYYY-MM-DD")

        params = {
            "works[]": works,
            "tags[]": tags,
            "measure": measure.value if measure is not None else None,
            "startDate": start_date,
            "endDate": end_date,
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = self._api_client.get("/tally", params=params)

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [Tally.build(data) for data in response.data]
