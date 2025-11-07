"""
All tests are run through the TrackBearClient which is the public API for the library.

Tests in this collection focus on the error handling and successful model building.
There is no focus on the underlying APIClient behavior as that is tested in the
trackbearclient_test.py collection.
"""

from __future__ import annotations

import copy
import json

import pytest
import responses
import responses.matchers

from trackbear_api import TrackBearClient
from trackbear_api.exceptions import APIResponseError
from trackbear_api.models import Balance
from trackbear_api.models import Stat

STAT_RESPONSE = {
    "date": "2021-03-23",
    "counts": {"word": 0, "time": 0, "page": 0, "chapter": 0, "scene": 0, "line": 0},
}


@responses.activate(assert_all_requests_are_fired=True)
def test_stat_list_success_with_params(client: TrackBearClient) -> None:
    """Assert the Stat model is built correctly."""
    mock_data = [copy.deepcopy(STAT_RESPONSE)] * 3
    mock_body = {"success": True, "data": mock_data}

    params = {"startDate": "2024-01-01", "endDate": "2025-01-01"}
    param_matcher = responses.matchers.query_param_matcher(params)

    responses.add(
        method="GET",
        status=200,
        url="https://trackbear.app/api/v1/stats/days",
        body=json.dumps(mock_body),
        match=[param_matcher],
    )

    stats = client.stat.list("2024-01-01", "2025-01-01")

    assert len(stats) == len(mock_data)

    for project in stats:
        assert isinstance(project, Stat)
        assert isinstance(project.counts, Balance)


def test_stat_list_raises_with_bad_start_date(client: TrackBearClient) -> None:
    """Assert the method raises ValueError with incorrect start date format."""
    pattern = "Invalid start_date 'foo'. Must be YYYY-MM-DD"

    with pytest.raises(ValueError, match=pattern):
        client.stat.list("foo", "2025-01-01")


def test_stat_list_raises_with_bad_end_date(client: TrackBearClient) -> None:
    """Assert the method raises ValueError with incorrect end date format."""
    pattern = "Invalid end_date 'bar'. Must be YYYY-MM-DD"

    with pytest.raises(ValueError, match=pattern):
        client.stat.list("2025-01-01", "bar")


@responses.activate(assert_all_requests_are_fired=True)
def test_stat_list_failure(client: TrackBearClient) -> None:
    """Assert a failure on the API side will raise the expected exception."""
    mock_body = {
        "success": False,
        "error": {
            "code": "SOME_ERROR_CODE",
            "message": "A human-readable error message",
        },
    }
    params: dict[str, str] = {}
    param_matcher = responses.matchers.query_param_matcher(params)
    pattern = r"TrackBear API Failure \(409\) SOME_ERROR_CODE - A human-readable error message"

    responses.add(
        method="GET",
        status=409,
        url="https://trackbear.app/api/v1/stats/days",
        body=json.dumps(mock_body),
        match=[param_matcher],
    )

    with pytest.raises(APIResponseError, match=pattern):
        client.stat.list()
