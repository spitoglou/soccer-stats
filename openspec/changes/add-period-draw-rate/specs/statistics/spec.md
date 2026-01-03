# Statistics Specification

## ADDED Requirements

### Requirement: Period Draw Rate Calculation
The system SHALL calculate a team's draw rate based on matches played in the current period.

#### Scenario: Team with matches in current period
- **WHEN** a team has played matches in the current period
- **THEN** `p_draw` is calculated as `draws / total_matches` for that period
- **AND** the value is a decimal between 0.0 and 1.0

#### Scenario: Team with no matches in current period
- **WHEN** a team has not played any matches in the current period
- **THEN** `p_draw` is set to `None` (displayed as "N/A")

#### Scenario: All draws in period
- **WHEN** a team has drawn all matches in the current period (e.g., 5 draws in 5 matches)
- **THEN** `p_draw` equals 1.0

#### Scenario: No draws in period
- **WHEN** a team has zero draws in the current period
- **THEN** `p_draw` equals 0.0

### Requirement: Period Draw Rate Display
The system SHALL display `p_draw` in the team statistics output alongside `c_prob`.

#### Scenario: Column ordering in output
- **WHEN** team statistics are displayed
- **THEN** `p_draw` column appears adjacent to `c_prob` column

#### Scenario: Decimal formatting
- **WHEN** `p_draw` has a numeric value
- **THEN** it is displayed with consistent decimal precision (matching `c_prob` format)

#### Scenario: N/A display
- **WHEN** `p_draw` is `None`
- **THEN** it is displayed as "N/A" or equivalent empty indicator in the output

### Requirement: Adjusted Cumulative Probability Calculation
The system SHALL calculate an adjusted cumulative probability without Gambler's Fallacy.

#### Scenario: Team with p_draw available
- **WHEN** a team has a valid `p_draw` value
- **THEN** `c_prob_adj` is calculated as `P(X >= 1)` where `X ~ Binomial(NEXT_MATCHES, p_draw)`
- **AND** the calculation uses a fixed window (NEXT_MATCHES = 5)
- **AND** does not incorporate CurrentNoDraw

#### Scenario: Team with no p_draw
- **WHEN** a team has `p_draw` as `None`
- **THEN** `c_prob_adj` is set to `None`

#### Scenario: Comparison with c_prob
- **WHEN** both `c_prob` and `c_prob_adj` are calculated
- **THEN** `c_prob_adj` typically shows lower values (fixed window vs expanding window)
- **AND** `c_prob_adj` is based on actual draw rate, not betting odds

### Requirement: Adjusted Probability Display
The system SHALL display `c_prob_adj` in the team statistics output alongside `c_prob`.

#### Scenario: Column ordering
- **WHEN** team statistics are displayed
- **THEN** columns appear in order: `p_draw`, `c_prob`, `c_prob_adj`
