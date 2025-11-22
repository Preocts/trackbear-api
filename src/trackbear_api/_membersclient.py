from __future__ import annotations

from collections.abc import Sequence

from . import _validator as validator
from . import models
from ._apiclient import APIClient


class MembersClient:
    """Provides methods and models for Leaderboard Members API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(self, board_uuid: str) -> Sequence[models.Member]:
        """
        List all members on a given leaderboard

        Args:
            board_uuid (str): The UUID of the leaderboard to get members from

        Returns:
            A sequence of trackbear_api.models.Member

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get(f"/leaderboard/{board_uuid}/members")

        validator.check_response(response)

        return [models.Member.build(data) for data in response.data]

    def save_owner(
        self,
        board_uuid: str,
        member_id: int,
        *,
        is_owner: bool = True,
    ) -> models.Member:
        """
        Save whether a member is an owner of the given leaderboard.

        Args:
            board_uuid (str): The UUID of the leaderboard to get the team from
            member_id (int): The member id to adjust
            is_owner (bool): Set whether the member is an owner (default: True)

        Returns:
            trackbear_api.models.Member

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        payload = {"isOwner": is_owner}

        url = f"/leaderboard/{board_uuid}/members/{member_id}"
        response = self._api_client.patch(url, payload)

        validator.check_response(response)

        return models.Member.build(response.data)

    def delete(self, board_uuid: str, member_id: int) -> models.Member:
        """
        Delete an existing member from a leaderboard.

        Args:
            board_uuid (int): Existing leaderboard uuid
            member_id (int): The ID of the team to delete

        Returns:
            trackbear_api.models.Member

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/leaderboard/{board_uuid}/members/{member_id}")

        validator.check_response(response)

        return models.Member.build(response.data)
