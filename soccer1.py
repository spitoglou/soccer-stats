import pandas as pd
# import numpy as np
from lib.championships import load_greece
from lib import period_stats, create_team_df_dict


df = load_greece()

team_dfs = create_team_df_dict(df)
print(team_dfs['Atromitos'])
print(team_dfs['Olympiakos'])


print(period_stats(team_dfs['Panionios'], '1819'))

a = team_dfs['Atromitos']
a.replace('', 0, inplace=True)
print(a['count_no_draw'].max(), a.iloc[-1, :]['count_no_draw'])

new = pd.DataFrame()
new = new.append({
    'Name': 'Atromitos',
    'MaxNoDraw': a['count_no_draw'].max(),
    'CurrentNoDraw': a.iloc[-1, :]['count_no_draw']
}, ignore_index=True)
print(new)
