from __future__ import annotations

from collections.abc import Sequence

from ._apiclient import APIClient
from .enums import Color
from .exceptions import APIResponseError
from .models import Tag


class TagClient:
    """Provides methods and models for Tag API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(self) -> Sequence[Tag]:
        """
        List all tags

        Returns:
            A sequence of Tag models, can be empty

        Raises:
            APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get("/tag")

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [Tag.build(data) for data in response.data]

    def get(self, tag_id: int) -> Tag:
        """
        Get Tag by id.

        Args:
            tag_id (int): Tag ID to request from TrackBear

        Returns:
            Tag model

        Raises:
            APIResponseError: On failure to retrieve requested model
        """
        response = self._api_client.get(f"/tag/{tag_id}")

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return Tag.build(response.data)

    def save(
        self,
        name: str,
        color: Color | str,
        tag_id: int | None = None,
    ) -> Tag:
        """
        Save a Tag.

        If `tag_id` is provided, then the existing tag is updated. Otherwise,
        a new tag is created.

        Args:
            name (str): The name of the tag
            color (enum | str): Color enum of the following: 'default', 'red', 'orange',
                'yellow', 'green', 'blue', 'purple', 'brown', 'white', 'black', 'gray'
            tag_id (int): Existing tag id if request is to update existing tag

        Returns:
            Tag object on success

        Raises:
            APIResponseError: On any failure message returned from TrackBear API
            ValueError: When `color` is not a valid value
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        if isinstance(color, Color):
            _color = color
        else:
            _color = Color(color)

        payload = {
            "name": name,
            "color": _color.value,
        }

        if tag_id is None:
            response = self._api_client.post("/tag", payload)
        else:
            response = self._api_client.patch(f"/tag/{tag_id}", payload)

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return Tag.build(response.data)

    def delete(self, tag_id: int) -> Tag:
        """
        Delete an existing tag.

        Args:
            tag_id (int): Existing tag id

        Returns:
            Tag object on success

        Raises:
            APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/tag/{tag_id}")

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return Tag.build(response.data)
