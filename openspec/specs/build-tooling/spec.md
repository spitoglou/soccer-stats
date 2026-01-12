# build-tooling Specification

## Purpose
TBD - created by archiving change modernize-python-uv. Update Purpose after archive.
## Requirements
### Requirement: Python Version Management
The project SHALL use Python 3.13 as the minimum required version, managed via a `.python-version` file.

#### Scenario: Python version specification
- **WHEN** a developer clones the repository
- **THEN** the `.python-version` file specifies Python 3.13
- **AND** UV automatically uses the correct Python version

#### Scenario: Python version validation
- **WHEN** a developer runs `uv sync` without Python 3.13
- **THEN** UV prompts to install Python 3.13 or fails with a clear error

### Requirement: UV Package Management
The project SHALL use UV as the package manager for dependency installation, resolution, and lockfile management.

#### Scenario: Initial environment setup
- **WHEN** a developer runs `uv sync`
- **THEN** all dependencies are installed from `uv.lock`
- **AND** a virtual environment is created in `.venv/`

#### Scenario: Adding a new dependency
- **WHEN** a developer runs `uv add <package>`
- **THEN** the package is added to `pyproject.toml`
- **AND** `uv.lock` is updated with resolved versions

#### Scenario: Reproducible builds
- **WHEN** two developers run `uv sync` on the same commit
- **THEN** they get identical dependency versions from `uv.lock`

### Requirement: PEP 621 Project Metadata
The project SHALL define all metadata in `pyproject.toml` following PEP 621 standards.

#### Scenario: Project metadata defined
- **WHEN** inspecting `pyproject.toml`
- **THEN** it contains `[project]` table with name, version, description, and dependencies

#### Scenario: Development dependencies
- **WHEN** a developer runs `uv sync`
- **THEN** development dependencies (pytest, ruff) are installed
- **AND** production dependencies are installed

### Requirement: Script Execution
The project SHALL use `uv run` to execute Python scripts within the managed environment.

#### Scenario: Running tests
- **WHEN** a developer runs `uv run pytest`
- **THEN** pytest executes with the project's virtual environment

#### Scenario: Running Flask application
- **WHEN** a developer runs `uv run python app.py`
- **THEN** the Flask application starts with all dependencies available

#### Scenario: Running report generation
- **WHEN** a developer runs `uv run python soccer1.py`
- **THEN** the HTML report is generated successfully

### Requirement: Lockfile Version Control
The project SHALL commit `uv.lock` to version control to ensure reproducible builds.

#### Scenario: Lockfile committed
- **WHEN** inspecting the repository
- **THEN** `uv.lock` is present and tracked by git

#### Scenario: Lockfile not in gitignore
- **WHEN** inspecting `.gitignore`
- **THEN** `uv.lock` is NOT listed as ignored

### Requirement: Ruff Linting
The project SHALL use Ruff as the linter, replacing flake8.

#### Scenario: Running linter
- **WHEN** a developer runs `uv run ruff check .`
- **THEN** Ruff checks all Python files for linting issues
- **AND** reports any violations with file locations and rule codes

#### Scenario: Auto-fixing linting issues
- **WHEN** a developer runs `uv run ruff check --fix .`
- **THEN** Ruff automatically fixes safe linting issues
- **AND** reports issues that require manual intervention

#### Scenario: Linter configuration
- **WHEN** inspecting `pyproject.toml`
- **THEN** `[tool.ruff.lint]` section defines enabled rule sets
- **AND** target Python version is set to 3.13

### Requirement: Ruff Formatting
The project SHALL use Ruff as the code formatter, replacing autopep8.

#### Scenario: Formatting code
- **WHEN** a developer runs `uv run ruff format .`
- **THEN** Ruff formats all Python files consistently

#### Scenario: Checking format compliance
- **WHEN** a developer runs `uv run ruff format --check .`
- **THEN** Ruff reports files that would be reformatted
- **AND** exits with non-zero status if changes are needed

#### Scenario: Formatter configuration
- **WHEN** inspecting `pyproject.toml`
- **THEN** `[tool.ruff.format]` section defines quote style and indent style

