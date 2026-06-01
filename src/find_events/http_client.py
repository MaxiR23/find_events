# INFO: Thin HTTP client wrapper with shared headers and timeout.
import requests

from find_events.config import TIMEOUT, USER_AGENT
from find_events.exceptions import FetchError, ParseError

_HEADERS = {"User-Agent": USER_AGENT}


def _get(url: str, params: dict | None = None, headers: dict | None = None) -> requests.Response:
    merged = {**_HEADERS, **(headers or {})}
    try:
        response = requests.get(url, params=params, headers=merged, timeout=TIMEOUT)
        response.raise_for_status()
        return response
    except requests.RequestException as exc:
        raise FetchError(f"Failed to fetch {url}: {exc}") from exc


def get_html(url: str, params: dict | None = None, headers: dict | None = None) -> str:
    return _get(url, params=params, headers=headers).text


def get_json(url: str, params: dict | None = None, headers: dict | None = None) -> dict:
    response = _get(url, params=params, headers=headers)
    try:
        return response.json()
    except ValueError as exc:
        raise ParseError(f"Invalid JSON from {url}: {exc}") from exc