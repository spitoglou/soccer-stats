# Soccer Draw Betting Simulation Report

**Generated:** 2025-12-10 22:27:39

---

## Executive Summary

This report compares 4 betting strategies for predicting soccer draws:

| Strategy | Description |
|----------|-------------|
| **Old c_prob (Streak >= 4)** | Gambler's Fallacy - starts betting after 4+ consecutive non-draws |
| **Old c_prob (Streak >= 6)** | Gambler's Fallacy - starts betting after 6+ consecutive non-draws |
| **c_prob_adj (Threshold 0.80)** | Probability-based trigger when P(draw in next 5) >= 80% |
| **c_prob_adj (Threshold 0.90)** | Probability-based trigger when P(draw in next 5) >= 90% |

### Overall Performance

| Metric | (Streak >= 4) | (Streak >= 6) | (T0.80) | (T0.90) |
|--------|------------|------------|------------|------------|
| Total Bet | 39,284 EUR | 20,664 EUR | 39,342 EUR | 17,806 EUR |
| Total Won | 31,510.21 EUR | 16,868.04 EUR | 38,035.21 EUR | 16,893.82 EUR |
| **Net Profit** | **-7,773.79 EUR** | **-3,795.96 EUR** | **-1,306.79 EUR** | **-912.18 EUR** |
| **ROI** | **-19.79 %** | **-18.37 %** | **-3.32 %** | **-5.12 %** |
| Bets Placed | 5,644 | 2,960 | 7,682 | 3,435 |
| Wins | 1,025 | 538 | 2,007 | 890 |
| Win Rate | 18.2% | 18.2% | 26.1% | 25.9% |
| Triggers | 1,582 | 850 | 2,684 | 1,178 |
| Max Drawdown | 266.00 EUR | 240.00 EUR | 135.50 EUR | 97.60 EUR |

### Key Findings

1. **All strategies lose money** - No strategy achieved positive ROI
2. **Best performer**: c_prob_adj (Threshold 0.80) with -3.32% ROI
3. **Worst performer**: Old c_prob (Streak >= 4) with -19.79% ROI
4. **Higher thresholds = fewer bets** but not better results

---

## Detailed Analysis

### Performance by Country

#### Old c_prob (Streak >= 4)

| Country | Bet | Won | Profit | ROI | Bets | Wins |
|---------|-----|-----|--------|-----|------|------|
| England | 8,780 | 6,446.28 | -2,333.72 | -26.58% | 1187 | 188 |
| France | 6,504 | 5,027.94 | -1,476.06 | -22.69% | 921 | 164 |
| Germany | 6,303 | 5,122.45 | -1,180.55 | -18.73% | 904 | 158 |
| Greece | 3,953 | 3,307.49 | -645.51 | -16.33% | 601 | 122 |
| Italy | 6,540 | 5,720.10 | -819.90 | -12.54% | 980 | 194 |
| Spain | 7,204 | 5,885.95 | -1,318.05 | -18.30% | 1051 | 199 |

#### Old c_prob (Streak >= 6)

| Country | Bet | Won | Profit | ROI | Bets | Wins |
|---------|-----|-----|--------|-----|------|------|
| England | 4,953 | 3,789.78 | -1,163.22 | -23.49% | 679 | 113 |
| France | 3,481 | 2,670.49 | -810.51 | -23.28% | 494 | 86 |
| Germany | 3,373 | 2,778.56 | -594.44 | -17.62% | 481 | 83 |
| Greece | 1,896 | 1,639.40 | -256.60 | -13.53% | 290 | 58 |
| Italy | 3,262 | 2,786.98 | -475.02 | -14.56% | 476 | 93 |
| Spain | 3,699 | 3,202.83 | -496.17 | -13.41% | 540 | 105 |

#### c_prob_adj (Threshold 0.80)

| Country | Bet | Won | Profit | ROI | Bets | Wins |
|---------|-----|-----|--------|-----|------|------|
| England | 6,377 | 6,228.09 | -148.91 | -2.34% | 1247 | 311 |
| France | 6,743 | 5,993.22 | -749.78 | -11.12% | 1291 | 314 |
| Germany | 5,920 | 6,078.80 | 158.80 | 2.68% | 1142 | 290 |
| Greece | 4,658 | 4,587.76 | -70.24 | -1.51% | 925 | 259 |
| Italy | 7,008 | 7,168.52 | 160.52 | 2.29% | 1388 | 381 |
| Spain | 8,636 | 7,978.82 | -657.18 | -7.61% | 1689 | 452 |

#### c_prob_adj (Threshold 0.90)

| Country | Bet | Won | Profit | ROI | Bets | Wins |
|---------|-----|-----|--------|-----|------|------|
| England | 2,714 | 2,581.96 | -132.04 | -4.87% | 540 | 144 |
| France | 3,074 | 2,538.60 | -535.40 | -17.42% | 573 | 132 |
| Germany | 2,996 | 3,105.03 | 109.03 | 3.64% | 560 | 141 |
| Greece | 2,198 | 1,899.81 | -298.19 | -13.57% | 417 | 104 |
| Italy | 2,937 | 2,859.12 | -77.88 | -2.65% | 572 | 150 |
| Spain | 3,887 | 3,909.30 | 22.30 | 0.57% | 773 | 219 |

### Performance by Period

#### Old c_prob (Streak >= 4)

| Period | Bet | Won | Profit | ROI |
|--------|-----|-----|--------|-----|
| 2019-2020 | 8,186 | 5,510.81 | -2,675.19 | -32.68% |
| 2020-2021 | 7,022 | 6,336.24 | -685.76 | -9.77% |
| 2021-2022 | 7,931 | 6,108.95 | -1,822.05 | -22.97% |
| 2022-2023 | 8,811 | 6,997.11 | -1,813.89 | -20.59% |
| 2023-2024 | 7,334 | 6,557.10 | -776.90 | -10.59% |

#### Old c_prob (Streak >= 6)

| Period | Bet | Won | Profit | ROI |
|--------|-----|-----|--------|-----|
| 2019-2020 | 4,734 | 3,325.64 | -1,408.36 | -29.75% |
| 2020-2021 | 3,443 | 3,071.81 | -371.19 | -10.78% |
| 2021-2022 | 4,285 | 3,263.76 | -1,021.24 | -23.83% |
| 2022-2023 | 4,639 | 3,948.57 | -690.43 | -14.88% |
| 2023-2024 | 3,563 | 3,258.26 | -304.74 | -8.55% |

#### c_prob_adj (Threshold 0.80)

| Period | Bet | Won | Profit | ROI |
|--------|-----|-----|--------|-----|
| 2019-2020 | 6,778 | 6,446.96 | -331.04 | -4.88% |
| 2020-2021 | 8,139 | 8,140.45 | 1.45 | 0.02% |
| 2021-2022 | 8,319 | 7,844.09 | -474.91 | -5.71% |
| 2022-2023 | 8,201 | 7,299.07 | -901.93 | -11.00% |
| 2023-2024 | 7,905 | 8,304.64 | 399.64 | 5.06% |

#### c_prob_adj (Threshold 0.90)

| Period | Bet | Won | Profit | ROI |
|--------|-----|-----|--------|-----|
| 2019-2020 | 3,128 | 2,834.87 | -293.13 | -9.37% |
| 2020-2021 | 3,703 | 3,588.40 | -114.60 | -3.09% |
| 2021-2022 | 4,057 | 4,018.37 | -38.63 | -0.95% |
| 2022-2023 | 3,271 | 2,612.39 | -658.61 | -20.13% |
| 2023-2024 | 3,647 | 3,839.79 | 192.79 | 5.29% |

### Top and Bottom Performers

#### Old c_prob (Streak >= 4)

**Top 5 Most Profitable:**

| Country | Team | Period | Profit | ROI |
|---------|------|--------|--------|-----|
| Germany | Bayern Munich | 2021 | 189.75 | 156.8% |
| Spain | Real Madrid | 2021 | 76.90 | 93.8% |
| Italy | Roma | 2021 | 68.32 | 108.4% |
| Germany | Mainz | 2223 | 68.20 | 106.6% |
| Spain | Barcelona | 2021 | 66.40 | 47.1% |

**Bottom 5 (Biggest Losses):**

| Country | Team | Period | Profit | ROI |
|---------|------|--------|--------|-----|
| England | Man City | 2021 | -268.00 | -100.0% |
| Italy | Napoli | 2223 | -216.00 | -80.6% |
| Germany | Bayern Munich | 2122 | -187.00 | -74.8% |
| Germany | Mainz | 1920 | -183.80 | -80.6% |
| England | Arsenal | 2122 | -180.00 | -66.4% |

#### Old c_prob (Streak >= 6)

**Top 5 Most Profitable:**

| Country | Team | Period | Profit | ROI |
|---------|------|--------|--------|-----|
| Germany | Bayern Munich | 2021 | 144.00 | 276.9% |
| England | Man City | 2223 | 87.29 | 73.4% |
| Germany | Bayern Munich | 2223 | 72.82 | 173.4% |
| France | Monaco | 2021 | 56.57 | 84.4% |
| Italy | Milan | 2223 | 44.60 | 97.0% |

**Bottom 5 (Biggest Losses):**

| Country | Team | Period | Profit | ROI |
|---------|------|--------|--------|-----|
| England | Man City | 2021 | -242.00 | -100.0% |
| Italy | Napoli | 2223 | -229.00 | -100.0% |
| France | Strasbourg | 1920 | -164.00 | -100.0% |
| England | Liverpool | 1920 | -150.80 | -81.5% |
| Germany | Mainz | 1920 | -147.80 | -77.0% |

#### c_prob_adj (Threshold 0.80)

**Top 5 Most Profitable:**

| Country | Team | Period | Profit | ROI |
|---------|------|--------|--------|-----|
| Germany | FC Koln | 2223 | 138.10 | 85.8% |
| Germany | M'gladbach | 2324 | 127.00 | 88.8% |
| Italy | Udinese | 2324 | 122.30 | 102.8% |
| Germany | Mainz | 2324 | 114.06 | 98.3% |
| Germany | Union Berlin | 2021 | 109.40 | 84.2% |

**Bottom 5 (Biggest Losses):**

| Country | Team | Period | Profit | ROI |
|---------|------|--------|--------|-----|
| Spain | Osasuna | 2122 | -105.80 | -61.2% |
| France | Lens | 2122 | -103.74 | -63.3% |
| Italy | Genoa | 1920 | -103.20 | -66.2% |
| Spain | Vallecano | 2223 | -101.20 | -57.8% |
| Germany | Leverkusen | 2021 | -100.15 | -60.0% |

#### c_prob_adj (Threshold 0.90)

**Top 5 Most Profitable:**

| Country | Team | Period | Profit | ROI |
|---------|------|--------|--------|-----|
| Germany | FC Koln | 2223 | 134.90 | 85.9% |
| Italy | Udinese | 2324 | 122.30 | 102.8% |
| Germany | Union Berlin | 2021 | 104.90 | 82.0% |
| Spain | Ath Madrid | 1920 | 96.70 | 74.4% |
| England | Crystal Palace | 2122 | 95.90 | 63.9% |

**Bottom 5 (Biggest Losses):**

| Country | Team | Period | Profit | ROI |
|---------|------|--------|--------|-----|
| Italy | Cagliari | 2122 | -88.60 | -76.4% |
| Spain | Sociedad | 2324 | -74.00 | -56.9% |
| Spain | Osasuna | 2122 | -63.00 | -90.0% |
| Germany | Leverkusen | 2021 | -62.00 | -88.6% |
| Germany | Wolfsburg | 2223 | -61.60 | -88.0% |

---

## Mathematical Analysis

### Why All Strategies Fail

#### 1. The Gambler's Fallacy (Old c_prob)

The old c_prob strategy assumes that after a streak of non-draws, a draw becomes "due."
This is mathematically incorrect:

```
P(draw | 5 previous non-draws) = P(draw) ≈ 0.25-0.30
```

Each match is an **independent event**. Past results don't affect future probabilities.

#### 2. The Threshold Trap (c_prob_adj)

While c_prob_adj avoids the Gambler's Fallacy, it still fails because:

- A high c_prob_adj (e.g., 0.90) requires a high draw rate (p_draw ≥ 0.37)
- Bookmakers **know** which teams draw frequently
- They set **lower odds** for high-draw teams, eliminating any edge

**Required draw rates for thresholds:**

| Threshold | Required p_draw | Meaning |
|-----------|-----------------|---------|
| 0.80 | ≥ 0.28 | Team draws ~28% of matches |
| 0.85 | ≥ 0.32 | Team draws ~32% of matches |
| 0.90 | ≥ 0.37 | Team draws ~37% of matches |

#### 3. The House Edge

Bookmaker margins (overround) typically add 5-10% to the true odds.
This means any strategy without genuine predictive power will lose ~3-5% over time.

Our simulation results align with this expectation:

- Old c_prob (Streak >= 4): -19.79% ROI
- Old c_prob (Streak >= 6): -18.37% ROI
- c_prob_adj (Threshold 0.80): -3.32% ROI
- c_prob_adj (Threshold 0.90): -5.12% ROI

### Progressive Betting Doesn't Help

The bet progression `[2, 4, 6, 9, 13]` (total: 34 EUR per cycle) is a variant of
the **Martingale system**. While it wins frequently, the occasional complete loss
of a cycle wipes out multiple wins.

**Expected outcomes per cycle:**

| Outcome | Probability | Net Result |
|---------|-------------|------------|
| Win on bet 1 | ~30% | +4 to +5 EUR |
| Win on bet 2 | ~21% | +6 to +8 EUR |
| Win on bet 3 | ~15% | +8 to +12 EUR |
| Win on bet 4 | ~10% | +10 to +18 EUR |
| Win on bet 5 | ~7% | +12 to +26 EUR |
| **Lose all 5** | **~17%** | **-34 EUR** |

---

## Conclusions

### Summary

1. **No strategy is profitable** - All three approaches lose money over the long term
2. **The mathematical edge doesn't exist** - Neither streak-based nor probability-based
   triggers provide predictive power
3. **Bookmakers are efficient** - Odds already account for team-specific draw rates
4. **Progressive betting amplifies losses** - While smoothing short-term variance,
   it doesn't overcome the negative expected value

### Recommendations

If the goal is **entertainment** with controlled losses:
- Use flat betting instead of progression
- Set strict loss limits per session
- Accept that the expected return is negative

If the goal is **profit**:
- These strategies will not achieve it
- Consider that sports betting markets are highly efficient
- Any genuine edge would require information not reflected in odds

---

## Appendix: Simulation Parameters

| Parameter | Value |
|-----------|-------|
| Countries | Greece, England, Italy, Spain, Germany, France |
| Periods | 2019-2020, 2020-2021, 2021-2022, 2022-2023, 2023-2024 |
| Bet Progression | [2, 4, 6, 9, 13] EUR |
| Bet Window | 5 matches |
| Old c_prob Streak Threshold | 4 consecutive non-draws |
| c_prob_adj Thresholds | 0.80, 0.90 |
| Fallback Odds | 3.5 |
