# INFO: Text normalization helpers for matching names.
import re
import unicodedata

def normalize_name(value: str) -> str:
    if not value:
        return ""
    nfkd = unicodedata.normalize("NFKD", value)
    no_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", no_accents.lower())


def names_match(a: str, b: str) -> bool:
    norm_a = normalize_name(a)
    return bool(norm_a) and norm_a == normalize_name(b)