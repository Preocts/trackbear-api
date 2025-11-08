"""
All of the mock API repsonses by route type. Shared across tests
"""

from __future__ import annotations

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
