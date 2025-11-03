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

    def get_by_id(self, project_id: str) -> Project:
        """
        Get Project by id.

        Args:
            project_id (str): Project ID to request from TrackBear

        Returns:
            Project model

        Raises:
            APIResponseError: On failure to retrieve requested model
        """
        response = self._handle_request("GET", f"/project/{project_id}")

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return Project.build(response.data)
