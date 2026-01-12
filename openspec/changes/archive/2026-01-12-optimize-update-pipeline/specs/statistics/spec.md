## MODIFIED Requirements

### Requirement: Binomial Probability Calculations
The system SHALL provide exact and cumulative binomial probability functions using vectorized operations for performance.

**Exact Binomial Formula:**
```
P(X = k) = C(n,k) * p^k * (1-p)^(n-k)

where:
  n = number of trials
  k = number of successes
  p = probability of success
  C(n,k) = n! / (k! * (n-k)!)
```

**Cumulative Probabilities:**
```
P(X < k)  = sum of P(X = i) for i = 0 to k-1
P(X <= k) = sum of P(X = i) for i = 0 to k
P(X > k)  = sum of P(X = i) for i = k+1 to n
P(X >= k) = sum of P(X = i) for i = k to n
```

**Implementation:**
- Probability calculations SHALL use vectorized numpy/scipy operations when applied to DataFrames
- Row-by-row `.apply(lambda...)` SHALL NOT be used for probability calculations
- Batch calculations SHALL be preferred over iterative single-row calculations

#### Scenario: Probability of at least 1 draw
- **WHEN** calculating probability of at least 1 draw in 5 matches with p=0.30
- **THEN** `P(X >= 1) = 1 - P(X = 0) = 1 - (0.70)^5 = 0.8319`

#### Scenario: Batch probability calculation
- **WHEN** calculating `c_prob` for all teams in a championship
- **THEN** the system SHALL compute probabilities for all teams in a single vectorized operation
- **AND** avoid calling probability functions row-by-row

---

## ADDED Requirements

### Requirement: Statistics Query Optimization
The system SHALL optimize DataFrame queries to avoid redundant filtering operations.

**Properties:**
- Multiple queries on the same filter criteria SHALL be combined into a single filter operation
- Result counts (W/D/L) SHALL be computed using `value_counts()` instead of separate queries
- Goals (GF/GA) SHALL be computed using vectorized `np.where()` instead of row-by-row apply

#### Scenario: Period statistics calculation
- **WHEN** calculating wins, draws, and losses for a team in a period
- **THEN** the system SHALL filter the DataFrame once for the period
- **AND** use `value_counts()` to count results in a single operation

#### Scenario: Goals calculation
- **WHEN** calculating goals for (GF) and goals against (GA)
- **THEN** the system SHALL use `np.where(home_mask, FTHG, FTAG)` for GF
- **AND** use `np.where(home_mask, FTAG, FTHG)` for GA
- **AND** avoid row-by-row lambda functions

---

### Requirement: Data Caching
The system SHALL cache computed team DataFrames to avoid redundant processing.

**Properties:**
- Pre-computed `team_dfs` dictionaries SHALL be passed to downstream functions when available
- Functions SHALL accept optional cached data parameters with `None` defaults for backwards compatibility
- Data SHALL NOT be reloaded from source when cached data is available

#### Scenario: Frequency graph generation
- **WHEN** generating frequency graphs after computing team statistics
- **THEN** the pre-computed `team_dfs` dictionary SHALL be reused
- **AND** the system SHALL NOT reload country data from source

#### Scenario: Backwards compatibility
- **WHEN** cached data parameter is `None` or not provided
- **THEN** the function SHALL load data from source as before
- **AND** existing callers without cached data SHALL continue to work

---

### Requirement: Efficient DataFrame Iteration
The system SHALL use efficient iteration methods for DataFrame row processing.

**Properties:**
- `.iterrows()` SHALL NOT be used for performance-critical operations
- `.itertuples()` SHALL be preferred when row iteration is necessary (10x faster)
- Vectorized operations SHALL be preferred over any iteration when possible

#### Scenario: Draw streak calculation
- **WHEN** calculating consecutive draw/no-draw streaks
- **THEN** the system SHALL use `.itertuples()` instead of `.iterrows()`
- **AND** maintain the same streak calculation logic

#### Scenario: Result aggregation
- **WHEN** aggregating match results across teams
- **THEN** vectorized pandas operations SHALL be used where possible
- **AND** iteration SHALL only be used when state must be tracked across rows
