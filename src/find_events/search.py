# INFO: Reusable core for searching events via the site search page.
from find_events.config import BASE_URL, CACHE_TTL_SECONDS
from find_events.http_client import get_html
from find_events.models import Event
from find_events.parser import parse_setlist_previews
from utils.cache import cached


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