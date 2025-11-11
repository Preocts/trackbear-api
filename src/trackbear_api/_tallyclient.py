from __future__ import annotations

import re
from collections.abc import Sequence

from . import enums
from . import exceptions
from . import models
from ._apiclient import APIClient

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
        measure: enums.Measure | str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Sequence[models.Tally]:
        """
        List all tallies by default or use provided filters.

        All arguements are optional and act as filters for the results.

        Args:
            works (Sequence[int]): (Optional) List of project ids
            tags: (Sequence[int]): (Optional) List of tag ids
            measure (Measure | str): (Optional) Measure enum of the following: `word`,
                `time`, `page`, `chapter`, `scene`, or `line`.
            start_date (str): (Optional) Starting date to pull (YYYY-MM-DD)
            end_date (str): (Optional) Ending date to pull (YYYY-MM-DD)

        Returns:
            A sequence of trackbear_api.models.Tally

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
            ValueError: When `measure` is not a valid value
            ValueError: If `start_date` or `end_date` are not "YYYY-MM-DD"
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        if measure is not None:
            measure = measure if isinstance(measure, enums.Measure) else enums.Measure(measure)

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
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [models.Tally.build(data) for data in response.data]

    def get(self, tally_id: int) -> models.Tally:
        """
        Get Tally by id.

        Args:
            tally_id (int): Tally ID to request from TrackBear

        Returns:
            trackbear_api.models.Tally

        Raises:
            exceptions.APIResponseError: On failure to retrieve requested model
        """
        response = self._api_client.get(f"/tally/{tally_id}")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Tally.build(response.data)

    def save(
        self,
        work_id: int,
        date: str,
        measure: enums.Measure | str,
        count: int,
        note: str = "",
        tags: Sequence[str] | None = None,
        tally_id: int | None = None,
        *,
        set_total: bool = False,
    ) -> models.Tally:
        """
        Save a models.Tally.

        If `tally_id` is provided, then the existing tally is updated. Otherwise,
        a new tally is created.

        Args:
            work_id (int): ID of the project the tally is applied to
            date (str): Date of the tally (YYYY-MM-DD)
            measure (Measure | str): Measure enum of the following: `word`, `time`,
                `page`, `chapter`, `scene`, or `line`.
            count (int): Value of the measure
            note (str): A note for the tally
            tags (Sequence[str]): (Optional) A list of tag names to apply. New tags
                will be created.
            tally_id (int): (Optional) Existing project id if request is to update
                existing projects
            set_total (bool): If true, the provided count will be set as the project total.

        Returns:
            trackbear_api.models.Tally

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
            ValueError: When `measure` is not a valid value
            ValueError: If `date` is not "YYYY-MM-DD"
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        measure = measure if isinstance(measure, enums.Measure) else enums.Measure(measure)

        payload = {
            "date": date,
            "measure": measure.value,
            "count": count,
            "note": note,
            "workId": work_id,
            "setTotal": set_total,
            "tags": tags or [],
        }

        if tally_id is None:
            response = self._api_client.post("/tally", payload)
        else:
            response = self._api_client.patch(f"/tally/{tally_id}", payload)

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Tally.build(response.data)

    def delete(self, tally_id: int) -> models.Tally:
        """
        Delete an existing models.tally.

        Args:
            tally_id (int): Existing tally id

        Returns:
            trackbear_api.models.Tally

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/tally/{tally_id}")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Tally.build(response.data)
