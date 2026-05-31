# INFO: Command-line entry point that asks for an artist and prints upcoming events.
import sys

from src.find_events import get_upcoming_events, ArtistNotFoundError, FetchError


def main() -> int:
    artist_name = input("Artist name: ").strip()
    if not artist_name:
        print("Error: artist name cannot be empty.")
        return 1

    try:
        events = get_upcoming_events(artist_name)
    except ArtistNotFoundError as exc:
        print(f"Not found: {exc}")
        return 1
    except FetchError as exc:
        print(f"Network error: {exc}")
        return 2

    if not events:
        print("No upcoming events.")
        return 0

    print(f"\nFound {len(events)} upcoming events:\n")
    for e in events:
        print(f"{e.date:15} | {(e.venue or '-'):40} | {e.city or '-'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())