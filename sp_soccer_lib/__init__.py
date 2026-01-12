import numpy as np
from loguru import logger

from config import CURRENT_PERIOD


def create_team_df(df, team):
    team_df = df.query('HomeTeam=="' + team + '" or AwayTeam=="' + team + '"')
    team_df = team_df.sort_index()
    return team_df


def championship_teams(df):
    return np.unique(
        np.concatenate(
            (
                df[df.period == CURRENT_PERIOD].HomeTeam.unique(),
                df[df.period == CURRENT_PERIOD].AwayTeam.unique(),
            )
        )
    )


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
    # Vectorized result calculation using np.select
    is_home = team_df["HomeTeam"] == team
    is_away = team_df["AwayTeam"] == team
    ftr = team_df["FTR"]

    conditions = [
        (is_home & (ftr == "H")),  # Home team wins at home
        (is_home & (ftr == "A")),  # Home team loses at home
        (is_away & (ftr == "H")),  # Away team loses (home wins)
        (is_away & (ftr == "A")),  # Away team wins
    ]
    choices = ["W", "L", "L", "W"]

    team_df["result"] = np.select(conditions, choices, default="D")
    return team_df


def update_draw_streaks(team_df, verbose=0):
    # Use itertuples() for ~10x speedup over iterrows()
    draw = []
    no_draw = []

    count = 1
    memory = "G"
    period_memory = "start"
    for row in team_df.itertuples():
        if row.FTR == "D":
            no_draw.append(0)
            if memory == "D" and row.period == period_memory:
                count += 1
                draw.append(count)
            else:
                draw.append(1)
                memory = "D"
                count = 1
        else:
            draw.append(0)
            if memory != "D" and row.period == period_memory:
                count += 1
                no_draw.append(count)
            else:
                no_draw.append(1)
                memory = "ND"
                count = 1
        period_memory = row.period
    team_df["count_draw"] = draw
    team_df["count_no_draw"] = no_draw
    return team_df


def period_stats(team_df, team_name, period="1920"):
    # Filter once for the period, then use value_counts() for W/D/L
    period_df = team_df[team_df["period"] == period]
    result_counts = period_df["result"].value_counts()
    wins = result_counts.get("W", 0)
    draws = result_counts.get("D", 0)
    losses = result_counts.get("L", 0)
    points = wins * 3 + draws * 1
    # TODO: make this more dynamic
    if team_name == "Aris" and period == "2122":
        points = points - 6
        logger.info("Made Aris 2122 Adjustment")

    # Vectorized GF/GA calculation using np.where
    is_home = team_df["HomeTeam"] == team_name
    team_df["GF"] = np.where(is_home, team_df["FTHG"], team_df["FTAG"])
    team_df["GA"] = np.where(is_home, team_df["FTAG"], team_df["FTHG"])

    gf = (
        period_df["GF"].sum()
        if "GF" in period_df.columns
        else team_df.loc[period_df.index, "GF"].sum()
    )
    ga = (
        period_df["GA"].sum()
        if "GA" in period_df.columns
        else team_df.loc[period_df.index, "GA"].sum()
    )
    return (wins, draws, losses, points, gf, ga)


def no_draw_frequencies(country, specific_teams=None, team_dfs=None):
    """Calculate no-draw frequency distribution.

    Args:
        country: Country name
        specific_teams: Optional list of teams to process
        team_dfs: Optional pre-computed team DataFrames (avoids redundant loading)
    """
    from .championships import load_country

    if team_dfs is None:
        df = load_country(country)
        team_dfs = create_team_df_dict(df)
        teams = specific_teams or championship_teams(df)
    else:
        teams = specific_teams or list(team_dfs.keys())

    no_draw_distribution = []
    for team in teams:
        if team not in team_dfs:
            continue
        placeholder = "start"
        # Use itertuples() for ~10x speedup over iterrows()
        for row in team_dfs[team].itertuples():
            if placeholder == "start":
                pass
            elif row.result == "D":
                no_draw_distribution.append(placeholder)
            placeholder = row.count_no_draw
    return no_draw_distribution
