# Project Context

## Purpose
A Soccer Statistics and Simulation Platform that analyzes European soccer championship data from multiple countries (Greece, England, Italy, Spain, Germany, France). The project:
- Collects historical match data from Football Data UK (football-data.co.uk)
- Analyzes team performance statistics across multiple seasons (2017-18 through 2024-25)
- Generates HTML handout reports with interactive visualizations
- Simulates betting scenarios and match probabilities
- Provides both REST API access and static HTML analytics

## Tech Stack
- **Python 3.13** - Minimum required version
- **UV** - Package manager (fast, reproducible builds with `uv.lock`)
- **pandas 2.2+** - Data manipulation and analysis
- **numpy 2.0+** - Numerical computing
- **Flask 3.0+** - REST API web framework
- **matplotlib 3.9+** - Data visualization/plotting
- **scipy 1.14+** - Scientific computing (probability calculations)
- **handout 1.1.2** - HTML report generation
- **loguru 0.7+** - Structured logging
- **SendGrid 6.11+** - Email delivery service
- **openpyxl 3.1+** - Excel file support
- **External libraries**: ThinkBayes, ThinkStats2, ThinkPlot (Bayesian statistics)

### Development Tools
- **pytest 8.0+** + **pytest-mock** - Testing framework
- **Ruff 0.8+** - Linting and formatting (replaces flake8/autopep8)
- **ipython 8.20+** / **ipykernel 6.29+** - Interactive development

### Package Management
- Dependencies defined in `pyproject.toml` (PEP 621)
- Lockfile: `uv.lock` for reproducible builds
- Python version: `.python-version` file specifies 3.13
- Commands:
  - `uv sync` - Install dependencies
  - `uv run <script>` - Run scripts in managed environment
  - `uv add <package>` - Add new dependencies
  - `uv run ruff check .` - Lint code
  - `uv run ruff format .` - Format code
  - `uv run pytest` - Run tests

## Project Conventions

### Code Style
- **Functions/variables**: snake_case (`load_dataset()`, `create_team_df_dict()`, `period_stats()`)
- **Classes**: PascalCase (`Team_Simulation`, `Simulation`, `FtpAddOns`)
- **Constants**: UPPER_CASE (`PERIODS`, `COUNTRIES`, `CURRENT_PERIOD`, `NEXT_MATCHES`)
- **Type hints**: Used in function signatures
- **Docstrings**: Triple-quoted format with `###` section headers
- **Linting**: Ruff with pycodestyle, Pyflakes, isort, flake8-bugbear rules
- **Formatting**: Ruff formatter (double quotes, space indent)

### Architecture Patterns
The project follows a layered functional architecture:

```
Data Access Layer
├── load_dataset() - fetches CSV from football-data.co.uk
├── load_country() - proxy function for country-specific loaders
└── Specific loaders: load_greece(), load_england(), etc.

Data Processing Layer (sp_soccer_lib/)
├── create_team_df_dict() - transforms raw data into team DataFrames
├── update_results() - calculates match results (W/D/L)
├── update_draw_streaks() - tracks draw/no-draw streaks
└── period_stats() - aggregates statistics by season

Analysis Layer
├── team_stats() - generates comprehensive team statistics
├── no_draw_frequencies() - draw pattern analysis
├── probabilities.py - binomial probability calculations
└── championships.py - calculates team rankings

Presentation Layer
├── Flask API (app.py) - JSON endpoints
├── Handout Reports (soccer1.py) - HTML report generation
└── Visualization (matplotlib plots)

Integration Layer
├── FTP Transfer (ftp_transfer.py) - uploads reports to server
├── Email Service (mail_send.py) - SendGrid integration
└── Update Pipeline (update.py) - orchestrates refresh workflow
```

**Design Principles**:
- Functional programming style with pure functions
- Heavy use of pandas DataFrame transformations
- Chain of transformation: `load_data → create_team_dfs → calculate_stats → generate_report`

### Testing Strategy
- **Framework**: pytest with pytest-mock
- **Unit Tests**: `tests/test_codium.py` - tests `load_dataset()` with mocked dependencies
- **Integration Tests**: `tests/test_greece.py` - tests full pipeline with real data
- **Test Execution**: Run with `uv run pytest`
- **Test Coverage**: Core data loading and statistics functions

### Git Workflow
- **Main branch**: `master`
- **Commit style**: Short descriptive messages (e.g., "Add 2024-2025 Period", "Simulation Checkpoint 2")
- **Spec-driven changes**: Uses OpenSpec framework for change proposals

## Domain Context

### Match Data Encoding
- `FTR` (Full Time Result): 'H' (Home), 'A' (Away), 'D' (Draw)
- `FTHG` (Full Time Home Goals), `FTAG` (Full Time Away Goals)
- `B365D` (Bet365 Draw Odds) - used for probability weighting

### Points System
- Win (W) = 3 points
- Draw (D) = 1 point
- Loss (L) = 0 points

### Statistics Tracked
- Wins, Draws, Losses per team per season
- Goal difference (GF - GA)
- Streak tracking: consecutive draws/no-draws
- Draw frequency distributions
- Binomial probability calculations for upcoming draws

### Supported Championships
| Country | League | Code |
|---------|--------|------|
| Greece | Super League Greece | G1 |
| England | Premier League | E0 |
| Italy | Serie A | I1 |
| Spain | La Liga | SP1 |
| Germany | Bundesliga | D1 |
| France | Ligue 1 | F1 |

### Betting Simulation
- `Team_Simulation` class simulates betting progression strategies
- Parameters: `bet_progr`, `threshold`, `bet_span`, `fixed_odds`
- Tracks cumulative gains/losses across simulated match sequences

## Important Constraints
- **Data Source**: Relies on football-data.co.uk CSV format; date parsing varies by season
- **Date Parsers**: Different parsers for different years (`dateparser1718` vs `dateparser1819`)
- **Team Name Corrections**: Hardcoded fixes for name mismatches (e.g., "Olympiacos Piraeus" → "Olympiakos")
- **Historical Adjustments**: Point deductions for rule violations (e.g., Aris 2122: -6 points)
- **Period Boundaries**: Streak calculations reset across seasons

## External Dependencies
- **Data Source**: https://www.football-data.co.uk/ - Historical match data CSVs
- **Email Service**: SendGrid API for notifications
- **FTP Server**: For uploading generated HTML reports
- **External Libraries**: ThinkBayes/ThinkStats2 (included in `/external/`)
