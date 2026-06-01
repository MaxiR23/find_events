# INFO: Service for fetching upcoming events in Argentina.
from datetime import date

from find_events.models import Event
from find_events.service import search_events


def get_upcoming_argentina() -> list[Event]:
    """Return upcoming events in Argentina."""
    return search_events(query="Argentina", year=date.today().year)