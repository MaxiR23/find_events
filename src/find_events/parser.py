# INFO: HTML parsing functions that turn raw markup into domain models.
from datetime import date
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from find_events.models import Event
from utils.parsing import clean_nbsp, safe_attr, safe_text

_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def find_artist_link(html: str) -> tuple[str, str] | None:
    """Return (relative_path, display_name) of the first artist link, or None."""
    soup = BeautifulSoup(html, "html.parser")
    link = soup.select_one("a[href^='setlists/'][title*='setlists']")
    if link is None:
        return None
    href = safe_attr(link, "href")
    if not href:
        return None
    display_name = safe_text(link) or safe_attr(link, "title") or ""
    return href, display_name


def _parse_event(li: Tag, page_url: str) -> Event | None:
    date_block = li.select_one("span.smallDateBlock")
    if date_block is None:
        return None

    month = safe_text(date_block, "strong.text-uppercase")
    day = safe_text(date_block, "strong.big")
    year_nodes = date_block.select("span")
    year = safe_text(year_nodes[-1]) if year_nodes else None

    if not (month and day and year):
        return None

    href = safe_attr(li.select_one("div.column.content a"), "href")

    return Event(
        date=_build_date(day, month, year),
        venue=safe_text(li, "div.column.content strong"),
        city=safe_text(li, "span.subline"),
        doors=clean_nbsp(safe_text(li, "span.doors")),
        start=clean_nbsp(safe_text(li, "span.scheduledStart")),
        url=urljoin(page_url, href) if href else None,
    )


def parse_upcoming_events(html: str, page_url: str) -> list[Event]:
    soup = BeautifulSoup(html, "html.parser")
    events: list[Event] = []

    for li in soup.select("li.setlist"):
        try:
            event = _parse_event(li, page_url)
        except Exception:
            # Skip malformed item; keep the rest of the list usable.
            continue
        if event is not None:
            events.append(event)

    return events


def _build_date(day: str | None, month: str | None, year: str | None) -> date | None:
    """Turn scraped day/month/year strings into a real date, or None."""
    if not (day and month and year):
        return None
    month_num = _MONTHS.get(month[:3].lower())
    if not month_num:
        return None
    try:
        return date(int(year), month_num, int(day))
    except ValueError:
        return None


def _detail_by_label(details: Tag, label: str) -> str | None:
    """Read a labelled value (Artist / Tour / Venue) from a .details block."""
    for span in details.select("span"):
        text = safe_text(span)
        if text and text.lower().startswith(label.lower()):
            return safe_text(span, "strong")
    return None


def _parse_preview(item: Tag) -> Event | None:
    date_block = item.select_one("div.dateBlock")
    event_date = _build_date(
        safe_text(date_block, ".day") if date_block else None,
        safe_text(date_block, ".month") if date_block else None,
        safe_text(date_block, ".year") if date_block else None,
    )

    details = item.select_one("div.details")
    artist = tour = venue = city = None
    if details:
        artist = _detail_by_label(details, "Artist")
        tour = _detail_by_label(details, "Tour")
        venue_full = _detail_by_label(details, "Venue")
        if venue_full:
            parts = [p.strip() for p in venue_full.split(",")]
            venue = parts[0] or None
            city = ", ".join(parts[1:]) or None if len(parts) > 1 else None

    doors = start = None
    times = item.select_one("div.setlistPreviewSetTimes")
    if times:
        time_nodes = times.select("span.text-lowercase")
        if len(time_nodes) >= 1:
            doors = clean_nbsp(safe_text(time_nodes[0]))
        if len(time_nodes) >= 2:
            start = clean_nbsp(safe_text(time_nodes[1]))

    return Event(
        date=event_date,
        artist_name=artist,
        venue=venue,
        city=city,
        tour=tour,
        doors=doors,
        start=start,
    )


def parse_setlist_previews(html: str) -> list[Event]:
    """Parse the .setlistPreview cards returned by the site search page."""
    soup = BeautifulSoup(html, "html.parser")
    events: list[Event] = []

    for item in soup.select("div.setlistPreview"):
        try:
            event = _parse_preview(item)
        except Exception:
            # Skip malformed card; keep the rest of the list usable.
            continue
        if event is not None:
            events.append(event)

    return events