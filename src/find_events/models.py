# INFO: Domain models representing scraped entities.
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class Event:
    date: str
    venue: Optional[str]
    city: Optional[str]
    doors: Optional[str]
    scheduled: Optional[str]
    url: Optional[str]

    def to_dict(self) -> dict:
        return asdict(self)