#!/usr/bin/env python
"""Quick baseline capture - stats only, skip slow frequency calculations."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURES_DIR.mkdir(exist_ok=True)

COUNTRIES = ["greece", "italy", "england", "spain", "germany", "france"]


def capture_team_stats() -> dict:
    from sp_soccer_lib import create_team_df_dict
    from sp_soccer_lib.championships import load_country, team_stats

    print("Capturing team statistics...")
    baseline = {}

    for country in COUNTRIES:
        print(f"  Processing {country}...")
        df = load_country(country)
        team_dfs = create_team_df_dict(df)
        stats = team_stats(team_dfs)
        stats_rounded = stats.round(6)

        baseline[country] = {
            "stats": stats_rounded.to_dict(),
            "shape": list(stats.shape),
            "index": list(stats.index),
            "columns": list(stats.columns),
        }

    return baseline


def json_serializer(obj):
    if hasattr(obj, "tolist"):
        return obj.tolist()
    if hasattr(obj, "item"):
        return obj.item()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


if __name__ == "__main__":
    stats = capture_team_stats()
    filepath = FIXTURES_DIR / "baseline_stats.json"
    with open(filepath, "w") as f:
        json.dump(stats, f, indent=2, default=json_serializer)
    print(f"Saved: {filepath}")
    print("Done!")
