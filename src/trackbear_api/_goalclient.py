from __future__ import annotations

from collections.abc import Sequence

from . import _validator as validator
from . import enums
from . import models
from ._apiclient import APIClient


class GoalClient:
    """Provides methods and models for Goal API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(self) -> Sequence[models.Goal]:
        """
        List all Goals.

        Returns:
            A sequence of trackbear_api.models.Goal

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get("/goal")

        validator.check_response(response)

        return [models.Goal.build(data) for data in response.data]

    def get(self, goal_id: int) -> models.Goal:
        """
        Get Goal by id.

        Args:
            goal_id (int): Tag ID to request from TrackBear

        Returns:
            trackbear_api.models.Goal

        Raises:
            exceptions.APIResponseError: On failure to retrieve requested model
        """
        response = self._api_client.get(f"/goal/{goal_id}")

        validator.check_response(response)

        return models.Goal.build(response.data)

    def save_target(
        self,
        title: str,
        description: str,
        measure: enums.Measure | str,
        count: int,
        start_date: str | None = None,
        end_date: str | None = None,
        work_ids: Sequence[int] | None = None,
        tag_ids: Sequence[int] | None = None,
        starred: bool = False,
        display_on_profile: bool = False,
        goal_id: int | None = None,
    ) -> models.Goal:
        """
        Save a Target Goal, a target measure to reach in the duration of the goal.

        If `goal_id` is provided, then the existing tag is updated. Otherwise,
        a new goal is created.

        Args:
            title (str): Title of the Project
            description (str): Description of the Project
            measure (Measure | str): Measure enum of the following: `word`, `time`,
                `page`, `chapter`, `scene`, or `line`
            count (int): Goal of the given measure
            start_date (str): (Optional) Starting date to pull (YYYY-MM-DD)
            end_date (str): (Optional) Ending date to pull (YYYY-MM-DD)
            work_ids (Sequence[int]): (Optional) List of work ids that apply to the
                goal. Default: None, all works apply to goal
            tag_ids (Sequence[int]): (Optional) List of tag ids that apply to the
                goal. Default: None, all tags apply to goal
            starred (bool): Star the project (default: False)
            display_on_profile (bool): Display project on public profile (default: False)
            goal_id (int): (Optional) Existing tag id if request is to update
                existing tag

        Returns:
            trackbear_api.models.Goal

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
            ValueError: When `measure` is not a valid value
            ValueError: If `start_date` or `end_date` are not "YYYY-MM-DD"
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        if isinstance(measure, enums.Measure):
            _measure = measure
        else:
            _measure = enums.Measure(measure)

        validator.check_date(start_date)
        validator.check_date(end_date)

        payload = {
            "title": title,
            "description": description,
            "type": enums.GoalType.TARGET.value,
            "parameters": {
                "threshold": {
                    "measure": _measure.value,
                    "count": count,
                },
            },
            "startDate": start_date,
            "endDate": end_date,
            "workIds": work_ids if work_ids is not None else [],
            "tagIds": tag_ids if tag_ids is not None else [],
            "starred": starred,
            "displayOnProfile": display_on_profile,
        }

        if goal_id is None:
            response = self._api_client.post("/goal", payload)
        else:
            response = self._api_client.patch(f"/goal/{goal_id}", payload)

        validator.check_response(response)

        return models.Goal.build(response.data)

    def save_habit(
        self,
        title: str,
        description: str,
        unit: enums.HabitUnit | str,
        period: int,
        start_date: str | None = None,
        end_date: str | None = None,
        measure: enums.Measure | str | None = None,
        count: int | None = None,
        work_ids: Sequence[int] | None = None,
        tag_ids: Sequence[int] | None = None,
        starred: bool = False,
        display_on_profile: bool = False,
        goal_id: int | None = None,
    ) -> models.Goal:
        """
        Save a Target Habit, hit an optional target measure on a given cadence.

        If `goal_id` is provided, then the existing tag is updated. Otherwise,
        a new goal is created.

        Args:
            title (str): Title of the Project
            description (str): Description of the Project
            unit (Unit | str): Unit enum of the following: `day`, `week`, `month`
                or `year`
            period (int): How often the cadance is every N units
            start_date (str): (Optional) Starting date to pull (YYYY-MM-DD)
            end_date (str): (Optional) Ending date to pull (YYYY-MM-DD)
            measure (Measure | str): (Optional) Measure enum of the following: `word`,
                `time`, `page`, `chapter`, `scene`, or `line`
            count (int): (Optional) Goal of the given measure
            work_ids (Sequence[int]): List of work ids that apply to the goal.
                Default: None, all works apply to goal
            tag_ids (Sequence[int]): (Optional) List of tag ids that apply to the goal.
                Default: None, all tags apply to goal
            starred (bool): Star the project (default: False)
            display_on_profile (bool): Display project on public profile (default: False)
            goal_id (int): (Optional) Existing tag id if request is to update
                existing tag

        Returns:
            trackbear_api.models.Goal

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
            ValueError: When `unit` or `measure` are not valid
            ValueError: If `start_date` or `end_date` are not "YYYY-MM-DD"
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        if not isinstance(measure, enums.Measure):
            _measure = enums.Measure(measure) if measure is not None else None
        else:
            _measure = measure

        if isinstance(unit, enums.HabitUnit):
            _unit = unit
        else:
            _unit = enums.HabitUnit(unit)

        validator.check_date(start_date)
        validator.check_date(end_date)

        if _measure is not None:
            threshold = {"measure": _measure.value, "count": count or 0}
        else:
            threshold = None

        payload = {
            "title": title,
            "description": description,
            "type": enums.GoalType.HABIT.value,
            "parameters": {
                "cadence": {
                    "unit": _unit.value,
                    "period": period,
                },
                "threshold": threshold,
            },
            "startDate": start_date,
            "endDate": end_date,
            "workIds": work_ids if work_ids is not None else [],
            "tagIds": tag_ids if tag_ids is not None else [],
            "starred": starred,
            "displayOnProfile": display_on_profile,
        }

        if goal_id is None:
            response = self._api_client.post("/goal", payload)
        else:
            response = self._api_client.patch(f"/goal/{goal_id}", payload)

        validator.check_response(response)

        return models.Goal.build(response.data)

    def delete(self, goal_id: int) -> models.Goal:
        """
        Delete an existing Goal.

        Args:
            goal_id (int): Existing goal id

        Returns:
            trackbear_api.models.Goal

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/goal/{goal_id}")

        validator.check_response(response)

        return models.Goal.build(response.data)
