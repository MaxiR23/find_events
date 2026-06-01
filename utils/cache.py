# INFO: Disk-based TTL cache with a decorator. Persists across runs.
from functools import wraps
from pathlib import Path

from diskcache import Cache

CACHE_DIR = Path(".cache")
_cache = Cache(str(CACHE_DIR))


def _make_key(prefix: str, args: tuple, kwargs: dict) -> str:
    parts = [prefix, *(repr(a) for a in args)]
    parts += [f"{k}={v!r}" for k, v in sorted(kwargs.items())]
    return "|".join(parts)


def cached(ttl_seconds: int, key_prefix: str | None = None):
    def decorator(func):
        prefix = key_prefix or f"{func.__module__}.{func.__qualname__}"

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = _make_key(prefix, args, kwargs)

            cached_result = _cache.get(key)
            if cached_result is not None:
                return cached_result

            result = func(*args, **kwargs)
            _cache.set(key, result, expire=ttl_seconds)
            return result

        def _clear():
            keys = [k for k in _cache if isinstance(k, str) and k.startswith(prefix)]
            for k in keys:
                _cache.delete(k)

        wrapper.cache_clear = _clear
        return wrapper

    return decorator


def clear_all():
    _cache.clear()