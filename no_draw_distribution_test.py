import pprint as pp

import matplotlib.pyplot as plt
import pandas as pd

from sp_soccer_lib import championship_teams, create_team_df_dict, no_draw_frequencies
from sp_soccer_lib.championships import load_country

df = load_country("greece")
team_dfs = create_team_df_dict(df)
# stats = team_stats(team_dfs)

no_draw_distribution = []
for team in championship_teams(df):
    # for team in ['Olympiakos']:
    pp.pprint(team_dfs[team])
    placeholder = "start"
    for index_label, row_series in team_dfs[team].iterrows():
        print(index_label, row_series["count_no_draw"])
        if placeholder != "start" and row_series["count_no_draw"] == "":
            if placeholder == "":
                no_draw_distribution.append(0)
                print("Added 0")
            else:
                no_draw_distribution.append(placeholder)
                print("Added ", placeholder)
            placeholder = ""
        else:
            placeholder = row_series["count_no_draw"]
print(no_draw_distribution)
print(len(no_draw_distribution))
print(no_draw_frequencies("greece"))
print(no_draw_frequencies("greece", ["Olympiakos"]))


series = pd.Series(no_draw_distribution)
counts = series.value_counts()
pp.pprint(dict(counts))
plt.hist(no_draw_distribution, bins=30)
plt.show()

print(no_draw_frequencies("greece"))
