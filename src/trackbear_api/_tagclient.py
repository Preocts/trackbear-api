from __future__ import annotations

from collections.abc import Sequence

from . import enums
from . import exceptions
from . import models
from ._apiclient import APIClient


class TagClient:
    """Provides methods and models for Tag API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(self) -> Sequence[models.Tag]:
        """
        List all tags

        Returns:
            A sequence of trackbear_api.models.Tag

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get("/tag")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [models.Tag.build(data) for data in response.data]

    def get(self, tag_id: int) -> models.Tag:
        """
        Get Tag by id.

        Args:
            tag_id (int): Tag ID to request from TrackBear

        Returns:
            Tag model

        Raises:
            exceptions.APIResponseError: On failure to retrieve requested model
        """
        response = self._api_client.get(f"/tag/{tag_id}")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Tag.build(response.data)

    def save(
        self,
        name: str,
        color: enums.Color | str,
        tag_id: int | None = None,
    ) -> models.Tag:
        """
        Save a models.Tag.

        If `tag_id` is provided, then the existing tag is updated. Otherwise,
        a new tag is created.

        Args:
            name (str): The name of the tag
            color (Color | str): Color enum of the following: 'default', 'red', 'orange',
                'yellow', 'green', 'blue', 'purple', 'brown', 'white', 'black', 'gray'
            tag_id (int): (Optional) Existing tag id if request is to update existing tag

        Returns:
            trackbear_api.models.Tag

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
            ValueError: When `color` is not a valid value
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        if isinstance(color, enums.Color):
            _color = color
        else:
            _color = enums.Color(color)

        payload = {
            "name": name,
            "color": _color.value,
        }

        if tag_id is None:
            response = self._api_client.post("/tag", payload)
        else:
            response = self._api_client.patch(f"/tag/{tag_id}", payload)

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Tag.build(response.data)

    def delete(self, tag_id: int) -> models.Tag:
        """
        Delete an existing tag.

        Args:
            tag_id (int): Existing tag id

        Returns:
            trackbear_api.models.Tag

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/tag/{tag_id}")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Tag.build(response.data)
