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
FIELDS = ['HomeTeam', 'AwayTeam', 'FTR', 'FTHG', 'FTAG', 'B365D']
CURRENT_PERIOD = '1920'

NEXT_MATCHES = 7


def corrected(df):
    ''' ### Correct possible team misnomers and sort dataframe '''
    df.replace('Olympiacos Piraeus', 'Olympiakos', inplace=True)
    df.sort_index(inplace=True)
    return df


def load_dataset(country, period, dateparser=dateparser1819, fields=FIELDS):
    ''' ### Load csv data from remote site.

        Parameters:

            country (str): country to load data from
            period (str): championship start-end years (eg "1920" fror 2019-2020 period)
            dateparser (function): choose the way to parse the dates
                (some csv files have dd/dd/yyyy and others dd/mm/yy)
    '''
    load = pd.read_csv('https://www.football-data.co.uk/mmz4281/' + period + '/' + COUNTRIES[country] + '.csv',
                       parse_dates=['Date'], index_col='Date', date_parser=dateparser)
    df = load[fields].copy()
    df['period'] = period
    return df


def load_greece(fields=FIELDS):
    df = load_dataset('Greece', '1819', fields=fields)
    df = df.append(load_dataset('Greece', '1718',
                                dateparser1718, fields=fields))
    df = df.append(load_dataset('Greece', '1920', fields=fields))
    return corrected(df)


def load_england(fields=FIELDS):
    df = load_dataset('England', '1819', fields=fields)
    df = df.append(load_dataset('England', '1718', fields=fields))
    df = df.append(load_dataset('England', '1920', fields=fields))
    return corrected(df)


def load_italy(fields=FIELDS):
    df = load_dataset('Italy', '1819', fields=fields)
    df = df.append(load_dataset('Italy', '1718',
                                dateparser1718, fields=fields))
    df = df.append(load_dataset('Italy', '1920', fields=fields))
    return corrected(df)


def load_spain(fields=FIELDS):
    df = load_dataset('Spain', '1819', fields=fields)
    df = df.append(load_dataset('Spain', '1718',
                                dateparser1718, fields=fields))
    df = df.append(load_dataset('Spain', '1920', fields=fields))
    return corrected(df)


def load_germany(fields=FIELDS):
    df = load_dataset('Germany', '1819', fields=fields)
    df = df.append(load_dataset('Germany', '1718',
                                dateparser1718, fields=fields))
    df = df.append(load_dataset('Germany', '1920', fields=fields))
    return corrected(df)


def load_france(fields=FIELDS):
    df = load_dataset('France', '1819', fields=fields)
    df = df.append(load_dataset('France', '1718',
                                dateparser1718, fields=fields))
    df = df.append(load_dataset('France', '1920', fields=fields))
    return corrected(df)


def load_country(country='greece', fields=FIELDS):
    ''' ### Load country proxy function

        Parameters:

            country (str): Country name
    '''
    if country == 'greece':
        return load_greece(fields)
    elif country == 'italy':
        return load_italy(fields)
    elif country == 'england':
        return load_england(fields)
    elif country == 'spain':
        return load_spain(fields)
    elif country == 'germany':
        return load_germany(fields)
    elif country == 'france':
        return load_france(fields)
    else:
        raise Exception('Not Found Country!')


def calc_c_prob(row):
    from .probabilities import cumulative_binomial_probabilities, convert_dec_to_prob
    matches = NEXT_MATCHES + int(row['CurrentNoDraw'])
    mean_probability = convert_dec_to_prob(row['B365D_mean'])
    return cumulative_binomial_probabilities(matches, 1, mean_probability)[3]


def team_stats(team_dfs, sort_by='current_period_pts', verbose=0):
    ''' ### Cumulative team stats for all available periods

        Parameters:

            teamdfs (dict): dictionary (created by create_team_df_dict())
                        with key the team name and value a pandas dataframe with the team's
                        matches (created by create_team_df())
            sort_by (str): sorting method (currently only "current_period_pts" implemented).
                        Leaves sorting unchanged if "None"
            verbose (int): reporting level (1: prints resulting dataframe, 2: prints also team dictionary)

        Returns:

            (Pandas Dataframe): Team Stats
    '''
    df = pd.DataFrame()
    for key, value in team_dfs.items():
        team_dict = {}
        team_dict['Name'] = key
        a = team_dfs[key]
        a.replace('', 0, inplace=True)
        team_dict.update({
            'MaxNoDraw': a['count_no_draw'].max(),
            'CurrentNoDraw': a.iloc[-1, :]['count_no_draw'],
            'B365D_mean': a['B365D'].mean()
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
        df['c_prob'] = df.apply(lambda row: calc_c_prob(row), axis=1)
        if verbose > 1:
            print(team_dict)
    df.set_index('Name', inplace=True)
    if sort_by == 'current_period_pts':
        df.sort_values(by=[CURRENT_PERIOD + '_points'],
                       inplace=True, ascending=False)
    if verbose > 0:
        print(df)
    return df
