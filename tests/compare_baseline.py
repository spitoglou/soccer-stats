#!/usr/bin/env python
"""Compare current output with baseline to verify optimizations don't change results."""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

FIXTURES_DIR = Path(__file__).parent / "fixtures"
COUNTRIES = ["greece", "italy", "england", "spain", "germany", "france"]


def load_baseline():
    filepath = FIXTURES_DIR / "baseline_stats.json"
    with open(filepath) as f:
        return json.load(f)


def get_current_stats():
    from sp_soccer_lib import create_team_df_dict
    from sp_soccer_lib.championships import load_country, team_stats

    current = {}
    for country in COUNTRIES:
        print(f"  Processing {country}...")
        df = load_country(country)
        team_dfs = create_team_df_dict(df)
        stats = team_stats(team_dfs)
        stats_rounded = stats.round(6)
        current[country] = {
            "stats": stats_rounded.to_dict(),
            "shape": list(stats.shape),
            "index": list(stats.index),
        }
    return current


def compare(baseline, current):
    errors = []
    for country in COUNTRIES:
        base = baseline[country]
        curr = current[country]

        # Check shape
        if base["shape"] != curr["shape"]:
            errors.append(f"{country}: Shape mismatch {base['shape']} vs {curr['shape']}")
            continue

        # Check teams
        if set(base["index"]) != set(curr["index"]):
            errors.append(f"{country}: Team names differ")
            continue

        # Check stats
        for col in base["stats"]:
            if col not in curr["stats"]:
                errors.append(f"{country}: Missing column {col}")
                continue
            for team in base["stats"][col]:
                base_val = base["stats"][col][team]
                curr_val = curr["stats"][col].get(team)

                # Handle None/NaN
                if base_val is None or (isinstance(base_val, float) and pd.isna(base_val)):
                    if curr_val is not None and not pd.isna(curr_val):
                        errors.append(f"{country}/{team}/{col}: Expected None, got {curr_val}")
                elif isinstance(base_val, float):
                    if curr_val is None or abs(base_val - curr_val) > 1e-4:
                        errors.append(f"{country}/{team}/{col}: {base_val} vs {curr_val}")
                else:
                    if base_val != curr_val:
                        errors.append(f"{country}/{team}/{col}: {base_val} vs {curr_val}")

    return errors


if __name__ == "__main__":
    print("Loading baseline...")
    baseline = load_baseline()

    print("Generating current output...")
    current = get_current_stats()

    print("Comparing...")
    errors = compare(baseline, current)

    if errors:
        print(f"\nFAILED: {len(errors)} differences found:")
        for e in errors[:20]:  # Show first 20
            print(f"  - {e}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
        sys.exit(1)
    else:
        print("\nSUCCESS: Output matches baseline!")
        sys.exit(0)
