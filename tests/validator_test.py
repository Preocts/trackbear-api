from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest

from trackbear_api import _validator as validators
from trackbear_api import exceptions
from trackbear_api import models


@pytest.mark.parametrize(
    "date,expected",
    (
        ("YYYY-DD-MM", pytest.raises(ValueError, match="Invalid date value")),
        ("foobar", pytest.raises(ValueError, match="Invalid date value")),
        (2005, pytest.raises(ValueError, match="Invalid date value")),
        ("2025-11-01", does_not_raise()),
        ("9999-99-99", does_not_raise()),  # Maybe we should test for valid ranges?
        (None, does_not_raise()),
    ),
)
def test_check_date(date: str | None, expected: Any) -> None:
    """Check that dates are validated correctly."""
    with expected:
        validators.check_date(date)


def test_check_response_success() -> None:
    response = models.TrackBearResponse.build(
        response={"success": True, "data": {}, "status_code": 200},
        remaining_requests=100,
        rate_reset=60,
        status_code=200,
    )

    validators.check_response(response)


def test_check_response_failure() -> None:
    response = models.TrackBearResponse.build(
        response={"success": False, "error": {"code": "foo", "message": "bar"}, "status_code": 429},
        remaining_requests=0,
        rate_reset=60,
        status_code=429,
    )

    with pytest.raises(exceptions.APIResponseError) as exception:
        validators.check_response(response)

    assert exception.value.status_code == 429
    assert exception.value.code == "foo"
    assert exception.value.message == "bar"
