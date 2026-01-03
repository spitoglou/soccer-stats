"""
c_prob_adj Based Betting Simulation

This simulation tests a betting strategy based on the adjusted cumulative probability
(c_prob_adj) which uses a fixed window and actual draw rates instead of the
Gambler's Fallacy approach.

Strategy:
1. Calculate rolling p_draw (draw rate) for each team at each match
2. Compute c_prob_adj = P(at least 1 draw in next N matches) using binomial distribution
3. When c_prob_adj exceeds threshold, start betting for N matches with progression
4. Track profit/loss across all teams and periods

Note: This strategy is still mathematically flawed because c_prob_adj doesn't
"build up" - it's just a property of the team's draw rate. However, this
simulation empirically validates that insight.
"""

import math
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from loguru import logger

from sp_soccer_lib import create_team_df_dict
from sp_soccer_lib.championships import load_country
from sp_soccer_lib.probabilities import cumulative_binomial_probabilities


@dataclass
class SimulationConfig:
    """Configuration for the betting simulation."""

    bet_window: int = 5  # Number of matches to bet on once triggered
    threshold: float = 0.80  # c_prob_adj threshold to trigger betting
    bet_progression: list = field(default_factory=lambda: [2, 4, 6, 9, 13])
    min_matches_for_pdraw: int = 3  # Minimum matches before calculating p_draw
    fixed_odds: float = 3.5  # Fallback odds if B365D is missing


@dataclass
class BettingState:
    """Tracks the current betting state for a team."""

    is_betting: bool = False
    bets_remaining: int = 0
    current_bet_index: int = 0


@dataclass
class SimulationResult:
    """Results from a single team-period simulation."""

    country: str
    team: str
    period: str
    total_bet: float = 0.0
    total_won: float = 0.0
    bet_count: int = 0
    win_count: int = 0
    triggers: int = 0  # Number of times threshold was crossed
    cash_flow: list = field(default_factory=list)

    @property
    def profit(self) -> float:
        return self.total_won - self.total_bet

    @property
    def roi(self) -> float:
        if self.total_bet == 0:
            return 0.0
        return (self.profit / self.total_bet) * 100


def calc_rolling_pdraw(team_df: pd.DataFrame, match_index: int, period: str) -> float | None:
    """Calculate draw rate based on matches played so far in the current period.

    Args:
        team_df: DataFrame with team's matches
        match_index: Current position in the dataframe (0-indexed iloc position)
        period: Current period string

    Returns:
        Draw rate or None if insufficient matches
    """
    # Get matches up to (but not including) current match in this period
    period_matches = team_df.iloc[:match_index]
    period_matches = period_matches[period_matches["period"] == period]

    total = len(period_matches)
    if total < 3:  # Need minimum matches for meaningful rate
        return None

    draws = len(period_matches[period_matches["result"] == "D"])
    return draws / total


def calc_cprob_adj(p_draw: float | None, window: int = 5) -> float | None:
    """Calculate probability of at least 1 draw in next N matches.

    Uses fixed window (no Gambler's Fallacy adjustment).

    Args:
        p_draw: Draw probability (0.0 to 1.0)
        window: Number of matches to consider

    Returns:
        P(X >= 1) where X ~ Binomial(window, p_draw), or None if p_draw unavailable
    """
    if p_draw is None or math.isnan(p_draw):
        return None

    # P(X >= 1) = 1 - P(X = 0) = 1 - (1 - p_draw)^window
    # Using cumulative_binomial_probabilities for consistency with existing code
    result = cumulative_binomial_probabilities(window, 1, p_draw)
    return result[3]  # X >= 1


class CProbAdjSimulation:
    """Simulates betting based on c_prob_adj threshold."""

    def __init__(self, config: SimulationConfig, verbose: bool = False):
        self.config = config
        self.verbose = verbose

    def get_odds(self, match: pd.Series) -> float:
        """Get betting odds for a match, with fallback."""
        odds = match.get("B365D")
        if odds is None or math.isnan(odds):
            return self.config.fixed_odds
        return odds

    def run_team_period(
        self, team: str, team_df: pd.DataFrame, period: str, country: str
    ) -> SimulationResult:
        """Run simulation for a single team in a single period.

        Args:
            team: Team name
            team_df: DataFrame with team's matches
            period: Period to simulate (e.g., "2324")
            country: Country name (for result tracking)

        Returns:
            SimulationResult with betting outcomes
        """
        result = SimulationResult(country=country, team=team, period=period)
        state = BettingState()

        # Filter to period matches
        period_mask = team_df["period"] == period
        period_indices = team_df.index[period_mask].tolist()

        if not period_indices:
            return result

        for iloc_pos, (match_date, match) in enumerate(team_df.iterrows()):
            if match["period"] != period:
                continue

            # Calculate current p_draw and c_prob_adj
            full_iloc = team_df.index.get_loc(match_date)
            p_draw = calc_rolling_pdraw(team_df, full_iloc, period)
            c_prob_adj = calc_cprob_adj(p_draw, self.config.bet_window)

            is_draw = match["FTR"] == "D"
            odds = self.get_odds(match)

            if self.verbose:
                logger.debug(
                    f"[{match_date.date()}] {match['HomeTeam']} vs {match['AwayTeam']} | "
                    f"p_draw={p_draw:.3f if p_draw else 'N/A'} | "
                    f"c_prob_adj={c_prob_adj:.3f if c_prob_adj else 'N/A'} | "
                    f"result={match['result']}"
                )

            # Check if we should start betting
            if not state.is_betting and c_prob_adj is not None:
                if c_prob_adj >= self.config.threshold:
                    state.is_betting = True
                    state.bets_remaining = self.config.bet_window
                    state.current_bet_index = 0
                    result.triggers += 1
                    if self.verbose:
                        logger.info(
                            f"TRIGGER: {team} c_prob_adj={c_prob_adj:.3f} >= {self.config.threshold}"
                        )

            # Process bet if in betting mode
            if state.is_betting and state.bets_remaining > 0:
                bet_amount = self.config.bet_progression[state.current_bet_index]
                result.total_bet += bet_amount
                result.bet_count += 1
                result.cash_flow.append(-bet_amount)

                if self.verbose:
                    logger.info(
                        f"BET: {team} bet #{state.current_bet_index + 1} = {bet_amount} EUR @ {odds:.2f}"
                    )

                if is_draw:
                    winnings = bet_amount * odds
                    result.total_won += winnings
                    result.win_count += 1
                    result.cash_flow.append(winnings)

                    if self.verbose:
                        logger.success(f"WIN: {team} won {winnings:.2f} EUR")

                    # Reset after win
                    state.is_betting = False
                    state.bets_remaining = 0
                    state.current_bet_index = 0
                else:
                    # Move to next bet in progression
                    state.bets_remaining -= 1
                    state.current_bet_index = min(
                        state.current_bet_index + 1, len(self.config.bet_progression) - 1
                    )

                    if state.bets_remaining == 0:
                        state.is_betting = False
                        if self.verbose:
                            logger.warning(f"BUST: {team} exhausted betting window without draw")

        return result


def run_full_simulation(
    countries: list[str],
    periods: list[str],
    config: SimulationConfig,
    verbose: bool = False,
) -> pd.DataFrame:
    """Run simulation across multiple countries and periods.

    Args:
        countries: List of country names
        periods: List of period strings
        config: Simulation configuration
        verbose: Whether to print detailed logs

    Returns:
        DataFrame with all simulation results
    """
    simulation = CProbAdjSimulation(config, verbose=verbose)
    all_results = []

    for country in countries:
        logger.info(f"Loading {country}...")
        df = load_country(country)
        team_dfs = create_team_df_dict(df)

        for team, team_df in team_dfs.items():
            for period in periods:
                result = simulation.run_team_period(team, team_df, period, country)
                if result.bet_count > 0:  # Only include if bets were made
                    all_results.append(
                        {
                            "country": country,
                            "team": team,
                            "period": period,
                            "total_bet": result.total_bet,
                            "total_won": result.total_won,
                            "profit": result.profit,
                            "roi": result.roi,
                            "bet_count": result.bet_count,
                            "win_count": result.win_count,
                            "triggers": result.triggers,
                        }
                    )

    return pd.DataFrame(all_results)


def print_summary(results_df: pd.DataFrame, config: SimulationConfig):
    """Print summary statistics for the simulation."""
    print("\n" + "=" * 70)
    print("SIMULATION SUMMARY")
    print("=" * 70)
    print(f"Configuration:")
    print(f"  - Threshold: {config.threshold}")
    print(f"  - Bet Window: {config.bet_window} matches")
    print(f"  - Progression: {config.bet_progression}")
    print(f"  - Max loss per cycle: {sum(config.bet_progression[: config.bet_window])} EUR")
    print()

    if results_df.empty:
        print("No bets were triggered with this configuration.")
        return

    total_bet = results_df["total_bet"].sum()
    total_won = results_df["total_won"].sum()
    total_profit = results_df["profit"].sum()
    overall_roi = (total_profit / total_bet * 100) if total_bet > 0 else 0

    print(f"Overall Results:")
    print(f"  - Total Bet: {total_bet:.2f} EUR")
    print(f"  - Total Won: {total_won:.2f} EUR")
    print(f"  - Net Profit: {total_profit:.2f} EUR")
    print(f"  - ROI: {overall_roi:.2f}%")
    print(f"  - Total Bets: {results_df['bet_count'].sum()}")
    print(f"  - Total Wins: {results_df['win_count'].sum()}")
    print(f"  - Triggers: {results_df['triggers'].sum()}")
    print()

    print("By Country:")
    country_summary = (
        results_df.groupby("country")
        .agg({"total_bet": "sum", "total_won": "sum", "profit": "sum", "bet_count": "sum"})
        .round(2)
    )
    print(country_summary.to_string())
    print()

    print("By Period:")
    period_summary = (
        results_df.groupby("period")
        .agg({"total_bet": "sum", "total_won": "sum", "profit": "sum", "bet_count": "sum"})
        .round(2)
    )
    print(period_summary.to_string())


if __name__ == "__main__":
    # Configuration
    config = SimulationConfig(
        bet_window=5,
        threshold=0.90,  # Try different thresholds: 0.70, 0.80, 0.85, 0.90
        bet_progression=[2, 4, 6, 9, 13],
    )

    countries = ["greece", "england", "italy", "spain", "germany", "france"]
    periods = ["1920", "2021", "2122", "2223", "2324"]

    # Run simulation
    logger.info("Starting c_prob_adj simulation...")
    results = run_full_simulation(countries, periods, config, verbose=False)

    # Print summary
    print_summary(results, config)

    # Export detailed results
    if not results.empty:
        results.to_excel("cprob_simulation_results.xlsx", index=False)
        logger.success("Results exported to cprob_simulation_results.xlsx")

        # Show worst and best performers
        print("\nTop 5 Most Profitable Teams:")
        print(results.nlargest(5, "profit")[["country", "team", "period", "profit", "roi"]])

        print("\nTop 5 Biggest Losers:")
        print(results.nsmallest(5, "profit")[["country", "team", "period", "profit", "roi"]])
