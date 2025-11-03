from __future__ import annotations

import os
from collections.abc import Generator
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def clear_environ() -> Generator[None, None, None]:
    """Clears environ of all values."""
    with patch.dict(os.environ, {}, clear=True):
        yield None


@pytest.fixture()
def add_environ_token() -> Generator[None, None, None]:
    """Add a mock TRACKBEAR_API_TOKEN value to environ."""
    with patch.dict(os.environ, {"TRACKBEAR_API_TOKEN": "environ_value"}):
        yield None


@pytest.fixture()
def add_environ_useragent() -> Generator[None, None, None]:
    """Add a mock TRACKBEAR_API_AGENT value to environ."""
    with patch.dict(os.environ, {"TRACKBEAR_API_AGENT": "environ_value"}):
        yield None


@pytest.fixture()
def add_environ_url() -> Generator[None, None, None]:
    """Add a mock TRACKBEAR_API_URL value to environ."""
    with patch.dict(os.environ, {"TRACKBEAR_API_URL": "environ_value"}):
        yield None
