# INFO: High-level use case that coordinates HTTP fetching and HTML parsing.
from urllib.parse import urljoin

from .config import BASE_URL
from .http_client import get_html
from .parser import find_artist_path, parse_upcoming_events
from .models import Event
from .exceptions import ArtistNotFoundError


def get_upcoming_events(artist_name: str) -> list[Event]:
    search_html = get_html(f"{BASE_URL}search", params={"query": artist_name})

    artist_path = find_artist_path(search_html)
    if not artist_path:
        raise ArtistNotFoundError(f"Artist '{artist_name}' was not found.")

    artist_url = urljoin(BASE_URL, artist_path)
    artist_html = get_html(artist_url)

    return parse_upcoming_events(artist_html, artist_url)