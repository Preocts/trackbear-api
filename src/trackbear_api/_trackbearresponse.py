from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass(slots=True, frozen=True)
class TrackBearResponse:
    """
    TrackBear API response Model.

    Always check `success` before processing additional attributes.

    When `success` is True: `data` will be available for processing

    When `success` is False: `code` and `message` will be available for processing
    """

    success: bool
    data: Any
    error: Error
    status_code: int
    remaining_requests: int
    rate_reset: int

    @classmethod
    def build(
        cls,
        response: dict[str, Any],
        remaining_requests: int,
        rate_reset: int,
        status_code: int,
    ) -> TrackBearResponse:
        """Bulid a model from request response data."""
        success = response["success"]

        return cls(
            success=success,
            data=response["data"] if success else "",
            error=Error(
                code=response["error"]["code"] if not success else "",
                message=response["error"]["message"] if not success else "",
            ),
            status_code=status_code,
            remaining_requests=remaining_requests,
            rate_reset=rate_reset,
        )


@dataclasses.dataclass(slots=True, frozen=True)
class Error:
    code: str
    message: str
