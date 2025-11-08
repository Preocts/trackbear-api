"""
All of the mock API repsonses by route type and helper functions. Shared across tests
"""

from __future__ import annotations

import re
from typing import Any


def keys_to_snake_case(response: dict[str, Any]) -> dict[str, Any]:
    """Translate camelCase keys of response into snake_case."""
    result = {}
    new_value: Any

    for key, value in response.items():
        new_key = re.sub("([A-Z])", r"_\1", key).lower()

        if isinstance(value, list):
            new_value = [keys_to_snake_case(val) for val in value]

        elif isinstance(value, dict):
            new_value = keys_to_snake_case(value)

        else:
            new_value = value

        result[new_key] = new_value

    return result


PROJECT_RESPONSE = {
    "id": 123,
    "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
    "createdAt": "2025-01-01",
    "updatedAt": "2025-02-02",
    "state": "active",
    "ownerId": 123,
    "title": "New Project",
    "description": "This is a mock project for some tests.",
    "phase": "planning",
    "startingBalance": {"word": 1667, "time": 0, "page": 2, "chapter": 0, "scene": 0, "line": 0},
    "cover": "string",
    "starred": True,
    "displayOnProfile": True,
    "totals": {"word": 1667, "time": 0, "page": 2, "chapter": 0, "scene": 0, "line": 0},
    "lastUpdated": "2025-02-02",
}

PROJECTSTUB_RESPONSE = {
    "id": 123,
    "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
    "createdAt": "2025-01-01",
    "updatedAt": "2025-02-02",
    "state": "active",
    "ownerId": 123,
    "title": "New Project",
    "description": "This is a mock project for some tests.",
    "phase": "planning",
    "startingBalance": {"word": 1667, "time": 0, "page": 2, "chapter": 0, "scene": 0, "line": 0},
    "cover": "string",
    "starred": True,
    "displayOnProfile": True,
}

STAT_RESPONSE = {
    "date": "2021-03-23",
    "counts": {"word": 1000, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
}

TAG_RESPONSE = {
    "id": 123,
    "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
    "createdAt": "2025-01-01",
    "updatedAt": "2025-02-02",
    "state": "active",
    "ownerId": 678,
    "name": "Pure Awesome",
    "color": "red",
}

TALLY_RESPONSE = {
    "id": 123,
    "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
    "createdAt": "2025-01-01",
    "updatedAt": "2025-02-02",
    "state": "active",
    "ownerId": 123,
    "date": "2021-03-23",
    "measure": "word",
    "count": 1667,
    "note": "Did well, enough.",
    "workId": 456,
    "work": {
        "id": 456,
        "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
        "createdAt": "2025-01-01",
        "updatedAt": "2025-02-02",
        "state": "active",
        "ownerId": 123,
        "title": "Some Awesome Project",
        "description": "This truly rocks",
        "phase": "planning",
        "startingBalance": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
        "cover": "string",
        "starred": True,
        "displayOnProfile": True,
    },
    "tags": [
        {
            "id": 987,
            "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
            "createdAt": "2025-01-02",
            "updatedAt": "2025-01-03",
            "state": "active",
            "ownerId": 123,
            "name": "DaBomb",
            "color": "blue",
        }
    ],
}
