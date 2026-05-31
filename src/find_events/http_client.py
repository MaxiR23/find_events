# INFO: Thin HTTP client wrapper around requests with shared headers and timeout.
import requests

from .config import USER_AGENT, TIMEOUT
from .exceptions import FetchError

_HEADERS = {"User-Agent": USER_AGENT}


def get_html(url: str, params: dict | None = None) -> str:
    try:
        response = requests.get(url, params=params, headers=_HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        raise FetchError(f"Failed to fetch {url}: {exc}") from exc