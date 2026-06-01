# INFO: Defensive helpers for HTML parsing.
from bs4 import Tag

NBSP = "\xa0"


def safe_text(node: Tag | None, selector: str | None = None) -> str | None:
    if node is None:
        return None
    target = node.select_one(selector) if selector else node
    if target is None:
        return None
    text = target.get_text(strip=True)
    return text or None


def safe_attr(node: Tag | None, attr: str) -> str | None:
    if node is None:
        return None
    value = node.get(attr)
    if not value:
        return None
    return value if isinstance(value, str) else str(value)


def clean_nbsp(text: str | None) -> str | None:
    if text is None:
        return None
    return text.replace(NBSP, " ")