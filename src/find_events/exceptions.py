# INFO: Custom exceptions raised by the find_events package.
class FindEventsError(Exception):
    """Base exception for all find_events errors."""


class ArtistNotFoundError(FindEventsError):
    """Raised when the searched artist cannot be found."""


class FetchError(FindEventsError):
    """Raised when an HTTP request fails."""