from __future__ import annotations

from collections.abc import Sequence

from . import exceptions
from . import models
from ._apiclient import APIClient


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

    def get(self, board_uuid: str) -> models.Leaderboard:
        """
        Get Leaderboard by uuid.

        NOTE: This method uses the UUID, not the ID like most others.

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
