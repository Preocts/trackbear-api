from __future__ import annotations

from collections.abc import Sequence

from . import enums
from . import exceptions
from . import models
from ._apiclient import APIClient


class ProjectClient:
    """Provides methods and models for Project API routes."""

    def __init__(self, api_client: APIClient) -> None:
        """Initialize client by providing defined APIClient."""
        self._api_client = api_client

    def list(self) -> Sequence[models.Project]:
        """
        List all projects

        Returns:
            A sequence of trackbear_api.models.Project

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.get("/project")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return [models.Project.build(data) for data in response.data]

    def get(self, project_id: int) -> models.Project:
        """
        Get Project by id.

        Args:
            project_id (int): Project ID to request from TrackBear

        Returns:
            trackbear_api.models.Project

        Raises:
            exceptions.APIResponseError: On failure to retrieve requested model
        """
        response = self._api_client.get(f"/project/{project_id}")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.Project.build(response.data)

    def save(
        self,
        title: str,
        description: str,
        phase: enums.Phase | str,
        *,
        starred: bool = False,
        display_on_profile: bool = False,
        word: int | None = None,
        time: int | None = None,
        page: int | None = None,
        chapter: int | None = None,
        scene: int | None = None,
        line: int | None = None,
        project_id: int | None = None,
    ) -> models.ProjectStub:
        """
        Save a Project.

        If `project_id` is provided, then the existing project is updated. Otherwise,
        a new projec is created.

        Args:
            title (str): Title of the Project
            description (str): Description of the Project
            phase (Phase | str): Phase enum of the following: `planning`, `outlining`,
                `drafting`, `revising`, `on hold`, `finished`, or `abandoned`.
            starred (bool): Star the project (default: False)
            display_on_profile (bool): Display project on public profile (default: False)
            word (int): (Optional) Starting balance of words
            time (int): (Optional) Starting balance of time
            page (int): (Optional) Starting balance of pages
            chapter (int): (Optional) Starting balance of chapters
            scene (int): (Optional) Starting balance of scenes
            line (int): (Optional) Starting balance of lines
            project_id (int): (Optional) Existing project id if request is to update
                existing projects

        Returns:
            trackbear.models.ProjectStub

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
            ValueError: When `phase` is not a valid value
        """
        # Forcing the use of the Enum here allows for fast failures at runtime if the
        # incorrect string is provided.
        if isinstance(phase, enums.Phase):
            _phase = phase
        else:
            _phase = enums.Phase(phase)

        balance = {
            "word": word,
            "time": time,
            "page": page,
            "chapter": chapter,
            "scene": scene,
            "line": line,
        }

        payload = {
            "title": title,
            "description": description,
            "phase": _phase.value,
            "startingBalance": {k: v for k, v, in balance.items() if v is not None},
            "starred": starred,
            "displayOnProfile": display_on_profile,
        }

        if project_id is None:
            response = self._api_client.post("/project", payload)
        else:
            response = self._api_client.patch(f"/project/{project_id}", payload)

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.ProjectStub.build(response.data)

    def delete(self, project_id: int) -> models.ProjectStub:
        """
        Delete an existing project.

        Args:
            project_id (int): Existing project id

        Returns:
            trackbear_api.models.ProjectStub

        Raises:
            exceptions.APIResponseError: On any failure message returned from TrackBear API
        """
        response = self._api_client.delete(f"/project/{project_id}")

        if not response.success:
            raise exceptions.APIResponseError(
                status_code=response.status_code,
                code=response.error.code,
                message=response.error.message,
            )

        return models.ProjectStub.build(response.data)
