[![Python 3.10 | 3.11 | 3.12 | 3.13 | 3.14](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/downloads)
[![PyPI - Version](https://img.shields.io/pypi/v/trackbear-api)](https://pypi.org/project/trackbear-api)
[![Python tests](https://github.com/Preocts/trackbear-api/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/trackbear-api/actions/workflows/python-tests.yml)


[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/trackbear-api/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/trackbear-api/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)

# trackbear-api

- [Contributing Guide and Developer Setup Guide](./CONTRIBUTING.md)
- [License: MIT](./LICENSE)

---

Python library for synchronous HTTP calls to the Trackbear API (https://help.trackbear.app/api)

- [TrackBear app](https://trackbear.app)
- [TrackBear API documentation](https://help.trackbear.app/api)

**Deveploment in progress, expect breaking changes frequently until version 0.1.0**

Implemented routes:

- Tallies
- Projects
- Tags
- Stats
- Goals

Routes pending implementation:

- Leaderboards
- Leaderboard Teams
- Leaderboard Members
- Leaderboard Participation
- Other

Features pending implementation:

- Rate limit exceptions

## Installation

```console
python -m pip install trackbear-api
```

## Environment Variables

The following environment variables allow you to configure the TrackBearClient
outside of code. All variables listed below can also be set during the
initialization of the `TrackBearClient` as well.

| Variable                      | Description                              | Has Default | Default                                                                   |
| ----------------------------- | ---------------------------------------- | ----------- | ------------------------------------------------------------------------- |
| TRACKBEAR_API_TOKEN           | Your secret API token                    | False       |                                                                           |
| TRACKBEAR_API_URL             | The URL of the TrackBear API             | True        | https://trackbear.app/api/v1/                                             |
| TRACKBEAR_API_AGENT           | The User-Agent header sent with requests | True        | trackbear-api/0.x.x (https://github.com/Preocts/trackbear-api) by Preocts |
| TRACKBEAR_API_TIMEOUT_SECONDS | Seconds before HTTPS reqeusts timeout    | True        | 10                                                                        |

## Example Use

The `TrackBearClient` give you all of the access to the TrackBear API. Various
routes of the API, such as Projects, are available through the `TrackBearClient`
from their respective attribute.

Error handling removed for brevity.

```python
from trackbear_api import TrackBearClient
from trackbear_api.enums import Phase

# Assumes TRACKBEAR_API_TOKEN is set in the environment
client = TrackBearClient()

# Create a new Project
new_project = client.project.save(
    title="My new TrackBear project",
    description="This will be an amazing story!",
    phase=Phase.OUTLINING,  # "outlining" as a string works here too
    starred=True,
    word=1667,
)

print(f"New Project created ({new_project.id}) '{new_project.title}'")

# List all projects
projects = client.project.list()

print(f"| {'Project Id':^12} | {'Title':^30} | {'Word Count':^12} |")
print("-" * 64)
for project in projects:
    print(f"| {project.id:<12} | {project.title:<30} | {project.totals.word:<12} |")
```

## Library API

The library's API is build to match TrackBear's API general structure.

https://help.trackbear.app/api/

### Tallies

| Provider Method         | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| `TrackBearClient.tally` | Contains helper methods for all Tally related routes |

| Method      | Description                              |
| ----------- | ---------------------------------------- |
| `.list()`   | Get all tallies, or filter by parameters |
| `.get()`    | Get a tally by specific id               |
| `.save()`   | Create or update tally                   |
| `.delete()` | Delete a tally by its id                 |

### Projects

| Provider Method           | Description                                            |
| ------------------------- | ------------------------------------------------------ |
| `TrackBearClient.project` | Contains helper methods for all Project related routes |

| Method      | Description                  |
| ----------- | ---------------------------- |
| `.list()`   | Get all projects             |
| `.get()`    | Get a project by specific id |
| `.save()`   | Create or update project     |
| `.delete()` | Delete a project by its id   |

### Goals

| Provider Method        | Description                                         |
| ---------------------- | --------------------------------------------------- |
| `TrackBearClient.goal` | Contains helper methods for all Goal related routes |

| Method           | Description                  |
| ---------------- | ---------------------------- |
| `.list()`        | Get all goals                |
| `.get()`         | Get a goal by specific id    |
| `.save_target()` | Create or update target goal |
| `.save_habit()`  | Create or update habit goal  |  |
| `.delete()`      | Delete a goal by its id      |

### Tags

| Provider Method       | Description                                        |
| --------------------- | -------------------------------------------------- |
| `TrackBearClient.tag` | Contains helper methods for all Tag related routes |

| Method      | Description              |
| ----------- | ------------------------ |
| `.list()`   | Get all tags             |
| `.get()`    | Get a tag by specific id |
| `.save()`   | Create or update tag     |
| `.delete()` | Delete a tag by its id   |

### Stats

| Provider Method        | Description                                         |
| ---------------------- | --------------------------------------------------- |
| `TrackBearClient.stat` | Contains helper methods for all Stat related routes |

| Method    | Description                              |
| --------- | ---------------------------------------- |
| `.list()` | Get stats. By default returns all stats. |

### Bare Access

Bare access to the API allows you to escape from the structured return models
and call routes directly. These methods return a `models.TrackBearResponse` object.

| Provider Method        | Description                                         |
| ---------------------- | --------------------------------------------------- |
| `TrackBearClient.bare` | Escape hatch allowing manually defined calls to API |

| Method      | Description                      |
| ----------- | -------------------------------- |
| `.get()`    | HTTP GET to the TrackBear API    |
| `.post()`   | HTTP POST to the TrackBear API   |
| `.patch()`  | HTTP PATCH to the TrackBear API  |
| `.delete()` | HTTP DELETE to the TrackBear API |

#### trackbear_api.models.TrackBearResponse

| Attribute             | Type | Description                                           |
| --------------------- | ---- | ----------------------------------------------------- |
| `.success`            | bool | True or False if the request was succesful.           |
| `.data`               | Any  | API response if `success` is True                     |
| `.error.code`         | str  | Error code if `success` is False                      |
| `.error.message`      | str  | Error message if `success` is False                   |
| `.status_code`        | int  | The HTTP status code of the response                  |
| `.remaining_requests` | int  | Number of requests remaining before rate limits apply |
| `.rate_reset`         | int  | Number of seconds before `remaining_requests` resets  |

## Exceptions

The library defines a handful of useful custom exceptions.

#### trackbear_api.exceptions.ModelBuildError(Exception)

Raised when building a dataclass model from the API response fails. This can
indicate the expected response has changed from the observed response. The
exception contains the model name that failed and the data the model attempted
to build with. Both are vital for bug reports.

| Attribute     | Type | Description                                   |
| ------------- | ---- | --------------------------------------------- |
| `data_string` | str  | The data which caused the model build to fail |
| `model_name`  | str  | The name of the model that failed             |

#### trackbear_api.exceptions.APIResponseError(Exception)

Raised by all provider methods when the API returns an unsuccessful response.

| Attribute     | Type | Description                                      |
| ------------- | ---- | ------------------------------------------------ |
| `status_code` | int  | HTTP status code returned by the API             |
| `code`        | str  | Error code provided by the API                   |
| `message`     | str  | Human readable error message provided by the API |

#### trackbear_api.exceptions.APITimeoutError(Exception)

Raised when the TrackBear API request, read, or connection times out.

| Attribute   | Type      | Description                               |
| ----------- | --------- | ----------------------------------------- |
| `exception` | Exception | Exception raised by internal HTTP library |
| `method`    | str       | HTTP method                               |
| `url`       | str       | Target URL                                |
| `timeout`   | int       | Timeout length in seconds                 |

---

### Rate Limiting

Rate limiting is defined by the TrackBear API here:
https://help.trackbear.app/api/rate-limits

This library does **not** presently enforce the rate limits.

### Logging

All loggers use the name `trackbear-api`. No handlers are defined by default in
this library.
