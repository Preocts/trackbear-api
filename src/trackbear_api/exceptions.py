"""Custom exceptions used by the trackbear-api library."""

from __future__ import annotations

import dataclasses

__all__ = [
    "ModelBuildError",
    "APIResponseError",
    "APITimeoutError",
]


@dataclasses.dataclass(frozen=True, slots=True)
class ModelBuildError(Exception):
    """
    Raised when a model fails to build from API data.

    Args:
        data_string (str): The data which caused the model build to fail
        model_name (str): The name of the model that failed
    """

    data_string: str
    model_name: str
    exception_type: str
    exception_str: str

    def __str__(self) -> str:
        msg = (
            f"Failure to build the {self.model_name} model from the provided data.\n\n"
            f"Exception type: {self.exception_type}\n"
            f"Exception __str__: {self.exception_str}\n\n"
            "Please provide the full stacktrace, with any preceding ERROR logs in a bug report.\n\n"
            f"{self.data_string=}"
        )
        return msg


@dataclasses.dataclass(frozen=True, slots=True)
class APIResponseError(Exception):
    """
    Raised when the TrackBear API returns an unsuccessful response.

    Args:
        status_code (int): HTTP status code turned by the API
        code (str): Error code provided by the API
        message (str): Human readable error message provided by the API
    """

    status_code: int
    code: str
    message: str

    def __str__(self) -> str:
        return f"TrackBear API Failure ({self.status_code}) {self.code} - {self.message}"


@dataclasses.dataclass(frozen=True, slots=True)
class APITimeoutError(Exception):
    """
    Raised when the TrackBear API request, read, or connection times out.

    Args:
        exception (Exception): Exception raised by internal HTTP library
        method (str): HTTP method
        url (str): Target URL
        timeout (int): Timeout length in seconds
    """

    exception: Exception
    method: str
    url: str
    timeout: int

    def __str__(self) -> str:
        return f"HTTP {self.method} timed out after {self.timeout} seconds. '{self.url}' - {self.exception}"
