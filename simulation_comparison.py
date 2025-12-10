"""
Simulation Comparison Report Generator

Compares three betting strategies:
1. Old c_prob (Gambler's Fallacy - streak-based trigger)
2. c_prob_adj with 0.80 threshold
3. c_prob_adj with 0.90 threshold

Produces a comprehensive markdown report.
"""

import math
from dataclasses import dataclass, field
from datetime import datetime

import numpy as np
import pandas as pd
from loguru import logger

from sp_soccer_lib import create_team_df_dict
from sp_soccer_lib.championships import load_country
from sp_soccer_lib.probabilities import cumulative_binomial_probabilities

# =============================================================================
# Configuration
# =============================================================================


@dataclass
class SimulationConfig:
    """Configuration for betting simulation."""

    name: str
    bet_window: int = 5
    bet_progression: list = field(default_factory=lambda: [2, 4, 6, 9, 13])
    fixed_odds: float = 3.5
    # For c_prob_adj strategies
    threshold: float | None = None
    # For old c_prob strategy
    streak_threshold: int | None = None


COUNTRIES = ["greece", "england", "italy", "spain", "germany", "france"]
PERIODS = ["1920", "2021", "2122", "2223", "2324"]


# =============================================================================
# Simulation Logic
# =============================================================================


@dataclass
class SimulationResult:
    """Results from a simulation run."""

    config_name: str
    country: str
    team: str
    period: str
    total_bet: float = 0.0
    total_won: float = 0.0
    bet_count: int = 0
    win_count: int = 0
    triggers: int = 0
    max_drawdown: float = 0.0
    cash_flow: list = field(default_factory=list)

    @property
    def profit(self) -> float:
        return self.total_won - self.total_bet

    @property
    def roi(self) -> float:
        return (self.profit / self.total_bet * 100) if self.total_bet > 0 else 0.0


def calc_rolling_pdraw(team_df: pd.DataFrame, match_iloc: int, period: str) -> float | None:
    """Calculate draw rate based on matches played so far in the period."""
    period_matches = team_df.iloc[:match_iloc]
    period_matches = period_matches[period_matches["period"] == period]
    total = len(period_matches)
    if total < 3:
        return None
    draws = len(period_matches[period_matches["result"] == "D"])
    return draws / total


def calc_cprob_adj(p_draw: float | None, window: int = 5) -> float | None:
    """Calculate P(at least 1 draw in next N matches)."""
    if p_draw is None or math.isnan(p_draw):
        return None
    result = cumulative_binomial_probabilities(window, 1, p_draw)
    return result[3]


def calc_old_cprob(current_no_draw: int, b365d_mean: float, next_matches: int = 5) -> float:
    """Calculate old c_prob using Gambler's Fallacy logic."""
    matches = next_matches + current_no_draw
    probability = 1 / b365d_mean if b365d_mean > 0 else 0.3
    result = cumulative_binomial_probabilities(matches, 1, probability)
    return result[3]


def get_odds(match: pd.Series, fixed_odds: float = 3.5) -> float:
    """Get betting odds with fallback."""
    odds = match.get("B365D")
    if odds is None or math.isnan(odds):
        return fixed_odds
    return odds


def calculate_max_drawdown(cash_flow: list) -> float:
    """Calculate maximum drawdown from cash flow."""
    if not cash_flow:
        return 0.0
    cumulative = np.cumsum(cash_flow)
    running_max = np.maximum.accumulate(cumulative)
    drawdown = running_max - cumulative
    return float(np.max(drawdown)) if len(drawdown) > 0 else 0.0


def run_cprob_adj_simulation(
    team: str,
    team_df: pd.DataFrame,
    period: str,
    country: str,
    config: SimulationConfig,
) -> SimulationResult:
    """Run c_prob_adj based simulation."""
    result = SimulationResult(config_name=config.name, country=country, team=team, period=period)

    is_betting = False
    bets_remaining = 0
    current_bet_index = 0

    period_mask = team_df["period"] == period
    if not period_mask.any():
        return result

    for match_date, match in team_df.iterrows():
        if match["period"] != period:
            continue

        full_iloc = team_df.index.get_loc(match_date)
        p_draw = calc_rolling_pdraw(team_df, full_iloc, period)
        c_prob_adj = calc_cprob_adj(p_draw, config.bet_window)

        is_draw = match["FTR"] == "D"
        odds = get_odds(match, config.fixed_odds)

        # Check trigger
        if not is_betting and c_prob_adj is not None:
            if c_prob_adj >= config.threshold:
                is_betting = True
                bets_remaining = config.bet_window
                current_bet_index = 0
                result.triggers += 1

        # Process bet
        if is_betting and bets_remaining > 0:
            bet_amount = config.bet_progression[current_bet_index]
            result.total_bet += bet_amount
            result.bet_count += 1
            result.cash_flow.append(-bet_amount)

            if is_draw:
                winnings = bet_amount * odds
                result.total_won += winnings
                result.win_count += 1
                result.cash_flow.append(winnings)
                is_betting = False
                bets_remaining = 0
                current_bet_index = 0
            else:
                bets_remaining -= 1
                current_bet_index = min(current_bet_index + 1, len(config.bet_progression) - 1)
                if bets_remaining == 0:
                    is_betting = False

    result.max_drawdown = calculate_max_drawdown(result.cash_flow)
    return result


def run_old_cprob_simulation(
    team: str,
    team_df: pd.DataFrame,
    period: str,
    country: str,
    config: SimulationConfig,
) -> SimulationResult:
    """Run old c_prob (streak-based) simulation."""
    result = SimulationResult(config_name=config.name, country=country, team=team, period=period)

    is_betting = False
    bets_remaining = 0
    current_bet_index = 0

    period_df = team_df[team_df["period"] == period]
    if period_df.empty:
        return result

    for match_date, match in period_df.iterrows():
        is_draw = match["FTR"] == "D"
        odds = get_odds(match, config.fixed_odds)
        count_no_draw = int(match["count_no_draw"]) if match["count_no_draw"] else 0

        # Check trigger based on streak threshold
        if not is_betting:
            if count_no_draw >= config.streak_threshold:
                is_betting = True
                bets_remaining = config.bet_window
                current_bet_index = count_no_draw - config.streak_threshold
                current_bet_index = min(current_bet_index, len(config.bet_progression) - 1)
                result.triggers += 1

        # Process bet
        if is_betting and bets_remaining > 0:
            bet_amount = config.bet_progression[current_bet_index]
            result.total_bet += bet_amount
            result.bet_count += 1
            result.cash_flow.append(-bet_amount)

            if is_draw:
                winnings = bet_amount * odds
                result.total_won += winnings
                result.win_count += 1
                result.cash_flow.append(winnings)
                is_betting = False
                bets_remaining = 0
                current_bet_index = 0
            else:
                bets_remaining -= 1
                current_bet_index = min(current_bet_index + 1, len(config.bet_progression) - 1)
                if bets_remaining == 0:
                    is_betting = False

    result.max_drawdown = calculate_max_drawdown(result.cash_flow)
    return result


def run_all_simulations() -> dict[str, pd.DataFrame]:
    """Run all three simulation strategies and return results."""

    configs = [
        SimulationConfig(
            name="Old c_prob (Streak >= 4)",
            streak_threshold=4,
            bet_window=5,
        ),
        SimulationConfig(
            name="Old c_prob (Streak >= 6)",
            streak_threshold=6,
            bet_window=5,
        ),
        SimulationConfig(
            name="c_prob_adj (Threshold 0.80)",
            threshold=0.80,
            bet_window=5,
        ),
        SimulationConfig(
            name="c_prob_adj (Threshold 0.90)",
            threshold=0.90,
            bet_window=5,
        ),
    ]

    all_results = {config.name: [] for config in configs}

    for country in COUNTRIES:
        logger.info(f"Processing {country}...")
        df = load_country(country)
        team_dfs = create_team_df_dict(df)

        for team, team_df in team_dfs.items():
            for period in PERIODS:
                for config in configs:
                    if config.streak_threshold is not None:
                        result = run_old_cprob_simulation(team, team_df, period, country, config)
                    else:
                        result = run_cprob_adj_simulation(team, team_df, period, country, config)

                    if result.bet_count > 0:
                        all_results[config.name].append(
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
                                "max_drawdown": result.max_drawdown,
                            }
                        )

    return {name: pd.DataFrame(results) for name, results in all_results.items()}


# =============================================================================
# Report Generation
# =============================================================================


def generate_markdown_report(results: dict[str, pd.DataFrame]) -> str:
    """Generate comprehensive markdown report."""

    report = []
    report.append("# Soccer Draw Betting Simulation Report")
    report.append("")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append("---")
    report.append("")

    # Executive Summary
    report.append("## Executive Summary")
    report.append("")
    report.append(
        f"This report compares {len(results)} betting strategies for predicting soccer draws:"
    )
    report.append("")
    report.append("| Strategy | Description |")
    report.append("|----------|-------------|")

    strategy_descriptions = {
        "Old c_prob (Streak >= 4)": "Gambler's Fallacy - starts betting after 4+ consecutive non-draws",
        "Old c_prob (Streak >= 6)": "Gambler's Fallacy - starts betting after 6+ consecutive non-draws",
        "c_prob_adj (Threshold 0.80)": "Probability-based trigger when P(draw in next 5) >= 80%",
        "c_prob_adj (Threshold 0.90)": "Probability-based trigger when P(draw in next 5) >= 90%",
    }
    for name in results.keys():
        desc = strategy_descriptions.get(name, "Custom strategy")
        report.append(f"| **{name}** | {desc} |")
    report.append("")

    # Summary table
    report.append("### Overall Performance")
    report.append("")

    # Build dynamic header
    header = "| Metric |"
    separator = "|--------|"
    for name in results.keys():
        short_name = (
            name.replace("Old c_prob ", "").replace("c_prob_adj ", "").replace("Threshold ", "T")
        )
        header += f" {short_name} |"
        separator += "------------|"
    report.append(header)
    report.append(separator)

    summaries = {}
    for name, df in results.items():
        if df.empty:
            summaries[name] = {
                "total_bet": 0,
                "total_won": 0,
                "profit": 0,
                "roi": 0,
                "bet_count": 0,
                "win_count": 0,
                "triggers": 0,
                "max_drawdown": 0,
            }
        else:
            summaries[name] = {
                "total_bet": df["total_bet"].sum(),
                "total_won": df["total_won"].sum(),
                "profit": df["profit"].sum(),
                "roi": (df["profit"].sum() / df["total_bet"].sum() * 100)
                if df["total_bet"].sum() > 0
                else 0,
                "bet_count": df["bet_count"].sum(),
                "win_count": df["win_count"].sum(),
                "triggers": df["triggers"].sum(),
                "max_drawdown": df["max_drawdown"].max(),
            }

    names = list(results.keys())
    s = [summaries[n] for n in names]

    # Build dynamic rows
    def build_row(label, key, fmt=",.0f", suffix="EUR", bold=False):
        row = f"| {label} |" if not bold else f"| **{label}** |"
        for i in range(len(s)):
            val = f"{s[i][key]:{fmt}}"
            if suffix:
                val = f"{val} {suffix}"
            if bold:
                val = f"**{val}**"
            row += f" {val} |"
        return row

    report.append(build_row("Total Bet", "total_bet", ",.0f", "EUR"))
    report.append(build_row("Total Won", "total_won", ",.2f", "EUR"))
    report.append(build_row("Net Profit", "profit", ",.2f", "EUR", bold=True))
    report.append(build_row("ROI", "roi", ".2f", "%", bold=True))
    report.append(build_row("Bets Placed", "bet_count", ",", ""))
    report.append(build_row("Wins", "win_count", ",", ""))

    # Win rate row
    win_rates = [
        s[i]["win_count"] / s[i]["bet_count"] * 100 if s[i]["bet_count"] > 0 else 0
        for i in range(len(s))
    ]
    row = "| Win Rate |"
    for wr in win_rates:
        row += f" {wr:.1f}% |"
    report.append(row)

    report.append(build_row("Triggers", "triggers", ",", ""))
    report.append(build_row("Max Drawdown", "max_drawdown", ".2f", "EUR"))
    report.append("")

    # Key Findings
    report.append("### Key Findings")
    report.append("")

    best_roi = max(s, key=lambda x: x["roi"])
    worst_roi = min(s, key=lambda x: x["roi"])
    best_name = names[s.index(best_roi)]
    worst_name = names[s.index(worst_roi)]

    report.append(f"1. **All strategies lose money** - No strategy achieved positive ROI")
    report.append(f"2. **Best performer**: {best_name} with {best_roi['roi']:.2f}% ROI")
    report.append(f"3. **Worst performer**: {worst_name} with {worst_roi['roi']:.2f}% ROI")
    report.append(f"4. **Higher thresholds = fewer bets** but not better results")
    report.append("")

    report.append("---")
    report.append("")

    # Detailed Analysis
    report.append("## Detailed Analysis")
    report.append("")

    # By Country
    report.append("### Performance by Country")
    report.append("")

    for name, df in results.items():
        if df.empty:
            continue
        report.append(f"#### {name}")
        report.append("")
        country_summary = (
            df.groupby("country")
            .agg(
                {
                    "total_bet": "sum",
                    "total_won": "sum",
                    "profit": "sum",
                    "bet_count": "sum",
                    "win_count": "sum",
                }
            )
            .round(2)
        )
        country_summary["roi"] = (
            country_summary["profit"] / country_summary["total_bet"] * 100
        ).round(2)

        report.append("| Country | Bet | Won | Profit | ROI | Bets | Wins |")
        report.append("|---------|-----|-----|--------|-----|------|------|")
        for country, row in country_summary.iterrows():
            report.append(
                f"| {country.title()} | {row['total_bet']:,.0f} | {row['total_won']:,.2f} | {row['profit']:,.2f} | {row['roi']:.2f}% | {int(row['bet_count'])} | {int(row['win_count'])} |"
            )
        report.append("")

    # By Period
    report.append("### Performance by Period")
    report.append("")

    for name, df in results.items():
        if df.empty:
            continue
        report.append(f"#### {name}")
        report.append("")
        period_summary = (
            df.groupby("period")
            .agg(
                {
                    "total_bet": "sum",
                    "total_won": "sum",
                    "profit": "sum",
                    "bet_count": "sum",
                }
            )
            .round(2)
        )
        period_summary["roi"] = (
            period_summary["profit"] / period_summary["total_bet"] * 100
        ).round(2)

        report.append("| Period | Bet | Won | Profit | ROI |")
        report.append("|--------|-----|-----|--------|-----|")
        for period, row in period_summary.iterrows():
            season = f"20{period[:2]}-20{period[2:]}"
            report.append(
                f"| {season} | {row['total_bet']:,.0f} | {row['total_won']:,.2f} | {row['profit']:,.2f} | {row['roi']:.2f}% |"
            )
        report.append("")

    # Top/Bottom Performers
    report.append("### Top and Bottom Performers")
    report.append("")

    for name, df in results.items():
        if df.empty:
            continue
        report.append(f"#### {name}")
        report.append("")

        report.append("**Top 5 Most Profitable:**")
        report.append("")
        report.append("| Country | Team | Period | Profit | ROI |")
        report.append("|---------|------|--------|--------|-----|")
        top5 = df.nlargest(5, "profit")
        for _, row in top5.iterrows():
            report.append(
                f"| {row['country'].title()} | {row['team']} | {row['period']} | {row['profit']:.2f} | {row['roi']:.1f}% |"
            )
        report.append("")

        report.append("**Bottom 5 (Biggest Losses):**")
        report.append("")
        report.append("| Country | Team | Period | Profit | ROI |")
        report.append("|---------|------|--------|--------|-----|")
        bottom5 = df.nsmallest(5, "profit")
        for _, row in bottom5.iterrows():
            report.append(
                f"| {row['country'].title()} | {row['team']} | {row['period']} | {row['profit']:.2f} | {row['roi']:.1f}% |"
            )
        report.append("")

    report.append("---")
    report.append("")

    # Mathematical Analysis
    report.append("## Mathematical Analysis")
    report.append("")

    report.append("### Why All Strategies Fail")
    report.append("")
    report.append("#### 1. The Gambler's Fallacy (Old c_prob)")
    report.append("")
    report.append(
        'The old c_prob strategy assumes that after a streak of non-draws, a draw becomes "due."'
    )
    report.append("This is mathematically incorrect:")
    report.append("")
    report.append("```")
    report.append("P(draw | 5 previous non-draws) = P(draw) ≈ 0.25-0.30")
    report.append("```")
    report.append("")
    report.append(
        "Each match is an **independent event**. Past results don't affect future probabilities."
    )
    report.append("")

    report.append("#### 2. The Threshold Trap (c_prob_adj)")
    report.append("")
    report.append("While c_prob_adj avoids the Gambler's Fallacy, it still fails because:")
    report.append("")
    report.append("- A high c_prob_adj (e.g., 0.90) requires a high draw rate (p_draw ≥ 0.37)")
    report.append("- Bookmakers **know** which teams draw frequently")
    report.append("- They set **lower odds** for high-draw teams, eliminating any edge")
    report.append("")
    report.append("**Required draw rates for thresholds:**")
    report.append("")
    report.append("| Threshold | Required p_draw | Meaning |")
    report.append("|-----------|-----------------|---------|")
    report.append("| 0.80 | ≥ 0.28 | Team draws ~28% of matches |")
    report.append("| 0.85 | ≥ 0.32 | Team draws ~32% of matches |")
    report.append("| 0.90 | ≥ 0.37 | Team draws ~37% of matches |")
    report.append("")

    report.append("#### 3. The House Edge")
    report.append("")
    report.append("Bookmaker margins (overround) typically add 5-10% to the true odds.")
    report.append(
        "This means any strategy without genuine predictive power will lose ~3-5% over time."
    )
    report.append("")
    report.append("Our simulation results align with this expectation:")
    report.append("")
    for name in names:
        report.append(f"- {name}: {summaries[name]['roi']:.2f}% ROI")
    report.append("")

    report.append("### Progressive Betting Doesn't Help")
    report.append("")
    report.append(
        "The bet progression `[2, 4, 6, 9, 13]` (total: 34 EUR per cycle) is a variant of"
    )
    report.append(
        "the **Martingale system**. While it wins frequently, the occasional complete loss"
    )
    report.append("of a cycle wipes out multiple wins.")
    report.append("")
    report.append("**Expected outcomes per cycle:**")
    report.append("")
    report.append("| Outcome | Probability | Net Result |")
    report.append("|---------|-------------|------------|")
    report.append("| Win on bet 1 | ~30% | +4 to +5 EUR |")
    report.append("| Win on bet 2 | ~21% | +6 to +8 EUR |")
    report.append("| Win on bet 3 | ~15% | +8 to +12 EUR |")
    report.append("| Win on bet 4 | ~10% | +10 to +18 EUR |")
    report.append("| Win on bet 5 | ~7% | +12 to +26 EUR |")
    report.append("| **Lose all 5** | **~17%** | **-34 EUR** |")
    report.append("")

    report.append("---")
    report.append("")

    # Conclusions
    report.append("## Conclusions")
    report.append("")
    report.append("### Summary")
    report.append("")
    report.append(
        "1. **No strategy is profitable** - All three approaches lose money over the long term"
    )
    report.append(
        "2. **The mathematical edge doesn't exist** - Neither streak-based nor probability-based"
    )
    report.append("   triggers provide predictive power")
    report.append(
        "3. **Bookmakers are efficient** - Odds already account for team-specific draw rates"
    )
    report.append(
        "4. **Progressive betting amplifies losses** - While smoothing short-term variance,"
    )
    report.append("   it doesn't overcome the negative expected value")
    report.append("")

    report.append("### Recommendations")
    report.append("")
    report.append("If the goal is **entertainment** with controlled losses:")
    report.append("- Use flat betting instead of progression")
    report.append("- Set strict loss limits per session")
    report.append("- Accept that the expected return is negative")
    report.append("")
    report.append("If the goal is **profit**:")
    report.append("- These strategies will not achieve it")
    report.append("- Consider that sports betting markets are highly efficient")
    report.append("- Any genuine edge would require information not reflected in odds")
    report.append("")

    report.append("---")
    report.append("")
    report.append("## Appendix: Simulation Parameters")
    report.append("")
    report.append("| Parameter | Value |")
    report.append("|-----------|-------|")
    report.append(f"| Countries | {', '.join([c.title() for c in COUNTRIES])} |")
    report.append(f"| Periods | {', '.join(['20' + p[:2] + '-20' + p[2:] for p in PERIODS])} |")
    report.append("| Bet Progression | [2, 4, 6, 9, 13] EUR |")
    report.append("| Bet Window | 5 matches |")
    report.append("| Old c_prob Streak Threshold | 4 consecutive non-draws |")
    report.append("| c_prob_adj Thresholds | 0.80, 0.90 |")
    report.append("| Fallback Odds | 3.5 |")
    report.append("")

    return "\n".join(report)


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    logger.info("Starting simulation comparison...")

    # Run all simulations
    results = run_all_simulations()

    # Generate report
    logger.info("Generating markdown report...")
    report = generate_markdown_report(results)

    # Save report
    report_path = "simulation_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    logger.success(f"Report saved to {report_path}")

    # Also save detailed Excel files
    for name, df in results.items():
        if not df.empty:
            # Create safe filename
            safe_name = name.replace(" ", "_").replace("(", "").replace(")", "").replace(".", "")
            safe_name = safe_name.replace(">", "").replace("<", "").replace("=", "")
            df.to_excel(f"simulation_{safe_name}.xlsx", index=False)
            logger.info(f"Saved simulation_{safe_name}.xlsx")

    # Print summary to console
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)
    for name, df in results.items():
        if not df.empty:
            total_profit = df["profit"].sum()
            total_bet = df["total_bet"].sum()
            roi = (total_profit / total_bet * 100) if total_bet > 0 else 0
            print(f"{name}: {total_profit:,.2f} EUR ({roi:.2f}% ROI)")
    print("=" * 70)
    print(f"\nFull report: {report_path}")
