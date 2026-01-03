# Change: Add Current Period Draw Rate Statistic

## Why
The existing `c_prob` calculation uses a cumulative binomial probability over multiple future matches, which answers "probability of at least 1 draw in N matches" rather than "probability next match is a draw." Additionally, it incorporates `CurrentNoDraw` which introduces the Gambler's Fallacy assumption.

A simpler, more statistically sound metric is needed: the team's actual draw rate in the current period. This provides:
- A direct, interpretable probability for the next match
- Based on current season form (more predictive than historical averages)
- No gambler's fallacy assumptions

## What Changes
- Add new column `p_draw` (period draw rate) to team statistics output
- Calculate as: `draws_in_current_period / matches_in_current_period`
- Display "N/A" when no matches played in current period (e.g., season start)
- Add new column `c_prob_adj` (adjusted cumulative probability)
- Calculate as: `P(X >= 1)` where `X ~ Binomial(NEXT_MATCHES, p_draw)`
- Uses fixed 5-match window with current period draw rate (no Gambler's Fallacy)
- Place columns next to existing `c_prob` in output
- Keep existing `c_prob` calculation unchanged

## Impact
- **Affected specs**: statistics (new capability)
- **Affected code**:
  - `sp_soccer_lib/championships.py` - add `calc_period_draw_rate()` function
  - `sp_soccer_lib/championships.py` - add `calc_c_prob_adj()` function
  - `sp_soccer_lib/championships.py` - update `team_stats()` to include new columns
  - `soccer1.py` - add `p_draw` and `c_prob_adj` to displayed columns
- **No breaking changes**: existing `c_prob` preserved
