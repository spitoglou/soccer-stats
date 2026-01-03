import math

import numpy as np
import pandas as pd

from sp_soccer_lib import create_team_df_dict
from sp_soccer_lib.championships import load_country, team_stats


def cash_flow_meta(cash_flow: list):
    cumulative = np.cumsum(cash_flow)
    print(cumulative)
    min_cum = np.min(cumulative)
    max_cum = np.max(cumulative)
    print(min_cum, max_cum)
    return [min_cum, max_cum]


def stats_dataframe(country):
    df = load_country(country)
    team_df = create_team_df_dict(df)
    return team_stats(team_df), team_df


class Team_Simulation:
    def __init__(
        self,
        team: str,
        country_team_df,
        period: str,
        bet_progr: list,
        threshold: int,
        bet_span: int,
        fixed_odds: int = 3,
        verbose: bool = False,
        abandon_on_first_bucket=False,
        restart_after_bucket=True,
    ):
        self.team = team
        self.country_team_df = country_team_df
        self.period = period
        self.bet_progr = bet_progr
        self.threshold = threshold
        self.bet_span = bet_span
        self.fixed_odds = fixed_odds
        self.verbose = verbose
        self.abandon_on_first_bucket = abandon_on_first_bucket
        self.restart_after_bucket = restart_after_bucket

    def get_matches_df(self):
        team_matches_df = self.country_team_df[self.team]
        team_matches_df = team_matches_df[team_matches_df["period"] == self.period]
        if self.verbose:
            print(team_matches_df.head())
            print(f"Matches in this period: {team_matches_df.shape[0]}")
            self.period_matches = team_matches_df.shape[0]
        return team_matches_df

    def get_odds(self):
        return (
            self.fixed_odds
            if math.isnan(self.current_match["B365D"])
            else self.current_match["B365D"]
        )

    def print_match_details(self):
        print("--------------------------------")
        print(
            f"[{self.match_index}][{self.match_date}] Match is {self.current_match['HomeTeam']}-{self.current_match['AwayTeam']}. Draw gives {self.get_odds()}. Result for {self.team} is {self.current_match['result']}"
        )
        print("--------------------------------")

    def print_bet(self):
        if self.next_bet:
            print(f"!!! This is bet No {self.next_bet}. Betting {self.calculate_bet()} Eur.  !!!")
        else:
            print("!!! No bet this time !!!")

    def calculate_bet(self):
        return self.bet_progr[(self.next_bet - 1) % self.bet_span]

    def run(self):
        team_matches_df = self.get_matches_df()

        self.team_bet = 0
        self.team_wins = 0
        self.cash_flow = []

        self.next_bet = 0
        over_threshold = False
        index = 0
        for match_date_index, match in team_matches_df.iterrows():
            index = index + 1
            self.match_date = match_date_index
            self.match_index = index
            self.current_match = match
            if self.abandon_on_first_bucket and over_threshold:
                print("Discarding Team Because Abandon Option is Enabled")
                break

            if self.verbose:
                self.print_match_details()

            odds = self.get_odds()

            if self.next_bet:
                bet = self.calculate_bet()
                self.team_bet = self.team_bet + bet
                self.cash_flow.append(-1 * bet)

            if self.verbose:
                self.print_bet()

            if match["FTR"] == "D":
                if self.next_bet:
                    winnings = bet * odds
                    if verbose:
                        print(f"Colourful Ballons!!! We retrieve {winnings}")
                    self.team_wins = self.team_wins + winnings
                    self.cash_flow.append(winnings)
                self.next_bet = 0
            else:
                if match["count_no_draw"] >= self.threshold + self.bet_span:
                    over_threshold = True
                else:
                    over_threshold = False
                match_in_main_betting_span = (
                    match["count_no_draw"] >= self.threshold
                    and match["count_no_draw"] < self.threshold + self.bet_span
                )
                if match_in_main_betting_span or (self.restart_after_bucket and over_threshold):
                    self.next_bet = match["count_no_draw"] - self.threshold + 1
                    # if self.next_bet < 0:
                    #     self.next_bet = 0

                else:
                    self.next_bet = 0

            print(f"Variable next_bet: {self.next_bet}")
            # abandon = True

            # print('!!!!!BET!!!!!!')
            # if row['count_no_draw'] == threshold:
            #     next_bet = 1

        # print(f'{team} bet for {period}: {team_bet}')
        # print(f'{team} wins for {period}: {team_wins}')
        # return team_bet, team_wins, cash_flow


if __name__ == "__main__":
    countries = ["germany", "greece", "italy"]
    periods = ["1920", "2021", "2122", "2223"]
    threshold_options = [3, 4, 5, 6]
    bet_span_options = [3, 4, 5, 6, 7, 8, 9, 10]

    bet_progr = [2, 4, 6, 9, 13, 20, 30, 45, 68, 103]

    test = False

    if test:
        countries = ["greece"]
        periods = ["2021"]
        threshold_options = [3]
        bet_span_options = [4]

    # abandon = False
    verbose = True

    total_bet = 0
    total_wins = 0
    team_result = []
    period_result = []
    for country in countries:
        stats_df, team_df = stats_dataframe(country)
        for threshold in threshold_options:
            for bet_span in bet_span_options:
                for period in periods:
                    for mode in ["normal", "restart", "abandon"]:
                        for _, team_row in stats_df.iterrows():
                            print(team_row.name)
                            team = team_row.name

                            if mode == "abandon":
                                abandon = True
                                restart = False
                            elif mode == "restart":
                                abandon = False
                                restart = True
                            else:
                                abandon = False
                                restart = False

                            simulation = Team_Simulation(
                                str(team),
                                team_df,
                                period,
                                bet_progr,
                                threshold,
                                bet_span,
                                verbose=verbose,
                                abandon_on_first_bucket=abandon,
                                restart_after_bucket=restart,
                            )
                            simulation.run()

                            team_bet = simulation.team_bet
                            team_wins = simulation.team_wins
                            cash_flow = simulation.cash_flow
                            try:
                                meta_cash_flow = cash_flow_meta(cash_flow)
                            except Exception as e:
                                print(e)
                                meta_cash_flow = []
                            print(f"Team bet: {team_bet}")
                            print(f"Team wins: {team_wins}")
                            print(f"Cash Flow: {cash_flow}")
                            total_bet = total_bet + team_bet
                            total_wins = total_wins + team_wins

                            # TODO: Here we need to calculate min and max cumulative cash flow

                            team_result.append(
                                {
                                    "country": country,
                                    "period": period,
                                    "mode": mode,
                                    "bet_progression": bet_progr,
                                    "threshold": threshold,
                                    "span": bet_span,
                                    "team": team,
                                    "bet": team_bet,
                                    "wins": team_wins,
                                    "cash_flow_meta": meta_cash_flow,
                                    "cash_flow": cash_flow,
                                }
                            )

                        print(f"Total bet: {total_bet}")
                        print(f"Total wins: {total_wins}")
                        # print(f'Cash Flow: {cash_flow}')
                        period_result.append(
                            {
                                "country": country,
                                "period": period,
                                "mode": mode,
                                "bet_progression": bet_progr,
                                "threshold": threshold,
                                "span": bet_span,
                                "total_bet": total_bet,
                                "total_wins": total_wins,
                            }
                        )
                        total_bet = 0
                        total_wins = 0
    print(team_result)
    print(period_result)
    pd.DataFrame.from_dict(team_result).to_excel("team.xlsx")
    pd.DataFrame.from_dict(period_result).to_excel("period.xlsx")
