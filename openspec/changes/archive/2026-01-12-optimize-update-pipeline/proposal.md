# Change: Optimize Update Pipeline Performance

## Why
The update pipeline (`update.py` → `soccer1.py` → `sp_soccer_lib/`) has significant performance issues including N+1 patterns, redundant data loading, slow pandas operations (`.iterrows()`, `.apply(lambda...)`), and inefficient caching. These issues compound across 6 countries × 20+ teams × 9 periods, causing unnecessary slowdowns during the daily update process.

## What Changes
- Replace `.iterrows()` with `.itertuples()` or vectorized operations (3-10x faster)
- Cache query results in `period_stats()` to eliminate redundant W/D/L filtering
- Pass pre-computed `team_dfs` to `frequency_graphs()` instead of reloading data
- Use vectorized operations (`np.where`, pandas masks) instead of `.apply(lambda...)`
- Convert `PATH_CACHE` from list to set for O(1) lookup in FTP transfers
- Fix unclosed file handles in `ftp_transfer.py` using context managers
- Fix typo `socket.gaierrora` → `socket.gaierror` and remove duplicate exception handler

## Impact
- Affected specs: `statistics`
- Affected code:
  - `sp_soccer_lib/__init__.py` (lines 24-32, 38, 53-82, 93-126)
  - `sp_soccer_lib/championships.py` (lines 177-193)
  - `ftp_transfer.py` (lines 34-51, 218-230, 244-254)
  - `soccer1.py` (lines 41, 62 - frequency_graphs calls)
