from __future__ import annotations

import pytest

from trackbear_api.exceptions import ModelBuildError
from trackbear_api.models import Project
from trackbear_api.models import ProjectStub


def test_project_model_optionals() -> None:
    """Assert optional fields are not required to build model."""
    mock_data = {
        "id": 123,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "string",
        "updatedAt": "string",
        "state": "string",
        "ownerId": 123,
        "title": "string",
        "description": "string",
        "phase": "string",
        "startingBalance": {},
        "cover": "string",
        "totals": {},
        "lastUpdated": "string",
    }

    model = Project.build(mock_data)

    assert model.id == 123


def test_project_model_failure() -> None:
    """Assert expected exception when Project model is built incorrectly."""
    mock_data = {
        "id": 123,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "string",
        "updatedAt": "string",
        "state": "string",
        "ownerId": 123,
        "title": "string",
        "description": "string",
        "phase": "string",
        "startingBalance": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
        "cover": "string",
        "starred": False,
        "displayOnProfile": False,
        "totals": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
        "lastUpdated": "string",
    }
    del mock_data["id"]
    pattern = "Failure to build the Project model from the provided data"

    with pytest.raises(ModelBuildError, match=pattern):
        Project.build(mock_data)


def test_projectstub_model_optionals() -> None:
    """Assert optional fields are not required to build model."""
    mock_data = {
        "id": 123,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "string",
        "updatedAt": "string",
        "state": "string",
        "ownerId": 123,
        "title": "string",
        "description": "string",
        "phase": "string",
        "startingBalance": {},
        "cover": "string",
    }

    model = ProjectStub.build(mock_data)

    assert model.id == 123


def test_projectstub_model_failure() -> None:
    """Assert expected exception when ProjectStub model is built incorrectly."""
    mock_data = {
        "id": 123,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "string",
        "updatedAt": "string",
        "state": "string",
        "ownerId": 123,
        "title": "string",
        "description": "string",
        "phase": "string",
        "startingBalance": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
        "cover": "string",
        "starred": False,
        "displayOnProfile": False,
    }
    del mock_data["id"]
    pattern = "Failure to build the ProjectStub model from the provided data"

    with pytest.raises(ModelBuildError, match=pattern):
        ProjectStub.build(mock_data)
