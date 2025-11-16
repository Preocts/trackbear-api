"""Validators validate inputs and raise exceptions as needed."""

from __future__ import annotations

import re
from typing import NoReturn

_DATE_PATTERN = re.compile(r"[\d]{4}-[\d]{2}-[\d]{2}")

__all__ = [
    "check_date",
]


def check_date(date: str | None) -> None | NoReturn:
    """
    Validate that the `date` is formatted as "YYYY-MM-DD".

    If `None` is provided, the validation is skipped in the assumption the value
    is an optional field.

    Args:
        date (str | None): The string to validate.

    Returns:
        None

    Raises:
        ValueError: When the `date` is not a valid format
    """
    if date is not None and _DATE_PATTERN.match(str(date)) is None:
        raise ValueError(f"Invalid date value: '{date}'. Must be YYYY-MM-DD")

    return None
