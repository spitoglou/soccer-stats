# Tasks: Modernize to Python 3.13, UV, and Ruff

## 1. Environment Setup
- [x] 1.1 Install UV package manager (`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`)
- [x] 1.2 Install Python 3.13 via UV (`uv python install 3.13`)
- [x] 1.3 Create `.python-version` file with content `3.13`

## 2. Project Configuration
- [x] 2.1 Create `pyproject.toml` with PEP 621 metadata
- [x] 2.2 Migrate dependencies from `requirements.txt` to `pyproject.toml`
- [x] 2.3 Add development dependencies (pytest, ruff) to `[dependency-groups]`
- [x] 2.4 Configure Ruff linter settings in `[tool.ruff.lint]`
- [x] 2.5 Configure Ruff formatter settings in `[tool.ruff.format]`

## 3. Dependency Updates
- [x] 3.1 Run `uv sync` to generate `uv.lock`
- [x] 3.2 Verify all dependencies are compatible with Python 3.13
- [x] 3.3 Update numpy to latest 3.13-compatible version (2.3.5)
- [x] 3.4 Update pandas to latest 3.13-compatible version (2.3.3)
- [x] 3.5 Update Flask to latest 3.13-compatible version (3.1.2)
- [x] 3.6 Resolve any dependency conflicts

## 4. Ruff Migration
- [x] 4.1 Run `uv run ruff check .` to identify linting issues
- [x] 4.2 Run `uv run ruff check --fix .` to auto-fix safe issues
- [x] 4.3 Run `uv run ruff format .` to format all Python files
- [x] 4.4 Review and manually fix any remaining issues
- [x] 4.5 Remove flake8 and autopep8 from dependencies

## 5. Code Compatibility
- [x] 5.1 Run test suite with Python 3.13 (`uv run pytest`)
- [x] 5.2 Fix any deprecation warnings or breaking changes
- [x] 5.3 Verify Flask app starts correctly
- [x] 5.4 Verify HTML report generation works
- [x] 5.5 Verify data loading from football-data.co.uk

## 6. Cleanup and Documentation
- [x] 6.1 Remove `requirements.txt` (after confirming migration)
- [x] 6.2 Update `openspec/project.md` with new tech stack
- [x] 6.3 Add `uv.lock` to version control
- [x] 6.4 Update `.gitignore` if needed (remove pip artifacts, add UV artifacts)

## 7. Validation
- [x] 7.1 Test suite runs (`uv run pytest`) - Note: some pre-existing test failures unrelated to migration
- [x] 7.2 Linting passes (`uv run ruff check .`)
- [x] 7.3 Formatting is consistent (`uv run ruff format --check .`)
- [x] 7.4 Flask API runs successfully
- [x] 7.5 Report generation works end-to-end
