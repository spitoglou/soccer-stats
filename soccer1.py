# import pandas as pd
# import numpy as np
from lib.championships import load_greece
from lib import period_stats, create_team_df_dict


df = load_greece()

team_dfs = create_team_df_dict(df)
print(team_dfs['Atromitos'])
print(team_dfs['Olympiakos'])


print(period_stats(team_dfs['Panionios'], '1819'))
