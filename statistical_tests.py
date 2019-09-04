from sp_soccer_lib.championships import load_england, load_italy, team_stats, load_country
from sp_soccer_lib.handout_helpers import style, get_country_header, make_link
from sp_soccer_lib import create_team_df_dict, championship_teams, no_draw_frequencies, create_team_df, update_draw_streaks, update_results
from sp_soccer_lib.probabilities import cumulative_binomial_probabilities

import pprint as pp
import pandas as pd

next_matches = 7


def calc_c_prob(row):
    return cumulative_binomial_probabilities(next_matches + int(row['CurrentNoDraw']), 1, 0.1)[3]


df = load_country('greece')  # , 'FTHG'

team_dfs = create_team_df_dict(df)
stats = team_stats(team_dfs)
# stats['Name'] = stats.index

stats['c_prob'] = stats.apply(lambda row: calc_c_prob(row), axis=1)


print(stats)
print(stats.columns)
