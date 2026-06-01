# INFO: High-level service that coordinates fetching, parsing and validation.
from urllib.parse import urljoin

from find_events.config import (
    BASE_URL,
    CACHE_TTL_SECONDS,
    TOP_ARTISTS_LIMIT,
    TOP_CHART_URL,
)
from find_events.exceptions import ArtistNotFoundError
from find_events.http_client import get_html, get_json
from find_events.models import Artist, Event
from find_events.parser import (
    find_artist_link,
    parse_setlist_previews,
    parse_upcoming_events,
)
from utils.cache import cached
from utils.text import names_match


@cached(ttl_seconds=CACHE_TTL_SECONDS, key_prefix="top_artists")
def fetch_top_artists(limit: int = TOP_ARTISTS_LIMIT) -> list[Artist]:
    data = get_json(TOP_CHART_URL, params={"limit": limit})
    items = data.get("data", []) if isinstance(data, dict) else []
    return [
        Artist(
            id=item["id"],
            name=item["name"],
            picture=item.get("picture_medium"),
        )
        for item in items
        if "id" in item and "name" in item
    ]


@cached(ttl_seconds=CACHE_TTL_SECONDS, key_prefix="search_events")
def search_events(
    query: str | None = None,
    artist: str | None = None,
    year: int | None = None,
) -> list[Event]:
    """Search setlist.fm and return parsed events.

    All arguments are optional filters mapped to the site's search params.
    Returns an empty list when nothing matches.
    """
    params: dict[str, str | int] = {}
    if query:
        params["query"] = query
    if artist:
        params["artist"] = artist
    if year:
        params["year"] = year

    html = get_html(f"{BASE_URL}search", params=params)
    return parse_setlist_previews(html)


@cached(ttl_seconds=CACHE_TTL_SECONDS, key_prefix="upcoming_events")
def get_upcoming_events(artist_name: str) -> list[Event]:
    search_html = get_html(f"{BASE_URL}search", params={"query": artist_name})

    link = find_artist_link(search_html)
    if link is None:
        raise ArtistNotFoundError(f"Artist '{artist_name}' was not found.")

    artist_path, display_name = link

    if not names_match(artist_name, display_name):
        raise ArtistNotFoundError(
            f"Top result '{display_name}' does not match '{artist_name}'."
        )

    artist_url = urljoin(BASE_URL, artist_path)
    artist_html = get_html(artist_url)

    return parse_upcoming_events(artist_html, artist_url)