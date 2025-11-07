from __future__ import annotations

import pytest

from trackbear_api.exceptions import ModelBuildError
from trackbear_api.models import Project
from trackbear_api.models import ProjectStub
from trackbear_api.models import Stat
from trackbear_api.models import Tag


def test_project_model_optionals() -> None:
    """Assert optional fields are not required to build model."""
    mock_data = {
        "id": 123,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "string",
        "updatedAt": "string",
        "state": "deleted",
        "ownerId": 123,
        "title": "string",
        "description": "string",
        "phase": "on hold",
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
        "state": "active",
        "ownerId": 123,
        "title": "string",
        "description": "string",
        "phase": "on hold",
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
        "state": "active",
        "ownerId": 123,
        "title": "string",
        "description": "string",
        "phase": "string",
        "startingBalance": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
        "cover": "string",
        "starred": False,
        "displayOnProfile": False,
    }

    pattern = "Failure to build the ProjectStub model from the provided data"

    with pytest.raises(ModelBuildError, match=pattern):
        ProjectStub.build(mock_data)


def test_tag_model_failure() -> None:
    """Assert expected exception when Tag model is built incorrectly."""
    mock_data = {
        "id": 123,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "string",
        "updatedAt": "string",
        "state": "string",
        "ownerId": 123,
        "name": "string",
        "color": "string",
    }

    pattern = "Failure to build the Tag model from the provided data"

    with pytest.raises(ModelBuildError, match=pattern):
        Tag.build(mock_data)


def test_stat_model_optionals() -> None:
    """Assert optional fields are not required to build model."""
    mock_data = {"date": "2021-03-23", "counts": {}}

    model = Stat.build(mock_data)

    assert model.date == "2021-03-23"
    assert model.counts.word == 0


def test_stat_model_failure() -> None:
    """Assert expected exception when Stat model is built incorrectly."""
    mock_data = {
        "counts": {
            "word": 0,
            "time": 0,
            "page": 0,
            "chapter": 0,
            "scene": 0,
            "line": 0,
        },
    }

    pattern = "Failure to build the Stat model from the provided data"

    with pytest.raises(ModelBuildError, match=pattern):
        Stat.build(mock_data)
