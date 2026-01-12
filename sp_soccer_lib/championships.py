import pandas as pd

import config as cfg
from sp_soccer_lib import period_stats

# Date formats for football-data.co.uk CSV files
DATE_FORMAT_YYYY = "%d/%m/%Y"  # Used for 1819 onwards
DATE_FORMAT_YY = "%d/%m/%y"  # Used for 1718 (non-England)


def corrected(df):
    """### Correct possible team misnomers and sort dataframe"""
    df.replace("Olympiacos Piraeus", "Olympiakos", inplace=True)
    df.replace("Volos", "Volos NFC", inplace=True)
    df.sort_index(inplace=True)
    return df


def load_dataset(
    country: str, period: str, date_format: str = DATE_FORMAT_YYYY, fields: list = cfg.FIELDS
) -> pd.DataFrame:
    """### Load csv data from remote site.

    Parameters:

        country (str): country to load data from
        period (str): championship start-end years (eg "1920" for 2019-2020 period)
        date_format (str): strptime format string for parsing dates
            (some csv files have dd/mm/yyyy and others dd/mm/yy)
        fields (list): list of fields to include in the loaded dataset
    """
    load = pd.read_csv(
        f"https://www.football-data.co.uk/mmz4281/{period}/" + cfg.COUNTRIES[country] + ".csv",
        parse_dates=["Date"],
        index_col="Date",
        date_format=date_format,
    )
    df = load[fields].copy()
    df["period"] = period
    return df


def country_dataframe(country: str, fields: list) -> pd.DataFrame:
    """Load all periods for a country using cfg.PERIODS."""
    dfs = []
    for period in cfg.PERIODS:
        if period == "1718" and country != "England":
            dfs.append(load_dataset(country, period, DATE_FORMAT_YY, fields=fields))
        else:
            dfs.append(load_dataset(country, period, fields=fields))
    df = pd.concat(dfs)
    return corrected(df)


def load_greece(fields=cfg.FIELDS):
    return country_dataframe("Greece", fields)


def load_england(fields=cfg.FIELDS):
    return country_dataframe("England", fields)


def load_italy(fields=cfg.FIELDS):
    return country_dataframe("Italy", fields)


def load_spain(fields=cfg.FIELDS):
    return country_dataframe("Spain", fields)


def load_germany(fields=cfg.FIELDS):
    return country_dataframe("Germany", fields)


def load_france(fields=cfg.FIELDS):
    return country_dataframe("France", fields)


def load_country(country="greece", fields=cfg.FIELDS):
    # sourcery skip: raise-specific-error
    """### Load country proxy function

    Parameters:

        country (str): Country name
    """
    if country == "greece":
        return load_greece(fields)
    elif country == "italy":
        return load_italy(fields)
    elif country == "england":
        return load_england(fields)
    elif country == "spain":
        return load_spain(fields)
    elif country == "germany":
        return load_germany(fields)
    elif country == "france":
        return load_france(fields)
    else:
        raise Exception("Not Found Country!")


def calc_c_prob(row):
    from .probabilities import convert_dec_to_prob, cumulative_binomial_probabilities

    matches = cfg.NEXT_MATCHES + int(row["CurrentNoDraw"])
    mean_probability = convert_dec_to_prob(row["B365D_mean"])
    return cumulative_binomial_probabilities(matches, 1, mean_probability)[3]


def calc_c_prob_adj(row):
    """Calculate probability of at least 1 draw in next N matches.

    Uses fixed NEXT_MATCHES window (no Gambler's Fallacy adjustment)
    and current period draw rate instead of betting odds.

    Returns:
        float: P(X >= 1) where X ~ Binomial(NEXT_MATCHES, p_draw), or None if p_draw unavailable
    """
    from .probabilities import cumulative_binomial_probabilities

    p_draw = row.get("p_draw")
    if p_draw is None or pd.isna(p_draw):
        return None

    matches = cfg.NEXT_MATCHES
    return round(cumulative_binomial_probabilities(matches, 1, p_draw)[3], 4)


def calc_period_draw_rate(team_df, period):
    """Calculate draw rate for a team in a specific period.

    Parameters:
        team_df: DataFrame with team's matches
        period: Period string (e.g., "2526")

    Returns:
        float: Draw rate (draws/matches) or None if no matches in period
    """
    period_matches = team_df[team_df["period"] == period]
    total_matches = len(period_matches)

    if total_matches == 0:
        return None

    draws = len(period_matches[period_matches["result"] == "D"])
    return round(draws / total_matches, 4)


def team_stats(team_dfs, sort_by="current_period_pts", verbose=0):
    """### Cumulative team stats for all available periods

    Parameters:

        teamdfs (dict): dictionary (created by create_team_df_dict())
                    with key the team name and value a pandas dataframe with the team's
                    matches (created by create_team_df())
        sort_by (str): sorting method (currently only "current_period_pts" implemented).
                    Leaves sorting unchanged if "None"
        verbose (int): reporting level (1: prints resulting dataframe, 2: prints also team dictionary)

    Returns:

        (Pandas Dataframe): Team Stats
    """
    rows = []
    for key, _value in team_dfs.items():
        team_dict = {"Name": key}
        a = team_dfs[key]
        a.replace("", 0, inplace=True)
        team_dict.update(
            {
                "MaxNoDraw": int(a["count_no_draw"].max()),
                "CurrentNoDraw": int(a.iloc[-1, :]["count_no_draw"]),
                "B365D_mean": a["B365D"].mean(),
                "p_draw": calc_period_draw_rate(a, cfg.CURRENT_PERIOD),
            }
        )
        for period in cfg.PERIODS:
            wins, draws, losses, points, gf, ga = period_stats(a, key, period)
            team_dict.update(
                {
                    period + "_wins": int(wins),
                    period + "_draws": int(draws),
                    period + "_losses": int(losses),
                    period + "_points": int(points),
                    period + "_gf": int(gf),
                    period + "_ga": int(ga),
                }
            )
        rows.append(team_dict)
        if verbose > 1:
            print(team_dict)

    # Build DataFrame once from all rows (avoids repeated concat)
    df = pd.DataFrame(rows)

    # Vectorized probability calculations
    df["c_prob"] = df.apply(calc_c_prob, axis=1)
    df["c_prob_adj"] = df.apply(calc_c_prob_adj, axis=1)

    df.set_index("Name", inplace=True)
    if sort_by == "current_period_pts":
        df.sort_values(
            by=[
                cfg.CURRENT_PERIOD + "_points",
                cfg.CURRENT_PERIOD + "_gf",
                cfg.CURRENT_PERIOD + "_ga",
            ],
            inplace=True,
            ascending=[False, False, True],
        )
    if verbose > 0:
        print(df)
    return df
