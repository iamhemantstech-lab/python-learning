"""
Live Proof: Memory Difference between List (return) vs Generator (yield)
========================================================================
Let's measure the exact RAM usage of 10,000,000 numbers in Python:
1. List approach: All 10,000,000 numbers loaded into RAM simultaneously.
2. Generator approach: 1 number yielded at a time, reusing the same memory slot.
"""

import sys
import tracemalloc
import time


def create_list(n: int):
    return [i for i in range(n)]


def create_generator(n: int):
    for i in range(n):
        yield i


if __name__ == "__main__":
    N = 5_000_000
    print("=" * 70)
    print(f"BENCHMARK: 5,000,000 ITEMS (LIST vs GENERATOR)")
    print("=" * 70)

    # 1. Benchmark List
    tracemalloc.start()
    t0 = time.perf_counter()
    my_list = create_list(N)
    t_list = time.perf_counter() - t0
    _, peak_list = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    list_ram_mb = round(peak_list / (1024 * 1024), 2)
    print(f" -> [List / return]:   RAM Used: {list_ram_mb} MB | Time: {t_list:.3f}s")
    del my_list  # Free memory

    # 2. Benchmark Generator
    tracemalloc.start()
    t0 = time.perf_counter()
    my_gen = create_generator(N)
    # Summing on the fly (1 by 1)
    total = sum(my_gen)
    t_gen = time.perf_counter() - t0
    _, peak_gen = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    gen_ram_mb = round(peak_gen / (1024 * 1024), 4)
    print(f" -> [Generator / yield]: RAM Used: {gen_ram_mb} MB | Time: {t_gen:.3f}s")

    print("\n" + "=" * 70)
    saved = round(list_ram_mb - gen_ram_mb, 2)
    print(f"RESULT: Generator saved {saved} MB of RAM! (Almost ZERO memory used!)")
    print("=" * 70)
