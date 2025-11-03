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

    success: bool = False
    data: Any = ""
    code: str = ""
    message: str = "Undefined Model"
    remaining_requests: int = 0
    rate_reset: int = 0
