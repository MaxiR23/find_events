# INFO: HTML parsing functions that turn raw markup into domain models.
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from .models import Event

NBSP = "\xa0"

def find_artist_path(html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    link = soup.select_one("a[href^='setlists/'][title*='setlists']")
    return link["href"] if link else None


def parse_upcoming_events(html: str, base_url: str) -> list[Event]:
    soup = BeautifulSoup(html, "html.parser")
    events: list[Event] = []

    for li in soup.select("li.setlist"):
        date_block = li.select_one("span.smallDateBlock")
        if not date_block:
            continue

        month = date_block.select_one("strong.text-uppercase").get_text(strip=True)
        day = date_block.select_one("strong.big").get_text(strip=True)
        year = date_block.select("span")[-1].get_text(strip=True)

        venue = li.select_one("div.column.content strong")
        city = li.select_one("span.subline")
        doors = li.select_one("span.doors")
        scheduled = li.select_one("span.scheduledStart")
        link = li.select_one("div.column.content a")

        events.append(Event(
            date=f"{day} {month} {year}",
            venue=venue.get_text(strip=True) if venue else None,
            city=city.get_text(strip=True) if city else None,
            doors=doors.get_text(strip=True).replace(NBSP, " ") if doors else None,
            scheduled=scheduled.get_text(strip=True).replace(NBSP, " ") if scheduled else None,
            url=urljoin(base_url, link["href"]) if link else None,
        ))

    return events