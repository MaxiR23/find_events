# INFO: Entry point for top artists and their events worldwide.
from concurrent.futures import ThreadPoolExecutor

from find_events.config import TOP_ARTISTS_LIMIT
from find_events.exceptions import FetchError
from find_events.models import Artist
from find_events.service import fetch_top_artists, search_events

_MAX_WORKERS = 8


def _events_for(artist: Artist) -> dict | None:
    """Fetch one artist's events worldwide; return None on failure or no events."""
    try:
        events = search_events(query=artist.name)
    except FetchError:
        return None
    if not events:
        return None
    return {
        "artist": artist.to_dict(),
        "events": [e.to_dict() for e in events],
    }


def get_top_on_tour(limit: int = TOP_ARTISTS_LIMIT) -> list[dict]:
    """Return top artists that have at least one event, fetched in parallel."""
    artists = fetch_top_artists(limit)

    with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as executor:
        results = executor.map(_events_for, artists)

    return [r for r in results if r is not None]