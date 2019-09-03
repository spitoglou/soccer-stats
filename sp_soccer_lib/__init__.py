
import numpy as np


def create_team_df(df, team):
    team_df = df.query('HomeTeam=="' + team + '" or AwayTeam=="' + team + '"')
    team_df = team_df.sort_index()
    return team_df


def championship_teams(df):
    return np.unique(np.concatenate((df.HomeTeam.unique(), df.AwayTeam.unique())))


def create_team_df_dict(dataframe):
    team_dfs = {}
    for team in championship_teams(dataframe):
        team_df = create_team_df(dataframe, team)
        streaks = update_draw_streaks(team_df, verbose=0)
        results = update_results(streaks, team)
        # results['team'] = team
        team_dfs[team] = results
    return team_dfs


def update_results(team_df, team):
    team_df['result'] = ''
    for index, row in team_df.iterrows():
        if row['HomeTeam'] == team and row['FTR'] == 'H':
            row['result'] = 'W'
        elif row['HomeTeam'] == team and row['FTR'] == 'A':
            row['result'] = 'L'
        elif row['AwayTeam'] == team and row['FTR'] == 'H':
            row['result'] = 'L'
        elif row['AwayTeam'] == team and row['FTR'] == 'A':
            row['result'] = 'W'
        else:
            row['result'] = 'D'
    return team_df


def update_draw_streaks(team_df, verbose=0):
    team_df['count_draw'] = ''
    team_df['count_no_draw'] = ''

    count_draw = 1
    count_no_draw = 1
    memory = 'G'
    for index, row in team_df.iterrows():
        if row['FTR'] == 'D':
            row['count_draw'] = 1
            memory = 'D'
        else:
            row['count_no_draw'] = 1
            memory = 'ND'
        if row['FTR'] == memory and row['FTR'] == 'D':
            row['count_draw'] = count_draw
            count_draw = count_draw + 1
            count_no_draw = 1
        elif memory == 'ND' and row['FTR'] != 'D':
            row['count_no_draw'] = count_no_draw
            count_draw = 1
            count_no_draw = count_no_draw + 1
        else:
            count_draw = 1
            count_no_draw = 1
            # row['count'] = ''
            # memory = row['FTR']
        if verbose > 1:
            print(count_draw, count_no_draw, row['FTR'], memory)
    return team_df


def period_stats(team_df, period='1920'):
    wins = team_df.query(
        'result == "W" and period == "' + period + '"').shape[0]
    draws = team_df.query(
        'result == "D" and period == "' + period + '"').shape[0]
    losses = team_df.query(
        'result == "L" and period == "' + period + '"').shape[0]
    points = wins * 3 + draws * 1
    return (wins, draws, losses, points)


def no_draw_frequencies(country, specific_teams=None):
    from .championships import load_country
    df = load_country(country)
    team_dfs = create_team_df_dict(df)
    no_draw_distribution = []
    if specific_teams:
        teams = specific_teams
    else:
        teams = championship_teams(df)
    for team in teams:
        # pp.pprint(team_dfs[team])
        placeholder = 'start'
        for (index_label, row_series) in team_dfs[team].iterrows():
            # print(index_label, row_series['count_no_draw'])
            if placeholder != 'start' and row_series['count_no_draw'] == '':
                if placeholder == '':
                    no_draw_distribution.append(0)
                    # print('Added 0')
                else:
                    no_draw_distribution.append(placeholder)
                    # print('Added ', placeholder)
                placeholder = ''
            else:
                placeholder = row_series['count_no_draw']
    # pp.pprint(no_draw_distribution)
    return no_draw_distribution
