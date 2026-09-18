import time
from collections import defaultdict
from typing import Dict, List

from backend.config import settings


class RateLimiter:
    """Simple in-memory rate limiter keyed by IP address.

    Each key has a sliding window of timestamps.
    Requests exceeding the limit within the window are rejected.
    """

    def __init__(self, limit: int = 5, window: int = 60):
        self.limit = limit
        self.window = window
        self._requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        """Returns True if the request is allowed (under limit)."""
        now = time.time()
        cutoff = now - self.window

        # Prune expired timestamps
        self._requests[key] = [
            ts for ts in self._requests[key] if ts > cutoff
        ]

        if len(self._requests[key]) >= self.limit:
            return False

        self._requests[key].append(now)
        return True


order_limiter = RateLimiter(
    limit=settings.rate_limit_orders,
    window=settings.rate_limit_window,
)

feedback_limiter = RateLimiter(
    limit=settings.rate_limit_feedback,
    window=settings.rate_limit_window,
)
