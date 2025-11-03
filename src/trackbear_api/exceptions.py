"""Custom exceptions used by the trackbear-api library."""

from __future__ import annotations

import dataclasses

__all__ = [
    "ModelBuildError",
]


@dataclasses.dataclass(frozen=True, slots=True)
class ModelBuildError(Exception):
    """Raised when a model fails to build from API data."""

    data_string: str
    model_name: str

    def __str__(self) -> str:
        msg = (
            f"Failure to build the {self.model_name} model from the provided data.\n\n"
            "Please provide the full stacktrace, with any preceding ERROR logs in a bug report.\n\n"
            f"{self.data_string=}"
        )
        return msg


@dataclasses.dataclass(frozen=True, slots=True)
class APIResponseError(Exception):
    """Raised when the TrackBear API returns an unsuccessful response."""

    status_code: int
    code: str
    message: str

    def __str__(self) -> str:
        return f"TrackBear API Failure ({self.status_code}) {self.code} - {self.message}"
