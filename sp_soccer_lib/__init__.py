
import numpy as np
from loguru import logger
from config import CURRENT_PERIOD


def create_team_df(df, team):
    team_df = df.query('HomeTeam=="' + team + '" or AwayTeam=="' + team + '"')
    team_df = team_df.sort_index()
    return team_df


def championship_teams(df):
    return np.unique(np.concatenate((df[df.period == CURRENT_PERIOD].HomeTeam.unique(), df[df.period == CURRENT_PERIOD].AwayTeam.unique())))


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
    results = []

    for index, row in team_df.iterrows():
        if row['HomeTeam'] == team and row['FTR'] == 'H':
            results.append('W')
        elif row['HomeTeam'] == team and row['FTR'] == 'A':
            results.append('L')
        elif row['AwayTeam'] == team and row['FTR'] == 'H':
            results.append('L')
        elif row['AwayTeam'] == team and row['FTR'] == 'A':
            results.append('W')
        else:
            results.append('D')
    team_df['result'] = results
    return team_df


def update_draw_streaks(team_df, verbose=0):
    draw = []
    no_draw = []

    count = 1
    memory = 'G'
    period_memory = 'start'
    for index, row in team_df.iterrows():
        if row['FTR'] == 'D':
            no_draw.append(0)
            if memory == 'D' and row['period'] == period_memory:
                count += 1
                draw.append(count)
            else:
                draw.append(1)
                memory = 'D'
                count = 1
        else:
            draw.append(0)
            if memory != 'D' and row['period'] == period_memory:
                count += 1
                no_draw.append(count)
            else:
                no_draw.append(1)
                memory = 'ND'
                count = 1
        period_memory = row['period']
    team_df['count_draw'] = draw
    team_df['count_no_draw'] = no_draw
    return team_df


def calc_gf(row):
    return row['FTHG'] if row['name'] == row['HomeTeam'] else row['FTAG']


def calc_ga(row):
    return row['FTAG'] if row['name'] == row['HomeTeam'] else row['FTHG']


def period_stats(team_df, team_name, period='1920'):
    wins = team_df.query(
        'result == "W" and period == "' + period + '"').shape[0]
    draws = team_df.query(
        'result == "D" and period == "' + period + '"').shape[0]
    losses = team_df.query(
        'result == "L" and period == "' + period + '"').shape[0]
    points = wins * 3 + draws * 1
    # TODO: make this more dynamic
    if team_name == 'Aris' and period == '2122':
        points = points - 6
        logger.info('Made Aris 2122 Adjustment')
    team_df['name'] = team_name
    team_df['GF'] = team_df.apply(lambda row: calc_gf(row), axis=1)
    team_df['GA'] = team_df.apply(lambda row: calc_ga(row), axis=1)
    gf = team_df.query(
        'period == "' + period + '"')['GF'].sum()
    ga = team_df.query(
        'period == "' + period + '"')['GA'].sum()
    return (wins, draws, losses, points, gf, ga)


def no_draw_frequencies(country, specific_teams=None):
    from .championships import load_country
    df = load_country(country)
    team_dfs = create_team_df_dict(df)
    no_draw_distribution = []
    teams = specific_teams or championship_teams(df)
    for team in teams:
        # pp.pprint(team_dfs[team])
        placeholder = 'start'
        for (index_label, row) in team_dfs[team].iterrows():
            if placeholder == 'start':
                pass
            elif row['result'] == 'D':
                no_draw_distribution.append(placeholder)
            placeholder = row['count_no_draw']
    # pp.pprint(no_draw_distribution)
    return no_draw_distribution
