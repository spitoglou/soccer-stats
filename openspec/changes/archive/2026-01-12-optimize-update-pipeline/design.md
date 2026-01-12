## Context
The update pipeline processes 6 countries with 20+ teams each across 9 periods. Current implementation has O(N²) complexity in several places due to:
- Row-by-row iteration with `.iterrows()` and `.apply(lambda...)`
- Redundant data reloading in `frequency_graphs()`
- Multiple sequential queries for the same filtering criteria
- Linear cache lookups in FTP path checking

## Goals / Non-Goals
**Goals:**
- Reduce update pipeline execution time by 50%+
- Eliminate N+1 query patterns
- Use idiomatic pandas vectorized operations
- Fix resource leaks and error handling bugs

**Non-Goals:**
- Changing the output format or behavior
- Adding new features
- Modifying the data source or schema

## Decisions

### Decision 1: Replace `.iterrows()` with `.itertuples()` or vectorized ops
**Rationale:** `.iterrows()` creates a new Series per row with O(N) overhead. `.itertuples()` returns namedtuples (10x faster). Vectorized operations using `np.where()` or boolean masks are fastest.

**Affected locations:**
- `sp_soccer_lib/__init__.py:38` - `update_results()`
- `sp_soccer_lib/__init__.py:60` - `update_draw_streaks()`
- `sp_soccer_lib/__init__.py:120` - `no_draw_frequencies()`

### Decision 2: Cache filtered results in `period_stats()`
**Rationale:** Currently filters for W/D/L separately (3 queries). Instead, filter once and use value_counts().

**Before:**
```python
wins = team_df.query('result == "W" and period == "' + period + '"').shape[0]
draws = team_df.query('result == "D" and period == "' + period + '"').shape[0]
losses = team_df.query('result == "L" and period == "' + period + '"').shape[0]
```

**After:**
```python
period_df = team_df[team_df['period'] == period]
result_counts = period_df['result'].value_counts()
wins = result_counts.get('W', 0)
draws = result_counts.get('D', 0)
losses = result_counts.get('L', 0)
```

### Decision 3: Pass pre-computed `team_dfs` to `frequency_graphs()`
**Rationale:** `no_draw_frequencies()` calls `load_country()` and `create_team_df_dict()` again, duplicating work already done in the main loop.

**Solution:** Add optional `team_dfs` parameter to `no_draw_frequencies()` and `frequency_graphs()`.

### Decision 4: Replace `.apply(lambda...)` with vectorized operations
**Rationale:** `.apply()` with lambda is slow because it calls Python for each row.

**Before:**
```python
team_df["GF"] = team_df.apply(lambda row: calc_gf(row), axis=1)
team_df["GA"] = team_df.apply(lambda row: calc_ga(row), axis=1)
```

**After:**
```python
team_df["GF"] = np.where(team_df["home"], team_df["FTHG"], team_df["FTAG"])
team_df["GA"] = np.where(team_df["home"], team_df["FTAG"], team_df["FTHG"])
```

### Decision 5: Use set instead of list for PATH_CACHE
**Rationale:** `path not in list` is O(N), `path not in set` is O(1).

**Before:**
```python
PATH_CACHE = []
if path not in self.PATH_CACHE:
    self.PATH_CACHE.append(path)
```

**After:**
```python
PATH_CACHE = set()
if path not in self.PATH_CACHE:
    self.PATH_CACHE.add(path)
```

### Decision 6: Use context managers for file handles
**Rationale:** Prevents resource leaks if exceptions occur during FTP upload.

**Before:**
```python
f_h = open(filepath, 'rb')
# ... operations ...
f_h.close()
```

**After:**
```python
with open(filepath, 'rb') as f_h:
    # ... operations ...
```

### Decision 7: Fix exception handling bugs
- Fix typo: `socket.gaierrora` → `socket.gaierror`
- Remove duplicate `except OSError` handler

## Risks / Trade-offs
- **Risk:** Vectorized operations may behave differently with NaN values
  - **Mitigation:** Add unit tests for edge cases before refactoring
- **Risk:** Changing function signatures (adding `team_dfs` param) could break callers
  - **Mitigation:** Use optional parameter with default `None`

## Migration Plan
1. Add tests for current behavior (baseline)
2. Implement changes incrementally, validating output matches
3. Run full update pipeline and compare output files
4. Benchmark before/after times

## Open Questions
- None - all changes are internal optimizations with no behavior change
