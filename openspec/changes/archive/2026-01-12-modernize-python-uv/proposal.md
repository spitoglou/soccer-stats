# Change: Modernize to Python 3.13, UV, and Ruff

## Why
The project currently uses Python 3.6+ features with pip-based dependency management via requirements.txt and flake8/autopep8 for linting/formatting. This proposal modernizes the entire toolchain:

1. **Python 3.13**: Significant performance improvements, better error messages, modern language features
2. **UV**: Rust-based package manager offering 10-100x faster dependency resolution, lockfile support, and integrated Python version management
3. **Ruff**: Rust-based linter/formatter (10-100x faster than flake8), single tool replacing flake8+autopep8, from the same team as UV

## What Changes
- **BREAKING**: Minimum Python version raised from 3.6 to 3.13
- Replace `requirements.txt` with `pyproject.toml` (PEP 621 standard)
- Add `uv.lock` for reproducible dependency resolution
- Add `.python-version` file for UV Python version management
- Replace `flake8` with `ruff check` for linting
- Replace `autopep8` with `ruff format` for code formatting
- Update all dependencies to Python 3.13-compatible versions
- Update development workflow to use `uv run`, `uv sync`, and `uv add`

## Impact
- **Affected specs**: build-tooling (new capability)
- **Affected code**:
  - `requirements.txt` → removed, replaced by `pyproject.toml`
  - All `.py` files → reformatted by Ruff
  - `update.py` → may need shebang/environment updates
  - `app.py` → verify Flask compatibility with Python 3.13
- **Developer workflow**: 
  - Install UV and Python 3.13
  - Use `uv run ruff check .` instead of `flake8`
  - Use `uv run ruff format .` instead of `autopep8`
- **Deployment**: Production environment must support Python 3.13

## Benefits
1. **Performance**: Python 3.13 faster startup and improved interpreter
2. **Speed**: UV resolves and installs dependencies 10-100x faster than pip
3. **Reproducibility**: `uv.lock` ensures identical environments across machines
4. **Unified tooling**: Astral ecosystem (UV + Ruff) provides consistent, fast toolchain
5. **Single config**: All settings in `pyproject.toml` (no separate .flake8 or setup.cfg)
6. **Better errors**: Python 3.13 and Ruff both have improved error messages
7. **Simpler workflow**: One tool for linting + formatting instead of two
