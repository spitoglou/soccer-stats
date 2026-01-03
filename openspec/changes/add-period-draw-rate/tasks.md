# Tasks: Add Current Period Draw Rate Statistic

## 1. Core Calculation
- [ ] 1.1 Add `calc_period_draw_rate(team_df, period)` function to `sp_soccer_lib/championships.py`
- [ ] 1.2 Function returns draw count / match count for specified period
- [ ] 1.3 Return `None` if no matches in period (handles season start)

## 2. Integration with team_stats
- [ ] 2.1 Update `team_stats()` to call `calc_period_draw_rate()` for current period
- [ ] 2.2 Add `p_draw` key to team_dict
- [ ] 2.3 Ensure `p_draw` column appears next to `c_prob` in output DataFrame

## 3. Display Updates
- [ ] 3.1 Update `soccer1.py` `country_df_properties()` to include `p_draw` in columns_to_show
- [ ] 3.2 Format `p_draw` as percentage or decimal (consistent with `c_prob`)
- [ ] 3.3 Handle N/A display for teams with no current period matches

## 4. Testing
- [ ] 4.1 Verify calculation with known data (e.g., team with 3 draws in 10 matches = 0.30)
- [ ] 4.2 Verify N/A handling at period start
- [ ] 4.3 Run `soccer1.py` and verify column appears in output

## 5. Validation
- [ ] 5.1 Linting passes (`uv run ruff check .`)
- [ ] 5.2 Handout generation works end-to-end
