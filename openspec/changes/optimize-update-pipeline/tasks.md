## 1. Preparation (Baseline Capture)
- [ ] 1.1 Run `python tests/capture_baseline.py` to capture current output
- [ ] 1.2 Commit baseline files (`tests/fixtures/baseline_*.json`) to version control
- [ ] 1.3 Verify baseline tests pass: `pytest tests/test_update_pipeline.py -v`

## 2. Fix Critical N+1 Patterns
- [ ] 2.1 Refactor `period_stats()` to filter once and use `value_counts()` (`sp_soccer_lib/__init__.py:93-107`)
- [ ] 2.2 Refactor `team_stats()` probability calculations to avoid row-by-row apply (`sp_soccer_lib/championships.py:192-193`)

## 3. Replace iterrows() with Faster Alternatives
- [ ] 3.1 Refactor `update_results()` to use `.itertuples()` or vectorized ops (`sp_soccer_lib/__init__.py:38`)
- [ ] 3.2 Refactor `update_draw_streaks()` to use `.itertuples()` (`sp_soccer_lib/__init__.py:60`)
- [ ] 3.3 Refactor `no_draw_frequencies()` loop to use `.itertuples()` (`sp_soccer_lib/__init__.py:120`)

## 4. Eliminate Redundant Data Loading
- [ ] 4.1 Add optional `team_dfs` parameter to `no_draw_frequencies()` (`sp_soccer_lib/__init__.py:110-126`)
- [ ] 4.2 Update `frequency_graphs()` to accept and pass `team_dfs` (`soccer1.py:41,62`)
- [ ] 4.3 Update callers in `soccer1.py` to pass pre-computed `team_dfs`

## 5. Replace apply(lambda) with Vectorized Operations
- [ ] 5.1 Replace `calc_gf`/`calc_ga` apply with `np.where()` (`sp_soccer_lib/__init__.py:103-104`)
- [ ] 5.2 Replace `calc_c_prob`/`calc_c_prob_adj` apply with vectorized operations (`sp_soccer_lib/championships.py:192-193`)

## 6. Fix FTP Transfer Issues
- [ ] 6.1 Convert `PATH_CACHE` from list to set (`ftp_transfer.py:34-51`)
- [ ] 6.2 Use context manager for file handles in `upload_all()` (`ftp_transfer.py:244-254`)
- [ ] 6.3 Fix `socket.gaierrora` typo to `socket.gaierror` (`ftp_transfer.py:218`)
- [ ] 6.4 Remove duplicate `except OSError` handler (`ftp_transfer.py:218-230`)

## 7. Validation
- [ ] 7.1 Run `pytest tests/test_update_pipeline.py -v` and verify all tests pass
- [ ] 7.2 Run `python soccer1.py` and verify handout output matches baseline checksums
- [ ] 7.3 Run `pytest tests/test_update_pipeline.py::TestPerformance -v` and document improvement
- [ ] 7.4 Verify optimization patterns applied: `pytest tests/test_update_pipeline.py::TestOptimizationApplied -v`
