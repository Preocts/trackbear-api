"""
All of the mock API repsonses by route type and helper functions. Shared across tests
"""

from __future__ import annotations

import re
from typing import Any

from trackbear_api import enums


def keys_to_snake_case(response: dict[str, Any]) -> dict[str, Any]:
    """Translate camelCase keys of response into snake_case."""
    result = {}
    new_value: Any

    for key, value in response.items():
        new_key = re.sub("([A-Z])", r"_\1", key).lower()

        if isinstance(value, list):
            new_value = [keys_to_snake_case(val) if isinstance(val, dict) else val for val in value]

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
PROJECT_SAVE_KWARGS = {
    "title": "Mock Title",
    "description": "Some description.",
    "phase": enums.Phase.DRAFTING,
    "starred": True,
    "display_on_profile": True,
    "word": 1000,
    "page": 10,
    "chapter": 0,
    "scene": 3,
}
PROJECT_SAVE_PAYLOAD = {
    "title": "Mock Title",
    "description": "Some description.",
    "phase": "drafting",
    "startingBalance": {
        "word": 1000,
        "page": 10,
        "chapter": 0,
        "scene": 3,
    },
    "starred": True,
    "displayOnProfile": True,
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

GOAL_RESPONSE_THRESHOLD = {
    "id": 123,
    "uuid": "8fb3e519-fc08-477f-a70e-4132eca599d4",
    "createdAt": "string",
    "updatedAt": "string",
    "state": "active",
    "ownerId": 123,
    "title": "string",
    "description": "string",
    "type": "target",
    "parameters": {"threshold": {"measure": "word", "count": 0}},
    "startDate": "string",
    "endDate": "string",
    "workIds": [123],
    "tagIds": [123],
    "starred": False,
    "displayOnProfile": False,
}
GOAL_RESPONSE_HABIT = GOAL_RESPONSE_THRESHOLD | {
    "type": "habit",
    "parameters": {"cadence": {"unit": "day", "period": 1}, "threshold": None},
}
GOAL_RESPONSE_HABIT_THRESHOLD = GOAL_RESPONSE_HABIT | {
    "parameters": {
        "cadence": {"unit": "day", "period": 1},
        "threshold": {"count": 1667, "measure": "word"},
    },
}
GOAL_SAVE_TARGET_KWARGS = {
    "title": "Target Goal",
    "description": "We'll crush this goal",
    "measure": enums.Measure.WORD,
    "count": 50000,
    "start_date": "2025-11-01",
    "end_date": "2025-11-30",
    "work_ids": [123],
}
GOAL_SAVE_TARGET_PAYLOAD = {
    "title": "Target Goal",
    "description": "We'll crush this goal",
    "type": "target",
    "parameters": {
        "threshold": {
            "measure": enums.Measure.WORD,
            "count": 50000,
        },
    },
    "startDate": "2025-11-01",
    "endDate": "2025-11-30",
    "workIds": [123],
    "tagIds": [],
    "starred": False,
    "displayOnProfile": False,
}
GOAL_SAVE_HABIT_KWARGS = GOAL_SAVE_TARGET_KWARGS | {
    "unit": enums.HabitUnit.DAY,
    "period": 12,
    "measure": None,
    "count": None,
}
GOAL_SAVE_HABIT_PAYLOAD = GOAL_SAVE_TARGET_PAYLOAD | {
    "type": "habit",
    "parameters": {"cadence": {"unit": "day", "period": 12}, "threshold": None},
}
GOAL_SAVE_HABIT_TARGET_KWARGS = GOAL_SAVE_TARGET_KWARGS | {
    "unit": enums.HabitUnit.DAY,
    "period": 12,
    "measure": enums.Measure.CHAPTER,
    "count": 1,
}
GOAL_SAVE_HABIT_TARGET_PAYLOAD = GOAL_SAVE_TARGET_PAYLOAD | {
    "type": "habit",
    "parameters": {
        "cadence": {"unit": "day", "period": 12},
        "threshold": {"measure": "chapter", "count": 1},
    },
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
TAG_SAVE_KWARGS = {
    "name": "Mock Tag",
    "color": enums.Color.BLUE,
}
TAG_SAVE_PAYLOAD = {
    "name": "Mock Tag",
    "color": "blue",
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
TALLY_SAVE_KWARGS = {
    "work_id": 123,
    "date": "2025-01-01",
    "measure": enums.Measure.SCENE,
    "count": 69,
    "note": "Some Note",
    "tags": ["New Tag"],
    "set_total": True,
}
TALLY_SAVE_PAYLOAD = {
    "date": "2025-01-01",
    "measure": "scene",
    "count": 69,
    "note": "Some Note",
    "workId": 123,
    "setTotal": True,
    "tags": ["New Tag"],
}
