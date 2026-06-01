# INFO: Service for fetching past events from external API.
from datetime import datetime

from find_events.config import (
    CACHE_TTL_SECONDS,
    API_KEY,
    API_URL,
)
from find_events.http_client import get_json
from find_events.models import Event
from utils.cache import cached

_API_HEADERS = {
    "Accept": "application/json",
    "x-api-key": API_KEY,
}


def _parse_event_date(raw: str | None):
    """Parse the API's dd-MM-yyyy date string into a real date, or None."""
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%d-%m-%Y").date()
    except ValueError:
        return None


def _parse_setlist(item: dict) -> Event | None:
    try:
        event_date = _parse_event_date(item.get("eventDate"))
        if event_date is None:
            return None

        artist = item.get("artist", {})
        venue = item.get("venue", {})
        city_info = venue.get("city", {})
        country_info = city_info.get("country", {})

        city_parts = [city_info.get("name", ""), country_info.get("name", "")]
        city_str = ", ".join(p for p in city_parts if p) or None

        return Event(
            date=event_date,
            venue=venue.get("name"),
            city=city_str,
            url=item.get("url"),
            artist_name=artist.get("name"),
        )
    except Exception:
        return None


@cached(ttl_seconds=CACHE_TTL_SECONDS, key_prefix="past_events")
def get_past_events(country_code: str = "AR", page: int = 1) -> list[Event]:
    base = API_URL.rstrip("/")
    data = get_json(
        f"{base}/search/setlists",
        params={"countryCode": country_code, "p": page},
        headers=_API_HEADERS,
    )
    items = data.get("setlist", []) if isinstance(data, dict) else []
    events = []
    for item in items:
        event = _parse_setlist(item)
        if event is not None:
            events.append(event)
    return events