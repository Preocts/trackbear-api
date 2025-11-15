from __future__ import annotations

import re
from collections.abc import Sequence

from . import enums
from . import exceptions
from . import models
from ._apiclient import APIClient

_DATE_PATTERN = re.compile(r"[\d]{4}-[\d]{2}-[\d]{2}")


class LeaderboardClient:
    """Provides methods and models for Leaderboard API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(self) -> Sequence[models.LeaderboardExtended]:
        """
        List all leaderboards, their members, and teams.

        Returns:
            A sequence of trackbear_api.models.LeaderboardExtended

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get("/leaderboard")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [models.LeaderboardExtended.build(data) for data in response.data]

    def list_participants(self, board_uuid: str) -> Sequence[models.Participant]:
        """
        List all participants of a given leaderboard.

        Returns:
            A sequence of trackbear_api.models.Participant

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get(f"/leaderboard/{board_uuid}/participants")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [models.Participant.build(data) for data in response.data]

    def get(self, board_uuid: str) -> models.Leaderboard:
        """
        Get Leaderboard by uuid.

        Args:
            board_uuid (str): Leaderboard UUID to request from TrackBear

        Returns:
            trackbear_api.models.Leaderboard

        Raises:
            exceptions.APIResponseError: On failure to retrieve requested model
        """
        return self._get(board_uuid, "/leaderboard")

    def get_by_join_code(self, join_code: str) -> models.Leaderboard:
        """
        Get Leaderboard by a join code.

        Args:
            join_code (str): The leaderboard's join code.

        Returns:
            trackbear_api.models.Leaderboard

        Raises:
            exceptions.APIResponseError: On failure to retrieve requested model
        """
        return self._get(join_code, "/leaderboard/joincode")

    def _get(self, uuid: str, route: str) -> models.Leaderboard:
        """Handle GET requests by url."""
        response = self._api_client.get(f"{route}/{uuid}")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Leaderboard.build(response.data)

    def save(
        self,
        title: str,
        description: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        measures: Sequence[enums.Measure | str] | None = None,
        word: int | None = None,
        time: int | None = None,
        page: int | None = None,
        chapter: int | None = None,
        scene: int | None = None,
        line: int | None = None,
        individual_goal_mode: bool = False,
        fundraiser_mode: bool = False,
        is_joinable: bool = True,
        starred: bool = False,
        board_uuid: str | None = None,
    ) -> models.Leaderboard:
        """
        Save a Leaderboard

        If `board_uuid` is provided, then the existing Leaderboard is updated. Otherwise,
        a new Leaderboard is created.

        Args:
            title (str): Title of the Project
            description (str): Description of the Project
            start_date (str): (Optional) Starting date to pull (YYYY-MM-DD)
            end_date (str): (Optional) Ending date to pull (YYYY-MM-DD)
            measures (Sequence[Measure | str]): List of measures that apply to the
                leaderboard. Can be of the following: `word`, `time`, `page`, `chapter`,
                `scene`, or `line`
            word (int): (Optional) Goal of words
            time (int): (Optional) Goal of time
            page (int): (Optional) Goal of pages
            chapter (int): (Optional) Goal of chapters
            scene (int): (Optional) Goal of scenes
            line (int): (Optional) Goal of lines
            individual_goal_mode (bool): When True, members define their own
                goals. (default: False)
            fundraiser_mode (bool): When True, everyone's progress will be counted
                collectively toward the goal. (default: False)
            is_joinable (bool): When True the leaderboard is open for users to
                join. (default: True)
            starred (bool): Star the project (default: False)
            board_uuid (str): (Optional) Existing Leaderboard uuid if request is to
                update existing LeaderBoard

        Returns:
            trackbear_api.models.Goal

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
            ValueError: If `start_date` or `end_date` are not "YYYY-MM-DD"
            ValueError: When `measure` is not a valid value
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        _measures = [
            measure if isinstance(measure, enums.Measure) else enums.Measure(measure)
            for measure in measures or []
        ]

        if start_date is not None and _DATE_PATTERN.match(start_date) is None:
            raise ValueError(f"Invalid start_date '{start_date}'. Must be YYYY-MM-DD")

        if end_date is not None and _DATE_PATTERN.match(end_date) is None:
            raise ValueError(f"Invalid end_date '{end_date}'. Must be YYYY-MM-DD")

        goal = {
            "word": word,
            "time": time,
            "page": page,
            "chapter": chapter,
            "scene": scene,
            "line": line,
        }
        goal = {key: value for key, value in goal.items() if value is not None}

        payload = {
            "title": title,
            "description": description,
            "startDate": start_date,
            "endDate": end_date,
            "individualGoalMode": individual_goal_mode,
            "fundraiserMode": fundraiser_mode,
            "measures": _measures,
            "goal": goal if len(goal) > 0 else None,
            "isJoinable": is_joinable,
            "starred": starred,
        }

        if board_uuid is None:
            response = self._api_client.post("/leaderboard", payload)
        else:
            response = self._api_client.patch(f"/leaderboard/{board_uuid}", payload)

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Leaderboard.build(response.data)

    def save_star(self, board_uuid: int, *, starred: bool = True) -> models.Starred:
        """
        Star or unstar a LeaderBoard

        Args:
            board_uuid (int): Existing leaderboard uuid
            starred (bool): True to star the loaderboard (default: True)

        Returns:
            trackbear_api.models.Leaderboard

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        payload = {"starred": starred}

        response = self._api_client.patch(f"/leaderboard/{board_uuid}/star", payload)

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Starred.build(response.data)

    def delete(self, board_uuid: int) -> models.Leaderboard:
        """
        Delete an existing Leaderboard.

        Args:
            board_uuid (int): Existing leaderboard uuid

        Returns:
            trackbear_api.models.Leaderboard

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/leaderboard/{board_uuid}")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Leaderboard.build(response.data)
