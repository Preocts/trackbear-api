from __future__ import annotations

import os
from collections.abc import Generator
from unittest.mock import patch

import pytest

from trackbear_api import TrackBearClient

ENVIRON = {
    "TRACKBEAR_API_TOKEN": "environ_value",
    "TRACKBEAR_API_AGENT": "environ_value",
    "TRACKBEAR_API_URL": "https://trackbear.app/api/v1",
    "TRACKBEAR_API_TIMEOUT_SECONDS": "3",
}


@pytest.fixture(autouse=True)
def clear_environ() -> Generator[None, None, None]:
    """Clears environ of all values."""
    with patch.dict(os.environ, {}, clear=True):
        yield None


@pytest.fixture()
def add_token() -> Generator[None, None, None]:
    """Adds only a mock token environment variable."""
    with patch.dict(os.environ, {"TRACKBEAR_API_TOKEN": ENVIRON["TRACKBEAR_API_TOKEN"]}):
        yield None


@pytest.fixture()
def add_environs() -> Generator[None, None, None]:
    """Adds mock environment variables."""
    with patch.dict(os.environ, ENVIRON):
        yield None


@pytest.fixture
def client(add_environs: None) -> TrackBearClient:
    """Create a mock TrackBearClient."""
    return TrackBearClient()
