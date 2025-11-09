"""
All tests are run through the TrackBearClient which is the public API for the library.

Tests in this collection focus on the error handling and successful model building.
There is no focus on the underlying APIClient behavior as that is tested in the
trackbearclient_test.py collection.
"""

from __future__ import annotations

import copy
import json

import responses

from trackbear_api import TrackBearClient
from trackbear_api.models import ProjectStub
from trackbear_api.models import Tag
from trackbear_api.models import Tally

from .test_parameters import TALLY_RESPONSE


@responses.activate(assert_all_requests_are_fired=True)
def test_tally_get_success(client: TrackBearClient) -> None:
    """Assert the Project model is built correctly."""
    mock_data = copy.deepcopy(TALLY_RESPONSE)
    mock_body = {"success": True, "data": mock_data}

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/tally/123",
        body=json.dumps(mock_body),
    )

    project = client.tally.get(123)

    assert isinstance(project, Tally)
    assert isinstance(project.work, ProjectStub)
    for tag in project.tags:
        assert isinstance(tag, Tag)
