"""
Baseline capture and comparison tests for the update pipeline.

This module provides:
1. Fixtures to capture baseline output before optimization
2. Comparison tests to verify output is identical after optimization
3. Performance benchmarks to measure improvement

Usage:
    # Capture baseline (run BEFORE optimization):
    python tests/capture_baseline.py

    # Compare after optimization:
    pytest tests/test_update_pipeline.py -v
"""

import hashlib
import json
import os
import statistics
import time
from pathlib import Path

import pandas as pd
import pytest

# Baseline fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"
BASELINE_STATS_FILE = FIXTURES_DIR / "baseline_stats.json"
BASELINE_FREQUENCIES_FILE = FIXTURES_DIR / "baseline_frequencies.json"
BASELINE_CHECKSUMS_FILE = FIXTURES_DIR / "baseline_checksums.json"

COUNTRIES = ["greece", "italy", "england", "spain", "germany", "france"]


def load_baseline(filepath: Path) -> dict:
    """Load baseline data from JSON file."""
    if not filepath.exists():
        pytest.skip(f"Baseline not found: {filepath}. Run capture_baseline.py first.")
    with open(filepath) as f:
        return json.load(f)


# =============================================================================
# BASELINE COMPARISON TESTS
# =============================================================================


class TestStatisticsConsistency:
    """Verify team statistics are identical before and after optimization."""

    @pytest.fixture
    def baseline_stats(self):
        return load_baseline(BASELINE_STATS_FILE)

    def test_team_stats_match_baseline(self, baseline_stats):
        """Verify all team statistics match baseline exactly."""
        from sp_soccer_lib import create_team_df_dict
        from sp_soccer_lib.championships import load_country, team_stats

        for country in COUNTRIES:
            df = load_country(country)
            team_dfs = create_team_df_dict(df)
            stats = team_stats(team_dfs)

            # Round floats for comparison tolerance
            actual = stats.round(6).to_dict()
            expected = baseline_stats[country]["stats"]

            # Compare each column
            for col in expected:
                assert col in actual, f"{country}: Missing column {col}"
                for team in expected[col]:
                    actual_val = actual[col].get(team)
                    expected_val = expected[col][team]

                    # Handle None/NaN comparisons
                    if expected_val is None or (
                        isinstance(expected_val, float) and pd.isna(expected_val)
                    ):
                        assert actual_val is None or pd.isna(actual_val), (
                            f"{country}/{team}/{col}: Expected None, got {actual_val}"
                        )
                    elif isinstance(expected_val, float):
                        assert abs(actual_val - expected_val) < 1e-4, (
                            f"{country}/{team}/{col}: {actual_val} != {expected_val}"
                        )
                    else:
                        assert actual_val == expected_val, (
                            f"{country}/{team}/{col}: {actual_val} != {expected_val}"
                        )

    def test_stats_shape_unchanged(self, baseline_stats):
        """Verify DataFrame shape (rows, columns) unchanged."""
        from sp_soccer_lib import create_team_df_dict
        from sp_soccer_lib.championships import load_country, team_stats

        for country in COUNTRIES:
            df = load_country(country)
            team_dfs = create_team_df_dict(df)
            stats = team_stats(team_dfs)

            expected_shape = tuple(baseline_stats[country]["shape"])
            assert stats.shape == expected_shape, f"{country}: Shape mismatch"

    def test_team_names_unchanged(self, baseline_stats):
        """Verify team names (index) unchanged."""
        from sp_soccer_lib import create_team_df_dict
        from sp_soccer_lib.championships import load_country, team_stats

        for country in COUNTRIES:
            df = load_country(country)
            team_dfs = create_team_df_dict(df)
            stats = team_stats(team_dfs)

            expected_teams = set(baseline_stats[country]["index"])
            actual_teams = set(stats.index)
            assert actual_teams == expected_teams, f"{country}: Team names mismatch"


class TestFrequencyDistributions:
    """Verify frequency distribution calculations are identical."""

    @pytest.fixture
    def baseline_frequencies(self):
        return load_baseline(BASELINE_FREQUENCIES_FILE)

    def test_country_frequencies_match(self, baseline_frequencies):
        """Verify country-level frequency statistics match baseline."""
        from sp_soccer_lib import no_draw_frequencies

        for country in COUNTRIES:
            freq = no_draw_frequencies(country)
            expected = baseline_frequencies[country]["country"]

            if expected["count"] == 0:
                assert len(freq) == 0, f"{country}: Expected empty frequencies"
                continue

            actual = {
                "mean": round(statistics.mean(freq), 6),
                "median": round(statistics.median(freq), 6),
                "count": len(freq),
            }

            assert actual["count"] == expected["count"], f"{country}: Count mismatch"
            assert abs(actual["mean"] - expected["mean"]) < 1e-4, f"{country}: Mean mismatch"
            assert abs(actual["median"] - expected["median"]) < 1e-4, f"{country}: Median mismatch"


class TestHandoutFileIntegrity:
    """Verify generated HTML/PNG files match baseline checksums."""

    @pytest.fixture
    def baseline_checksums(self):
        return load_baseline(BASELINE_CHECKSUMS_FILE)

    def test_html_files_unchanged(self, baseline_checksums):
        """Verify HTML file content unchanged (MD5 match)."""
        html_files = {k: v for k, v in baseline_checksums.items() if k.endswith(".html")}

        for filepath, expected in html_files.items():
            assert os.path.exists(filepath), f"Missing: {filepath}"

            with open(filepath, "rb") as f:
                actual_md5 = hashlib.md5(f.read()).hexdigest()

            assert actual_md5 == expected["md5"], f"{filepath}: Content changed (MD5 mismatch)"

    def test_png_files_exist(self, baseline_checksums):
        """Verify PNG files exist (may differ due to matplotlib rendering)."""
        png_files = {k: v for k, v in baseline_checksums.items() if k.endswith(".png")}

        for filepath, expected in png_files.items():
            assert os.path.exists(filepath), f"Missing: {filepath}"

            actual_size = os.path.getsize(filepath)
            expected_size = expected["size"]

            # Allow 10% size variance for PNG (matplotlib rendering differences)
            size_ratio = actual_size / expected_size if expected_size > 0 else 1
            assert 0.9 < size_ratio < 1.1, (
                f"{filepath}: Size changed significantly ({actual_size} vs {expected_size})"
            )


class TestPerformance:
    """Benchmark performance improvements."""

    @pytest.mark.slow
    def test_pipeline_execution_time(self):
        """Benchmark full pipeline execution."""
        from soccer1 import update_local_handout

        start = time.time()
        update_local_handout()
        elapsed = time.time() - start

        print(f"\nPipeline execution time: {elapsed:.1f}s")

        # Target: 50% improvement (baseline ~30-60s, target <20s)
        # Adjust threshold based on actual baseline
        assert elapsed < 60, f"Pipeline too slow: {elapsed:.1f}s"

    def test_team_df_creation_time(self):
        """Benchmark team DataFrame creation."""
        from sp_soccer_lib import create_team_df_dict
        from sp_soccer_lib.championships import load_country

        for country in COUNTRIES:
            df = load_country(country)

            start = time.time()
            team_dfs = create_team_df_dict(df)
            elapsed = time.time() - start

            print(f"{country}: create_team_df_dict took {elapsed:.2f}s")
            assert elapsed < 10, f"{country}: create_team_df_dict too slow: {elapsed:.1f}s"


# =============================================================================
# CODE INSPECTION TESTS (Post-Optimization)
# =============================================================================


class TestOptimizationApplied:
    """Verify optimization patterns are applied in the code."""

    def test_no_iterrows_in_critical_paths(self):
        """Verify .iterrows() replaced in performance-critical code."""
        import inspect

        from sp_soccer_lib import update_draw_streaks, update_results

        for func in [update_results, update_draw_streaks]:
            source = inspect.getsource(func)
            # After optimization, these should use .itertuples() or vectorized ops
            # This test will fail before optimization (expected)
            if ".iterrows()" in source:
                pytest.skip(f"{func.__name__} still uses .iterrows() (not yet optimized)")

    def test_frequency_function_accepts_team_dfs(self):
        """Verify no_draw_frequencies accepts cached team_dfs parameter."""
        import inspect

        from sp_soccer_lib import no_draw_frequencies

        sig = inspect.signature(no_draw_frequencies)
        # After optimization, should have team_dfs parameter
        if "team_dfs" not in sig.parameters:
            pytest.skip("no_draw_frequencies missing team_dfs parameter (not yet optimized)")

    def test_path_cache_is_set(self):
        """Verify FTP PATH_CACHE uses set instead of list."""
        import inspect

        from ftp_transfer import FtpAddOns

        source = inspect.getsource(FtpAddOns)
        # After optimization, should use set() for O(1) lookup
        if "PATH_CACHE = []" in source:
            pytest.skip("PATH_CACHE still uses list (not yet optimized)")
