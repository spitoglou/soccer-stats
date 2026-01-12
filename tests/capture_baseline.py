#!/usr/bin/env python
"""
Capture baseline snapshots for the update pipeline.

Run this script BEFORE applying optimizations to capture the expected output.
The baseline files will be used by test_update_pipeline.py to verify
that optimizations don't change the output.

Usage:
    python tests/capture_baseline.py

Output:
    tests/fixtures/baseline_stats.json
    tests/fixtures/baseline_frequencies.json
    tests/fixtures/baseline_checksums.json
"""

import hashlib
import json
import os
import statistics
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

FIXTURES_DIR = Path(__file__).parent / "fixtures"
COUNTRIES = ["greece", "italy", "england", "spain", "germany", "france"]


def capture_team_stats() -> dict:
    """Capture team statistics for all countries."""
    from sp_soccer_lib import create_team_df_dict
    from sp_soccer_lib.championships import load_country, team_stats

    print("Capturing team statistics...")
    baseline = {}

    for country in COUNTRIES:
        print(f"  Processing {country}...")
        df = load_country(country)
        team_dfs = create_team_df_dict(df)
        stats = team_stats(team_dfs)

        # Convert to serializable format
        # Round floats to avoid floating point comparison issues
        stats_rounded = stats.round(6)

        baseline[country] = {
            "stats": stats_rounded.to_dict(),
            "shape": list(stats.shape),
            "index": list(stats.index),
            "columns": list(stats.columns),
        }

    return baseline


def capture_frequencies() -> dict:
    """Capture frequency distribution statistics."""
    from sp_soccer_lib import (
        championship_teams,
        create_team_df_dict,
        no_draw_frequencies,
    )
    from sp_soccer_lib.championships import load_country

    print("Capturing frequency distributions...")
    baseline = {}

    for country in COUNTRIES:
        print(f"  Processing {country}...")
        baseline[country] = {}

        # Country-level frequencies
        freq = no_draw_frequencies(country)
        if freq:
            baseline[country]["country"] = {
                "mean": round(statistics.mean(freq), 6),
                "median": round(statistics.median(freq), 6),
                "count": len(freq),
                "frequencies": freq,  # Store raw data for detailed comparison
            }
        else:
            baseline[country]["country"] = {
                "mean": None,
                "median": None,
                "count": 0,
                "frequencies": [],
            }

        # Per-team frequencies (optional, more detailed)
        df = load_country(country)
        team_dfs = create_team_df_dict(df)
        teams = championship_teams(df)

        baseline[country]["teams"] = {}
        for team in teams:
            try:
                freq = no_draw_frequencies(country, [team])
                if freq and len(freq) >= 2:
                    baseline[country]["teams"][team] = {
                        "mean": round(statistics.mean(freq), 6),
                        "median": round(statistics.median(freq), 6),
                        "count": len(freq),
                    }
                else:
                    baseline[country]["teams"][team] = {
                        "mean": None,
                        "median": None,
                        "count": len(freq) if freq else 0,
                    }
            except statistics.StatisticsError:
                baseline[country]["teams"][team] = {"mean": None, "median": None, "count": 0}

    return baseline


def capture_handout_checksums() -> dict:
    """Capture MD5 checksums of generated handout files."""
    print("Capturing handout file checksums...")

    handout_dir = Path("handout")
    if not handout_dir.exists():
        print("  Warning: handout/ directory not found. Run update first.")
        return {}

    baseline = {}
    file_count = 0

    for filepath in handout_dir.rglob("*"):
        if filepath.is_file() and filepath.suffix in (".html", ".png", ".css", ".js"):
            relative_path = str(filepath.relative_to(Path.cwd()))
            # Normalize path separators for cross-platform
            relative_path = relative_path.replace("\\", "/")

            with open(filepath, "rb") as f:
                content = f.read()
                baseline[relative_path] = {
                    "size": len(content),
                    "md5": hashlib.md5(content).hexdigest(),
                }
                file_count += 1

    print(f"  Captured {file_count} files")
    return baseline


def save_baseline(data: dict, filepath: Path):
    """Save baseline data to JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Custom JSON encoder for handling special types
    def json_serializer(obj):
        if hasattr(obj, "tolist"):  # numpy arrays
            return obj.tolist()
        if hasattr(obj, "item"):  # numpy scalars
            return obj.item()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=json_serializer)

    print(f"  Saved: {filepath}")


def main():
    print("=" * 60)
    print("BASELINE CAPTURE FOR UPDATE PIPELINE")
    print("=" * 60)
    print()

    # Capture all baselines
    stats = capture_team_stats()
    frequencies = capture_frequencies()
    checksums = capture_handout_checksums()

    # Save to fixtures directory
    print()
    print("Saving baseline files...")
    save_baseline(stats, FIXTURES_DIR / "baseline_stats.json")
    save_baseline(frequencies, FIXTURES_DIR / "baseline_frequencies.json")
    save_baseline(checksums, FIXTURES_DIR / "baseline_checksums.json")

    print()
    print("=" * 60)
    print("BASELINE CAPTURE COMPLETE")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Commit these baseline files to version control")
    print("  2. Apply optimizations to the codebase")
    print("  3. Run: pytest tests/test_update_pipeline.py -v")
    print("  4. All tests should pass if output is unchanged")
    print()


if __name__ == "__main__":
    main()
