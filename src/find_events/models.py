# INFO: Domain models representing scraped entities.
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Event:
    date: Optional[datetime.date] = None
    artist_name: Optional[str] = None
    venue: Optional[str] = None
    city: Optional[str] = None
    tour: Optional[str] = None
    doors: Optional[str] = None
    start: Optional[str] = None
    url: Optional[str] = None

    def formatted_date(self) -> Optional[str]:
        return self.date.strftime("%d %b %Y") if self.date else None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["date"] = self.formatted_date()
        return data


@dataclass(frozen=True)
class Artist:
    id: int
    name: str
    picture: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)