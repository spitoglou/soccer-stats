import pandas as pd
from lib.date_parsers import dateparser1819, dateparser1718


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

    df.replace('Olympiacos Piraeus', 'Olympiakos', inplace=True)

    df.sort_index(inplace=True)
    return df
