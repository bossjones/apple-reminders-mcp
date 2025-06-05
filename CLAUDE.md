# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Apple Reminders MCP (Model Context Protocol) server that provides programmatic access to Apple Reminders using AppleScript. The project is built with Python and uses the FastMCP framework.

## Core Architecture

### Main Components

- **Server (`src/apple_reminders_mcp/server.py`)**: FastMCP server with Apple Reminders tools
  - Uses AppleScript via subprocess calls to interact with Apple Reminders
  - Provides MCP tools: `create_reminder`, `get_reminder`, `list_reminder_lists`, `delete_reminder`
  - Handles date/time formatting and error handling for AppleScript operations

- **CLI (`src/apple_reminders_mcp/cli.py`)**: Command-line interface using AsyncTyper
  - Provides version, dependencies, and diagnostic commands
  - Uses structured logging with Loguru integration
  - Includes early initialization pattern for logging setup

- **Environment (`src/apple_reminders_mcp/env.py`)**: Pydantic-based settings management
  - Comprehensive configuration with validation
  - Supports multiple environments (dev, staging, production)
  - Includes API keys management and security settings

- **Logging (`src/apple_reminders_mcp/logging/`)**: Thread-safe logging infrastructure
  - Early initialization pattern to prevent import conflicts
  - Thread-safe configuration with interceptors
  - Supports JSON logging, file output, and sensitive data obfuscation

### Development Tools and Commands

**Essential Commands (from Makefile):**
- `make install` - Set up virtual environment with uv and pre-commit hooks
- `make check` - Run comprehensive code quality checks (pre-commit, pyright, deptry)
- `make test` - Run pytest with coverage reporting
- `make build` - Build wheel distribution
- `make docs` - Build and serve MkDocs documentation
- `make docs-test` - Test documentation build

**Quality Assurance:**
- Uses `uv` for dependency management and virtual environments
- Pre-commit hooks for code formatting and linting
- Pyright for static type checking
- Ruff for linting and formatting (configured in pyproject.toml)
- Pytest with comprehensive coverage reporting
- MyPy for additional type checking

**Testing:**
- Run tests: `uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml`
- Single test: `uv run python -m pytest tests/test_specific.py -v`
- Test markers available for different test categories (see pyproject.toml pytest configuration)

**Linting and Type Checking:**
- Lint: `uv run pre-commit run -a`
- Type check: `uv run pyright src`
- Format: `uv run ruff format`
- Dependency check: `uv run deptry src`

## Development Patterns

### Environment Configuration
- Use `McpSettings` from `env.py` for configuration management
- Settings auto-load from `.env` files and environment variables
- All secrets should use `SecretStr` type for proper handling

### Logging Setup
- Always call `early_init()` first before importing other modules
- Use `setup_apple_reminders_mcp_logging(settings)` for production logging
- Thread-safe logging is configured for async/multi-threaded environments

### Error Handling
- AppleScript interactions should always include try/catch with proper error messages
- Use JSON responses for structured error reporting in MCP tools
- Include both success and error paths in all tool implementations

### Code Style
- Line length: 120 characters (configured in pyproject.toml)
- Use type hints throughout the codebase
- Follow Google docstring style for documentation
- Prefer explicit imports over wildcard imports

## MCP Server Specifics

The server provides these MCP tools for Apple Reminders:

1. **create_reminder**: Creates new reminders with date/time, notes, and list assignment
2. **get_reminder**: Retrieves reminders from specific lists with completion status filtering
3. **list_reminder_lists**: Lists all available reminder lists
4. **delete_reminder**: Removes reminders by name from specific lists or all lists

All tools use AppleScript execution via `run_applescript()` function and include comprehensive error handling.

## Dependencies

- **MCP Framework**: `mcp[cli]>=1.9.3` for Model Context Protocol server
- **Async Framework**: Built on FastMCP for async MCP server implementation
- **CLI Framework**: Typer/AsyncTyper for command-line interface
- **Logging**: Loguru for structured, thread-safe logging
- **Configuration**: Pydantic Settings for type-safe configuration management
- **Development**: Comprehensive dev dependencies including pytest, ruff, pyright, pre-commit

## Environment Setup

1. Install with uv: `make install`
2. Configure environment variables in `.env` file
3. Run pre-commit to fix any formatting issues: `uv run pre-commit run -a`
4. Test the setup: `make test`
