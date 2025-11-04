from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from ._apiclient import APIClient
from .exceptions import APIResponseError
from .models import Project
from .models import ProjectStub


class ProjectClient:
    """Provides methods and models for Project API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(self) -> Sequence[Project]:
        """
        List all projects

        Returns:
            A sequence of Project models, can be empty

        Raises:
            APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get("/project")

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [Project.build(data) for data in response.data]

    def get(self, project_id: int) -> Project:
        """
        Get Project by id.

        Args:
            project_id (int): Project ID to request from TrackBear

        Returns:
            Project model

        Raises:
            APIResponseError: On failure to retrieve requested model
        """
        response = self._api_client.get(f"/project/{project_id}")

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return Project.build(response.data)

    def save(
        self,
        title: str,
        description: str,
        phase: Literal[
            "planning",
            "outlining",
            "drafting",
            "revising",
            "on hold",
            "finished",
            "abandoned",
        ],
        *,
        starred: bool = False,
        display_on_profile: bool = False,
        word: int = 0,
        time: int = 0,
        page: int = 0,
        chapter: int = 0,
        scene: int = 0,
        line: int = 0,
        project_id: int | None = None,
    ) -> ProjectStub:
        """
        Save a Project.

        If `project_id` is provided, then the existing project is updated. Otherwise,
        a new projec is created.

        NOTE: While updating an existing project, be mindful of default values.

        Args:
            title (str): Title of the Project
            description (str): Description of the Project
            phase (str): On of the following: `planning`, `outlining`, `drafting`,
                `revising`, `on hold`, `finished`, or `abandoned`.
            starred (bool): Star the project (default: False)
            display_on_profile (bool): Display project on public profile (default: False)
            word (int): Starting balance of words (default: 0)
            time (int): Starting balance of time (default: 0)
            page (int): Starting balance of pages (default: 0)
            chapter (int): Starting balance of chapters (default: 0)
            scene (int): Starting balance of scenes (default: 0)
            line (int): Starting balance of lines (default: 0)
            project_id (int): Existing project id if request is to update existing projects

        Returns:
            ProjectStub object on success

        Raises:
            APIResponseError: On any failure message returned from TrackBear API
        """
        payload = {
            "title": title,
            "description": description,
            "phase": phase,
            "startingBalance": {
                "word": word,
                "time": time,
                "page": page,
                "chapter": chapter,
                "scene": scene,
                "line": line,
            },
            "starred": starred,
            "displayOnProfile": display_on_profile,
        }

        if project_id is None:
            response = self._api_client.post("/project", payload)
        else:
            response = self._api_client.patch(f"/project/{project_id}", payload)

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return ProjectStub.build(response.data)

    def delete(self, project_id: int) -> ProjectStub:
        """
        Delete an existing project.

        Args:
            project_id (int): Existing project id if request is to update existing projects

        Returns:
            ProjectStub object on success

        Raises:
            APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/project/{project_id}")

        if not response.success:
            raise APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return ProjectStub.build(response.data)
