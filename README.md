[![Python 3.10 | 3.11 | 3.12 | 3.13 | 3.14](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/downloads)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Nox](https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg)](https://github.com/wntrblm/nox)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/trackbear-api/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/trackbear-api/main)
[![Python tests](https://github.com/Preocts/trackbear-api/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/trackbear-api/actions/workflows/python-tests.yml)

# trackbear-api

- [Contributing Guide and Developer Setup Guide](./CONTRIBUTING.md)
- [License: MIT](./LICENSE)

---

### Deveploment in progress

Python library for using the Trackbear app API https://help.trackbear.app/api

## Installation

tbd

## Example use

### Defining a client

The client allows you to communicate with TrackBear's API. It requires your API
token and allows you to define a custom User-Agent header if desired.

See the [.env.example](.env.example) file for which environment variables are
supported.

```python
from trackbear_api import TrackBearClient

# If TRACKBEAR_API_TOKEN is set in the environment
client = TrackBearClient()

# To provide the API token directly
client = TrackBearClient(api_token="provide your token directly")

# Default User-Agent header can be replaced directly or through the environment
client = TrackBearClient(user_agent="My Custom App/1.0 (https://...)")

# GET a list of projects: https://help.trackbear.app/api/Projects_list
# POST, PATCH, DELETE are also available with the same behaviors
response = client.get("/project")

if not response.success:
    raise ValueError(f"Error: {response.code}: {response.message}")

for project in response.data:
    print(project["title"])
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
