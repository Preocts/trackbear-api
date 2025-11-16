from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest

from trackbear_api import _validator as validators


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
