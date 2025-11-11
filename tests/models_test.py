from __future__ import annotations

import dataclasses
from typing import Any
from typing import Protocol

import pytest

from trackbear_api import models
from trackbear_api.exceptions import ModelBuildError

from . import test_parameters


class ModelType(Protocol):
    @classmethod
    def build(cls, data: dict[str, Any]) -> ModelType: ...


@pytest.mark.parametrize(
    "model_type",
    (
        models.Project,
        models.ProjectStub,
        models.Goal,
        models.Stat,
        models.Tag,
        models.Tally,
    ),
)
def test_build_model_failure(model_type: type[ModelType]) -> None:
    """Assert expected exception when model is built incorrectly."""
    name = model_type.__name__
    pattern = f"Failure to build the {name} model from the provided data"

    with pytest.raises(ModelBuildError, match=pattern):
        model_type.build({})


@pytest.mark.parametrize(
    "data,model_type",
    (
        (test_parameters.PROJECT_RESPONSE, models.Project),
        (test_parameters.PROJECTSTUB_RESPONSE, models.ProjectStub),
        (test_parameters.GOAL_RESPONSE_THRESHOLD, models.Goal),
        (test_parameters.GOAL_RESPONSE_HABIT_THRESHOLD, models.Goal),
        (test_parameters.GOAL_RESPONSE_HABIT, models.Goal),
        (test_parameters.STAT_RESPONSE, models.Stat),
        (test_parameters.TAG_RESPONSE, models.Tag),
        (test_parameters.TALLY_RESPONSE, models.Tally),
    ),
)
def test_build_model_success(data: dict[str, Any], model_type: type[ModelType]) -> None:
    """Assert models build correctly."""
    result = model_type.build(data)

    assert isinstance(result, model_type)
    assert dataclasses.is_dataclass(result)
    assert not isinstance(result, type)
    assert dataclasses.asdict(result) == test_parameters.keys_to_snake_case(data)
