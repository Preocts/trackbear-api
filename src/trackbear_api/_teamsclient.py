from __future__ import annotations

from collections.abc import Sequence

from . import _validator as validator
from . import enums
from . import models
from ._apiclient import APIClient


class TeamsClient:
    """Provides methods and models for Leaderboard Teams API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(self, board_uuid: str) -> Sequence[models.Team]:
        """
        List all teams on a given leaderboard

        Args:
            board_uuid (str): The UUID of the leaderboard to get teams from

        Returns:
            A sequence of trackbear_api.models.Team

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get(f"/leaderboard/{board_uuid}/teams")

        validator.check_response(response)

        return [models.Team.build(data) for data in response.data]

    def get(self, board_uuid: str, team_id: int) -> models.Team:
        """
        Get a team from a specific leaderboard

        Args:
            board_uuid (str): The UUID of the leaderboard to get the team from
            team_id (int): The ID of the team to get

        Returns:
            trackbear_api.models.Team

        Raises:
            exceptions.APIResponseError: On failure to retrieve requested model
        """
        response = self._api_client.get(f"/leaderboard/{board_uuid}/teams/{team_id}")

        validator.check_response(response)

        return models.Team.build(response.data)

    def save(
        self,
        board_uuid: str,
        board_id: int,
        name: str,
        color: enums.MemberColor | str,
        team_id: str | None = None,
    ) -> models.Team:
        """
        Save a team to a leaderboard.

        If `team_id` is provided, then the existing Team is updated. Otherwise,
        a new Team is created.

        Args:
            board_uuid (str): The UUID of the leaderboard to get the team from
            board_id (int): The leaderboard id (not the uuid)
            name (str): The name of the team
            color (MemberColor | str): Color for the team. Can be of the following:
                `auto`, `red`, `orange`, `amber`, `yellow`, `lime`, `green`, `teal`,
                `cyan`, `sky`, `blue`, `violet`, `purple`, `fuchia`, `pink`, `rose`,
                or `gray`
            team_id (str): (Optional) Existing team id if request is to update
                existing team

        Returns:
            trackbear_api.models.Team

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
            ValueError: If `start_date` or `end_date` are not "YYYY-MM-DD"
            ValueError: When `measure` is not a valid value
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        _color = color if isinstance(color, enums.MemberColor) else enums.MemberColor(color)

        payload = {
            "boardId": board_id,
            "name": name,
            "color": _color,
        }

        if team_id is None:
            response = self._api_client.post(f"/leaderboard/{board_uuid}/teams", payload)
        else:
            response = self._api_client.patch(f"/leaderboard/{board_uuid}/teams/{team_id}", payload)

        validator.check_response(response)

        return models.Team.build(response.data)

    def delete(self, board_uuid: str, team_id: int) -> models.Team:
        """
        Delete an existing TEam.

        Args:
            board_uuid (int): Existing leaderboard uuid
            team_id (int): The ID of the team to delete

        Returns:
            trackbear_api.models.Team

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/leaderboard/{board_uuid}/teams/{team_id}")

        validator.check_response(response)

        return models.Team.build(response.data)
