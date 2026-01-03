# Design: Modernize to Python 3.13 and UV

## Context
The project uses a traditional pip + requirements.txt workflow which lacks:
- Lockfile support for reproducible builds
- Fast dependency resolution
- Integrated Python version management
- Modern project metadata standards (PEP 621)

UV is a Rust-based Python package manager from Astral (creators of Ruff) that provides all these features with significant speed improvements.

## Goals / Non-Goals

### Goals
- Upgrade to Python 3.13 for performance and language improvements
- Adopt UV for faster, reproducible dependency management
- Use PEP 621 `pyproject.toml` as the single source of project metadata
- Maintain all existing functionality

### Non-Goals
- Restructuring the codebase
- Adding new features beyond tooling modernization
- Enabling Python 3.13 free-threading (experimental, not production-ready)

## Decisions

### Decision 1: Use UV instead of pip/pip-tools/poetry
**Rationale**: UV provides:
- 10-100x faster installs than pip
- Built-in lockfile (`uv.lock`) without needing pip-tools
- Python version management (replaces pyenv)
- Drop-in pip compatibility for most commands
- Active development and strong community adoption

**Alternatives considered**:
- **pip-tools**: Adds lockfiles but no speed improvement, requires separate Python management
- **Poetry**: Good lockfile support but slower than UV, different CLI paradigm
- **PDM**: PEP 621 compliant but less community adoption than UV

### Decision 2: Python 3.13 as minimum version
**Rationale**: 
- Latest stable Python release with best performance
- Improved error messages aid debugging
- Free-threading (experimental) available for future parallelism
- All major libraries now support 3.13

**Risk**: Some edge-case libraries may lag in 3.13 support
**Mitigation**: Verify all dependencies before committing

### Decision 3: Maintain requirements.txt temporarily
**Rationale**: Keep `requirements.txt` during transition for rollback capability
**Action**: Delete after successful validation

### Decision 4: Migrate from flake8/autopep8 to Ruff
**Rationale**: 
- Ruff is 10-100x faster than flake8 (written in Rust)
- Single tool replaces both linter (flake8) and formatter (autopep8)
- Same maintainer as UV (Astral) - consistent toolchain
- Configuration lives in `pyproject.toml` - single config file
- Drop-in compatible with flake8 rule sets

**Alternatives considered**:
- **Keep flake8/autopep8**: Works but slower, requires two tools, separate configs
- **Black + flake8**: Popular but still two tools, Black is slower than Ruff

### Decision 5: Do not enable Python 3.13 free-threading
**Rationale**:
- Free-threading (no-GIL) is experimental in Python 3.13
- Requires special build with `--disable-gil` flag
- Core dependencies (numpy, pandas) don't fully support it yet
- No immediate need for parallelism in this project
- Can be revisited when the feature stabilizes in Python 3.14+

### Decision 6: No CI/CD changes required
**Rationale**: The project has no existing CI/CD pipelines (.gitlab-ci.yml, GitHub Actions, Dockerfiles). Local development workflow only.

## pyproject.toml Structure

```toml
[project]
name = "soccer-analytics"
version = "1.0.0"
description = "Soccer statistics and simulation platform"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "handout>=1.1.2",
    "loguru>=0.7.2",
    "numpy>=2.0.0",
    "pandas>=2.2.0",
    "openpyxl>=3.1.2",
    "flask>=3.0.0",
    "matplotlib>=3.9.0",
    "scipy>=1.14.0",
    "sendgrid>=6.11.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "ipython>=8.20.0",
    "ipykernel>=6.29.0",
    "pytest>=8.0.0",
    "pytest-mock>=3.14.0",
]

[tool.uv]
dev-dependencies = [
    "ruff>=0.8.0",
    "pytest>=8.0.0",
    "pytest-mock>=3.14.0",
]

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
]
ignore = [
    "E501",   # line too long (handled by formatter)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## UV Workflow Commands

| Old (pip) | New (UV) |
|-----------|----------|
| `pip install -r requirements.txt` | `uv sync` |
| `pip install package` | `uv add package` |
| `pip install -e .` | `uv sync` (auto-installs project) |
| `python script.py` | `uv run script.py` |
| `pip freeze > requirements.txt` | `uv lock` (auto-generated) |
| `python -m pytest` | `uv run pytest` |
| `flake8 .` | `uv run ruff check .` |
| `autopep8 --in-place file.py` | `uv run ruff format file.py` |

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| Dependency incompatibility with 3.13 | Build failure | Test all deps before committing |
| UV not installed on dev machines | Onboarding friction | Document install in README |
| CI/CD pipeline changes needed | Deployment delay | Update pipelines in same PR |
| Windows-specific UV issues | Dev environment issues | Test on Windows before merge |

## Migration Plan

1. **Preparation** (no code changes)
   - Document current working state
   - Ensure all tests pass on current setup

2. **Add new tooling** (additive)
   - Create `pyproject.toml`
   - Create `.python-version`
   - Generate `uv.lock`

3. **Validate** (testing)
   - Run full test suite with UV
   - Verify Flask app
   - Verify report generation

4. **Cleanup** (removal)
   - Remove `requirements.txt`
   - Update documentation

5. **Rollback plan**
   - Keep `requirements.txt` in git history
   - Can revert to pip workflow by restoring file

## Resolved Questions

1. **Should we also migrate from flake8 to Ruff?**
   - **Decision**: Yes, included in this proposal
   - **Rationale**: Same maintainer as UV (Astral), 10-100x faster, single tool replaces flake8+autopep8

2. **Do we need to update any CI/CD pipelines?**
   - **Decision**: No changes needed
   - **Rationale**: No CI/CD pipelines exist in this project

3. **Should we enable Python 3.13 free-threading experimental features?**
   - **Decision**: No
   - **Rationale**: Experimental feature, numpy/pandas don't fully support it, no immediate parallelism needs
