# Statistics Specification

## Purpose

Documents the probability and draw-related calculations used in the soccer analytics platform for predicting match outcomes and analyzing team performance.
## Requirements
### Requirement: Period Draw Rate (p_draw)
The system SHALL calculate a team's draw rate based on matches played in the current period.

**Formula:**
```
p_draw = draws_in_period / total_matches_in_period
```

**Properties:**
- Range: 0.0 to 1.0
- Returns `None` if no matches in current period
- Based on actual match results, not betting odds

#### Scenario: Standard calculation
- **WHEN** a team has played 13 matches with 4 draws in the current period
- **THEN** `p_draw = 4/13 = 0.3077`

#### Scenario: No matches in period
- **WHEN** a team has not played any matches in the current period
- **THEN** `p_draw` is `None` (displayed as "N/A")

---

### Requirement: Cumulative Probability (c_prob)
The system SHALL calculate the probability of at least one draw occurring in the next N matches using betting odds and current no-draw streak.

**Formula:**
```
matches = NEXT_MATCHES + CurrentNoDraw
probability = 1 / B365D_mean
c_prob = P(X >= 1) where X ~ Binomial(matches, probability)
```

**Properties:**
- Uses Bet365 average draw odds converted to probability
- Window expands based on current no-draw streak (Gambler's Fallacy assumption)
- Higher values when team has longer no-draw streak

#### Scenario: Team with no-draw streak
- **WHEN** a team has `CurrentNoDraw = 5` and `B365D_mean = 3.5`
- **THEN** `matches = 5 + 5 = 10`
- **AND** `probability = 1/3.5 = 0.286`
- **AND** `c_prob = P(X >= 1)` over Binomial(10, 0.286)

#### Scenario: Statistical note
- **WHEN** interpreting `c_prob`
- **THEN** be aware it incorporates Gambler's Fallacy (past results affecting future probability)
- **AND** uses bookmaker odds which include margin

---

### Requirement: Adjusted Cumulative Probability (c_prob_adj)
The system SHALL calculate an adjusted cumulative probability without Gambler's Fallacy assumptions.

**Formula:**
```
matches = NEXT_MATCHES (fixed at 5)
c_prob_adj = P(X >= 1) where X ~ Binomial(matches, p_draw)
```

**Properties:**
- Uses fixed 5-match window (no streak adjustment)
- Based on actual period draw rate, not betting odds
- More statistically sound than `c_prob`
- Returns `None` if `p_draw` is unavailable

#### Scenario: Standard calculation
- **WHEN** a team has `p_draw = 0.1538`
- **THEN** `c_prob_adj = P(X >= 1)` over Binomial(5, 0.1538)
- **AND** result is approximately 0.5661

#### Scenario: Comparison with c_prob
- **WHEN** comparing `c_prob` and `c_prob_adj` for the same team
- **THEN** `c_prob_adj` typically shows lower, more realistic values
- **AND** `c_prob_adj` does not inflate based on no-draw streaks

---

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

### Requirement: Odds Conversion
The system SHALL convert between decimal odds and probability.

**Formulas:**
```
probability = 1 / decimal_odds
decimal_odds = 1 / probability
```

#### Scenario: Convert Bet365 odds to probability
- **WHEN** `B365D = 3.50` (decimal odds for draw)
- **THEN** `probability = 1/3.50 = 0.2857` (28.57%)

#### Scenario: Note on bookmaker margin
- **WHEN** using converted odds as probability
- **THEN** be aware this includes bookmaker margin (overround)
- **AND** true probability is slightly higher than implied

---

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

## Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| `NEXT_MATCHES` | 5 | Default lookahead window for probability calculations |
| `CURRENT_PERIOD` | "2526" | Current season (2025-2026) |

## Column Display Order

Statistics are displayed in the following order:
1. `W`, `D`, `L` - Wins, Draws, Losses
2. `GF`, `GA` - Goals For, Goals Against
3. `PTS` - Points
4. `CurrentNoDraw` - Current consecutive no-draw streak
5. `MaxNoDraw` - Maximum no-draw streak in history
6. `B365D_mean` - Average Bet365 draw odds
7. `p_draw` - Current period draw rate
8. `c_prob` - Cumulative probability (original)
9. `c_prob_adj` - Cumulative probability (adjusted)
