from __future__ import annotations

from collections.abc import Sequence

from . import _validator as validator
from . import enums
from . import models
from ._apiclient import APIClient


class ParticipationClient:
    """Provides methods and models for Leaderboard Participation (/me) API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def get(self, board_uuid: str) -> models.Participation:
        """
        Get your participation for a given leaderboard.

        Args:
            board_uuid (str): The UUID of the leaderboard

        Returns:
            trackbear_api.models.Participation

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get(f"/leaderboard/{board_uuid}/me")

        validator.check_response(response)

        return models.Participation.build(response.data)

    def join(
        self,
        board_uuid: str,
        display_name: str,
        *,
        is_participant: bool = False,
        color: enums.MemberColor | str | None = None,
        goal_measure: enums.Measure | str | None = None,
        starting_count: int = 0,
        work_ids: Sequence[int] | None = None,
        tag_ids: Sequence[int] | None = None,
    ) -> models.Participation:
        """
        Join a leaderboard as a participant.

        Args:
            board_uuid (str): The UUID of the leaderboard to get the team from
            display_name (str): The name to display on the board
            is_participant (bool): (optional) Whether you are participanting on the
                board (default: False)
            color (MemberColor | str): (optional) Color for the team. Can be of the
                following: `auto`, `red`, `orange`, `amber`, `yellow`, `lime`, `green`,
                `teal`, `cyan`, `sky`, `blue`, `violet`, `purple`, `fuchia`, `pink`,
                `rose`, or `gray`
            goal_measure (Measure | str): (optional) Measure enum of the following:
                `word`, `time`, `page`, `chapter`, `scene`, or `line`
            starting_count (int): (optional) Starting balance of measure
            work_ids (Sequence[int]): (Optional) List of work ids that apply to the
                goal. Default: None, all works apply to goal
            tag_ids (Sequence[int]): (Optional) List of tag ids that apply to the
                goal. Default: None, all tags apply to goal
        Returns:
            trackbear_api.models.Participation

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        return self._save_owner(
            board_uuid=board_uuid,
            display_name=display_name,
            is_participant=is_participant,
            color=color,
            goal_measure=goal_measure,
            starting_count=starting_count,
            work_ids=work_ids,
            tag_ids=tag_ids,
            is_update=False,
        )

    def update(
        self,
        board_uuid: str,
        display_name: str,
        *,
        is_participant: bool = False,
        color: enums.MemberColor | str | None = None,
        goal_measure: enums.Measure | str | None = None,
        starting_count: int = 0,
        work_ids: Sequence[int] | None = None,
        tag_ids: Sequence[int] | None = None,
    ) -> models.Participation:
        """
        Update your information for a leaderboard as a participant.

        Args:
            board_uuid (str): The UUID of the leaderboard to get the team from
            display_name (str): The name to display on the board
            is_participant (bool): (optional) Whether you are participanting on the
                board (default: False)
            color (MemberColor | str): (optional) Color for the team. Can be of the
                following: `auto`, `red`, `orange`, `amber`, `yellow`, `lime`, `green`,
                `teal`, `cyan`, `sky`, `blue`, `violet`, `purple`, `fuchia`, `pink`,
                `rose`, or `gray`
            goal_measure (Measure | str): (optional) Measure enum of the following:
                `word`, `time`, `page`, `chapter`, `scene`, or `line`
            starting_count (int): (optional) Starting balance of measure
            work_ids (Sequence[int]): (Optional) List of work ids that apply to the
                goal. Default: None, all works apply to goal
            tag_ids (Sequence[int]): (Optional) List of tag ids that apply to the
                goal. Default: None, all tags apply to goal
        Returns:
            trackbear_api.models.Participation

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        return self._save_owner(
            board_uuid=board_uuid,
            display_name=display_name,
            is_participant=is_participant,
            color=color,
            goal_measure=goal_measure,
            starting_count=starting_count,
            work_ids=work_ids,
            tag_ids=tag_ids,
            is_update=True,
        )

    def _save_owner(
        self,
        board_uuid: str,
        display_name: str,
        *,
        is_participant: bool = False,
        color: enums.MemberColor | str | None = None,
        goal_measure: enums.Measure | str | None = None,
        starting_count: int = 0,
        work_ids: Sequence[int] | None = None,
        tag_ids: Sequence[int] | None = None,
        is_update: bool = False,
    ) -> models.Participation:
        """Save participation information."""
        if color is None:
            _color = None
        else:
            _color = color if isinstance(color, enums.MemberColor) else enums.MemberColor(color)

        if goal_measure is None:
            _goal = None
        else:
            _goal = {
                "measure": (
                    goal_measure
                    if isinstance(goal_measure, enums.Measure)
                    else enums.Measure(goal_measure)
                ),
                "count": starting_count,
            }

        payload = {
            "displayName": display_name,
            "isParticipant": is_participant,
            "color": _color,
            "goal": _goal,
            "workIds": work_ids,
            "tagIds": tag_ids,
        }

        if is_update:
            response = self._api_client.patch(f"/leaderboard/{board_uuid}/me", payload)
        else:
            response = self._api_client.post(f"/leaderboard/{board_uuid}/me", payload)

        validator.check_response(response)

        return models.Participation.build(response.data)

    def leave(self, board_uuid: str) -> models.Participation:
        """
        Leave a leaderboard.

        Args:
            board_uuid (int): Existing leaderboard uuid

        Returns:
            trackbear_api.models.Participation

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/leaderboard/{board_uuid}/me")

        validator.check_response(response)

        return models.Participation.build(response.data)
