# INFO: Entry point - runs all event sources and prints results.
from find_events.top import get_top_on_tour
from find_events.upcoming import get_upcoming_argentina
from find_events.past import get_past_events


def _header(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)


def _line(date_str, artist, venue, city) -> str:
    return f"  {date_str or 'TBA'} | {artist or 'Unknown'} | {venue or 'TBA'} | {city or ''}"


def _print_events(events) -> None:
    """Print a list of Event objects with the unified format."""
    for e in events:
        print(_line(e.formatted_date(), e.artist_name, e.venue, e.city))


def main():
    _header("TOP ARTISTS ON TOUR")
    top = get_top_on_tour()
    if not top:
        print("  No top artists currently on tour.")
    for item in top:
        print(f"  {item['artist']['name']}")

    print()
    _header("UPCOMING EVENTS (AR)")
    upcoming = get_upcoming_argentina()
    if not upcoming:
        print("  No upcoming events found.")
    _print_events(upcoming)

    print()
    _header("PAST EVENTS (AR)")
    past = get_past_events()
    if not past:
        print("  No past events found.")
    _print_events(past)


if __name__ == "__main__":
    main()