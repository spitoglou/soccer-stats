# import pandas as pd
# import numpy as np
from sp_soccer_lib.championships import load_greece, load_england, load_italy, team_stats
from sp_soccer_lib import period_stats, create_team_df_dict


df = load_greece()

team_dfs = create_team_df_dict(df)
print(team_dfs['Atromitos'])
print(team_dfs['Olympiakos'])


print(period_stats(team_dfs['Panionios'], '1819'))

england = load_england()
print(england)
eng_team_dfs = create_team_df_dict(england)
print(eng_team_dfs['Arsenal'])
print(eng_team_dfs['Wolves'])

italy = load_italy()
print(italy)
it_team_dfs = create_team_df_dict(italy)
print(it_team_dfs['Juventus'])
print(it_team_dfs['Napoli'])
team_stats(it_team_dfs).to_html('test.html')
