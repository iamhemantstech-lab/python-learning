"""
Topic 2.3: Class-Based Decorators with __call__ & Stateful Decorators
=====================================================================
Deep Python Concept:
In Python, any object implementing the `__call__` dunder method is a CALLABLE.

Why write a decorator as a Class?
1. State Management: Classes can cleanly store state in `self` (counters, caches, metrics).
2. Helper Methods: You can attach utility methods like `func.clear_cache()` or `func.stats()`.
3. Readability: For complex decorators, `__init__` and `__call__` are often cleaner than 3 nested functions.
"""

from typing import Callable, Any
import functools
import time


# -----------------------------------------------------------------------------
# 1. THE CLASS-BASED CACHE DECORATOR (Stateful)
# -----------------------------------------------------------------------------
class SmartCache:
    """
    A class-based caching decorator that stores results in memory,
    tracks hit/miss statistics, and provides a method to clear the cache.
    """

    def __init__(self, func: Callable):
        self.func = func
        self.cache: dict[tuple, Any] = {}
        self.hits: int = 0
        self.misses: int = 0
        # Preserving original function metadata
        functools.update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # Build a hashable cache key from positional and keyword args
        key = (args, tuple(sorted(kwargs.items())))

        if key in self.cache:
            self.hits += 1
            print(f" [CACHE HIT] Returning cached result for args: {args}")
            return self.cache[key]

        self.misses += 1
        print(f" [CACHE MISS] Computing fresh result for args: {args}...")
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        return result

    def get_stats(self) -> dict:
        """Helper method exposed on the decorated function!"""
        total = self.hits + self.misses
        hit_ratio = round((self.hits / total * 100), 1) if total > 0 else 0.0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "cached_entries": len(self.cache),
            "hit_ratio_percent": hit_ratio
        }

    def clear_cache(self) -> None:
        """Allows resetting the cache programmatically."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        print(" [CACHE RESET] Cache cleared successfully.")


# -----------------------------------------------------------------------------
# 2. APPLYING THE CLASS DECORATOR
# -----------------------------------------------------------------------------
@SmartCache
def get_user_permissions(role: str) -> list[str]:
    """Simulates an expensive database query fetching role permissions."""
    time.sleep(0.1)  # Simulate DB latency
    permissions_db = {
        "admin": ["read", "write", "delete", "admin_dashboard"],
        "user": ["read", "profile_update"],
        "guest": ["read"]
    }
    return permissions_db.get(role, [])


# -----------------------------------------------------------------------------
# 3. DEMONSTRATION & VERIFICATION
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("DEMO: CLASS-BASED DECORATOR WITH __call__ AND ATTACHED METHODS")
    print("=" * 70)

    # 1. First calls (Misses - DB simulated queries)
    print("\n[Step 1: Fetching Permissions - Cache Misses]")
    print("Admin Perms:", get_user_permissions("admin"))
    print("User Perms: ", get_user_permissions("user"))

    # 2. Repeat calls (Hits - Instant in-memory retrieval)
    print("\n[Step 2: Fetching Same Permissions - Cache Hits]")
    print("Admin Perms:", get_user_permissions("admin"))
    print("Admin Perms:", get_user_permissions("admin"))
    print("User Perms: ", get_user_permissions("user"))

    # 3. Inspecting Statistics via the attached class method
    print("\n[Step 3: Checking Decorator Statistics via attached method]")
    print("Stats:", get_user_permissions.get_stats())

    # 4. Programmatic Cache Invalidation
    print("\n[Step 4: Clearing Cache Programmatically]")
    get_user_permissions.clear_cache()
    print("Stats after reset:", get_user_permissions.get_stats())

    print("\n" + "=" * 70)
    print("SUCCESS: Class-based decorator encapsulated state and provided helper APIs!")
    print("=" * 70)
