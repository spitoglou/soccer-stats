# import pandas as pd
# import numpy as np
from lib.championships import load_greece
from lib import update_draw_streaks, create_team_df, championship_teams, update_results


df = load_greece()

team_dfs = {}
for team in championship_teams(df):
    team_df = create_team_df(df, team)
    streaks = update_draw_streaks(team_df, verbose=0)
    results = update_results(streaks, team)
    # results['team'] = team
    team_dfs[team] = results
print(team_dfs['Atromitos'])


def period_stats(team_df, period='1920'):
    wins = team_df.query(
        'result == "W" and period == "' + period + '"').shape[0]
    draws = team_df.query(
        'result == "D" and period == "' + period + '"').shape[0]
    losses = team_df.query(
        'result == "L" and period == "' + period + '"').shape[0]
    points = wins * 3 + draws * 1
    return (wins, draws, losses, points)


print(period_stats(team_dfs['Panionios'], '1819'))
