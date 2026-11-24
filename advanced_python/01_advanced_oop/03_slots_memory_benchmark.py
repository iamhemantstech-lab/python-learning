"""
Topic 1.3: Memory Optimization & Python Data Model: `__slots__` vs `__dict__`
=============================================================================
Under-The-Hood Mechanics:
By default, every standard Python object stores its attributes in an internal
dictionary called `__dict__`.
A Python dictionary has substantial memory overhead because it is a dynamic hash table.

When you define `__slots__ = ("id", "user_id", "token")`, Python:
1. PREVENTS the creation of `__dict__` for each instance.
2. Allocates a small, fixed-size C array of pointers in memory.
3. Typically saves 50% to 70% of RAM on high-volume backend objects!
"""

import sys
import tracemalloc
import time


# Standard Class (Uses dynamic __dict__)
class StandardSession:
    def __init__(self, session_id: int, user_id: int, ip_address: str, user_agent: str):
        self.session_id = session_id
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent


# Optimized Class (Uses fixed C-struct __slots__)
class OptimizedSession:
    __slots__ = ("session_id", "user_id", "ip_address", "user_agent")

    def __init__(self, session_id: int, user_id: int, ip_address: str, user_agent: str):
        self.session_id = session_id
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent


def benchmark_class(cls, num_objects: int = 500_000):
    tracemalloc.start()
    start_time = time.perf_counter()

    # Allocate 500,000 objects in memory
    objects = [
        cls(
            session_id=i,
            user_id=i * 2,
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        )
        for i in range(num_objects)
    ]

    elapsed = time.perf_counter() - start_time
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Cleanup memory
    del objects

    return {
        "time_seconds": round(elapsed, 3),
        "peak_ram_mb": round(peak_mem / (1024 * 1024), 2)
    }


if __name__ == "__main__":
    print("=" * 70)
    print("DEMO: MEMORY BENCHMARK - STANDARD CLASS vs __slots__")
    print("=" * 70)

    # 1. Structural Comparison
    s1 = StandardSession(1, 100, "127.0.0.1", "Chrome")
    s2 = OptimizedSession(1, 100, "127.0.0.1", "Chrome")

    print("\n[Under-the-Hood Inspection]")
    print(f"Standard object attributes live in __dict__: {s1.__dict__}")
    print(f"Has __dict__? -> Standard: {hasattr(s1, '__dict__')}, Optimized: {hasattr(s2, '__dict__')}")

    # 2. Running Live Benchmark
    NUM = 400_000
    print(f"\n[Running Memory Benchmark for {NUM:,} Objects in RAM...]")

    res_standard = benchmark_class(StandardSession, NUM)
    print(f" -> Standard Class:  RAM = {res_standard['peak_ram_mb']} MB | Time = {res_standard['time_seconds']}s")

    res_optimized = benchmark_class(OptimizedSession, NUM)
    print(f" -> Optimized Slots: RAM = {res_optimized['peak_ram_mb']} MB | Time = {res_optimized['time_seconds']}s")

    # Calculate Savings
    saved_ram = res_standard["peak_ram_mb"] - res_optimized["peak_ram_mb"]
    percent_saved = round((saved_ram / res_standard["peak_ram_mb"]) * 100, 1)

    print("\n" + "=" * 70)
    print(f"RESULTS: __slots__ saved {saved_ram:.1f} MB ({percent_saved}% LESS RAM!)")
    print("=" * 70)
