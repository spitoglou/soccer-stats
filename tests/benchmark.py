#!/usr/bin/env python
"""Benchmark the optimized update pipeline."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sp_soccer_lib import create_team_df_dict
from sp_soccer_lib.championships import load_country, team_stats

COUNTRIES = ["greece", "italy", "england", "spain", "germany", "france"]


def benchmark():
    print("Benchmarking update pipeline performance...")
    print("=" * 50)

    total_start = time.time()

    for country in COUNTRIES:
        start = time.time()

        df = load_country(country)
        load_time = time.time() - start

        start = time.time()
        team_dfs = create_team_df_dict(df)
        create_time = time.time() - start

        start = time.time()
        stats = team_stats(team_dfs)
        stats_time = time.time() - start

        print(
            f"{country:10} | load: {load_time:.2f}s | create_dfs: {create_time:.2f}s | stats: {stats_time:.2f}s"
        )

    total_time = time.time() - total_start
    print("=" * 50)
    print(f"Total time: {total_time:.2f}s")

    return total_time


if __name__ == "__main__":
    benchmark()
