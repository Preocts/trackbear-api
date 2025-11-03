[![Python 3.10 | 3.11 | 3.12 | 3.13 | 3.14](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/downloads)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/trackbear-api/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/trackbear-api/main)
[![Python tests](https://github.com/Preocts/trackbear-api/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/trackbear-api/actions/workflows/python-tests.yml)
[![PyPI version](https://badge.fury.io/py/trackbear-api.svg)](https://badge.fury.io/py/trackbear-api)

# trackbear-api

- [Contributing Guide and Developer Setup Guide](./CONTRIBUTING.md)
- [License: MIT](./LICENSE)

---

### Deveploment in progress

Python library for using the Trackbear app API https://help.trackbear.app/api

## Installation

```console
python -m pip install trackbear-api
```

## Example use

### Defining a client

The client allows you to communicate with TrackBear's API. It requires your API
token and allows you to define a custom User-Agent header if desired.

```python
from trackbear_api import TrackBearClient

# If TRACKBEAR_API_TOKEN is set in the environment
client = TrackBearClient()

# To provide the API token directly
client = TrackBearClient(api_token="provide your token directly")

# GET a list of projects: https://help.trackbear.app/api/Projects_list
# POST, PATCH, DELETE are also available with the same behaviors
response = client.get("/project")

if not response.success:
    raise ValueError(f"Error: {response.error.code}: {response.error.message}")

print(f"| {'Project Id':^12} | {'Title':^30} | {'Word Count':^12} |")
print("-" * 64)
for project in projects:
    print(f'| {project["id"]:<12} | {project["title"]:<30} | {project["totals"]["word"]:<12} |')
```

### TrackBearResponse object

| Attribute             | Type | Description                                           |
| --------------------- | ---- | ----------------------------------------------------- |
| `.success`            | bool | True or False if the request was succesful.           |
| `.data`               | Any  | API response if `success` is True                     |
| `.error.code`         | str  | Error code if `success` is False                      |
| `.error.message`      | str  | Error message if `success` is False                   |
| `.status_code`        | int  | The HTTP status code of the response                  |
| `.remaining_requests` | int  | Number of requests remaining before rate limits apply |
| `.rate_reset`         | int  | Number of seconds before `remaining_requests` resets  |

### Rate Limiting

Rate limiting is defined by the TrackBear API here:
https://help.trackbear.app/api/rate-limits

This library does **not** enforce the rate limits. It is on the client to
monitor the returned rate limit information and act accordingly.

### Logging

All loggers use the name `trackbear-api`. No handlers are defined by default in
this library.

### Environment Variables

The following environment variables allow you to configure the TrackBearClient
outside of code. All variables listed below can also be set during the
initialization of the `TrackBearClient` as well.

| Variable            | Description                              | Has Default | Default                                                                   |
| ------------------- | ---------------------------------------- | ----------- | ------------------------------------------------------------------------- |
| TRACKBEAR_API_TOKEN | Your secret API token                    | False       |                                                                           |
| TRACKBEAR_API_URL   | The URL of the TrackBear API             | True        | https://trackbear.app/api/v1/                                             |
| TRACKBEAR_API_AGENT | The User-Agent header sent with requests | True        | trackbear-api/0.x.x (https://github.com/Preocts/trackbear-api) by Preocts |
