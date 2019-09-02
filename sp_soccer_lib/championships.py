import pandas as pd
from sp_soccer_lib.date_parsers import dateparser1819, dateparser1718
from sp_soccer_lib import period_stats

PERIODS = ['1718', '1819', '1920']
COUNTRIES = {
    'Greece': 'G1',
    'England': 'E0',
    'Italy': 'I1',
    'Spain': 'SP1',
    'Germany': 'D1',
    'France': 'F1'
}
FIELDS = ['HomeTeam', 'AwayTeam', 'FTR']
CURRENT_PERIOD = '1920'


def corrected(df):
    df.replace('Olympiacos Piraeus', 'Olympiakos', inplace=True)
    df.sort_index(inplace=True)
    return df


def load_dataset(country, period, dateparser=dateparser1819):
    load = pd.read_csv('https://www.football-data.co.uk/mmz4281/' + period + '/' + COUNTRIES[country] + '.csv',
                       parse_dates=['Date'], index_col='Date', date_parser=dateparser)
    df = load[FIELDS].copy()
    df['period'] = period
    return df


def load_greece():
    df = load_dataset('Greece', '1819')
    df = df.append(load_dataset('Greece', '1718', dateparser1718))
    df = df.append(load_dataset('Greece', '1920'))
    return corrected(df)


def load_england():
    df = load_dataset('England', '1819')
    df = df.append(load_dataset('England', '1718'))
    df = df.append(load_dataset('England', '1920'))
    return corrected(df)


def load_italy():
    df = load_dataset('Italy', '1819')
    df = df.append(load_dataset('Italy', '1718', dateparser1718))
    df = df.append(load_dataset('Italy', '1920'))
    return corrected(df)


def load_spain():
    df = load_dataset('Spain', '1819')
    df = df.append(load_dataset('Spain', '1718', dateparser1718))
    df = df.append(load_dataset('Spain', '1920'))
    return corrected(df)


def load_germany():
    df = load_dataset('Germany', '1819')
    df = df.append(load_dataset('Germany', '1718', dateparser1718))
    df = df.append(load_dataset('Germany', '1920'))
    return corrected(df)


def load_france():
    df = load_dataset('France', '1819')
    df = df.append(load_dataset('France', '1718', dateparser1718))
    df = df.append(load_dataset('France', '1920'))
    return corrected(df)


def load_country(country='greece'):
    if country == 'greece':
        return load_greece()
    elif country == 'italy':
        return load_italy()
    elif country == 'england':
        return load_england()
    elif country == 'spain':
        return load_spain()
    elif country == 'germany':
        return load_germany()
    elif country == 'france':
        return load_france()
    else:
        raise Exception('Not Found Country!')


def team_stats(team_dfs, sort_by='current_period_pts', verbose=0):
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
    if sort_by == 'current_period_pts':
        df.sort_values(by=[CURRENT_PERIOD + '_points'], inplace=True, ascending=False)
    if verbose > 0:
        print(df)
    return df
