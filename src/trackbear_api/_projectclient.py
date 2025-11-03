from __future__ import annotations

from collections.abc import Sequence

from ._apiclient import APIClient
from .exceptions import APIResponseError
from .models import Project


class ProjectClient(APIClient):
    """Provides methods and models for Project API routes."""

    def list(self) -> Sequence[Project]:  # noqa: A003
        """
        List all projects

        Returns:
            A sequence of Project models, can be empty

        Raises:
            APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._handle_request("GET", "/project")

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [Project.build(data) for data in response.data]
