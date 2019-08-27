import pandas as pd
from lib.date_parsers import dateparser1819, dateparser1718
from lib import period_stats

PERIODS = ['1718', '1819', '1920']


def corrections(df):
    df.replace('Olympiacos Piraeus', 'Olympiakos', inplace=True)
    return df


def load_greece():
    load = pd.read_csv('https://www.football-data.co.uk/mmz4281/1819/G1.csv',
                       parse_dates=['Date'], index_col='Date', date_parser=dateparser1819)
    df = load[['HomeTeam', 'AwayTeam', 'FTR']].copy()
    df['period'] = '1819'
    load2 = pd.read_csv('https://www.football-data.co.uk/mmz4281/1718/G1.csv',
                        parse_dates=['Date'], index_col='Date', date_parser=dateparser1718)
    df2 = load2[['HomeTeam', 'AwayTeam', 'FTR']].copy()
    df2['period'] = '1718'
    df = df.append(df2)
    load3 = pd.read_csv('https://www.football-data.co.uk/mmz4281/1920/G1.csv',
                        parse_dates=['Date'], index_col='Date', date_parser=dateparser1819)
    df3 = load3[['HomeTeam', 'AwayTeam', 'FTR']].copy()
    df3['period'] = '1920'
    df = df.append(df3)

    df = corrections(df)
    df.sort_index(inplace=True)
    return df


def team_stats(team_dfs, verbose=0):
    df = pd.DataFrame()
    for key, value in team_dfs.items():
        team_dict = {}
        team_dict['Name'] = key
        a = team_dfs[key]
        a.replace('', 0, inplace=True)
        team_dict.update({
            'MaxNoDraw': a['count_no_draw'].max(),
            'CurrentNoDraw': a.iloc[-1, :]['count_no_draw']
        })
        for period in PERIODS:
            wins, draws, losses, points = period_stats(a, period)
            team_dict.update({
                period + '_wins': wins,
                period + '_draws': draws,
                period + '_losses': losses,
                period + '_points': points
            })
        df = df.append(team_dict, ignore_index=True)
        if verbose > 1:
            print(team_dict)
    df.set_index('Name', inplace=True)
    if verbose > 0:
        print(df)
    return df
