# MCP Apple Reminders Server

[![Release](https://img.shields.io/github/v/release/bossjones/apple-reminders-mcp)](https://img.shields.io/github/v/release/bossjones/apple-reminders-mcp)
[![Build status](https://img.shields.io/github/actions/workflow/status/bossjones/apple-reminders-mcp/main.yml?branch=main)](https://github.com/bossjones/apple-reminders-mcp/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/bossjones/apple-reminders-mcp/branch/main/graph/badge.svg)](https://codecov.io/gh/bossjones/apple-reminders-mcp)
[![Commit activity](https://img.shields.io/github/commit-activity/m/bossjones/apple-reminders-mcp)](https://img.shields.io/github/commit-activity/m/bossjones/apple-reminders-mcp)
[![License](https://img.shields.io/github/license/bossjones/apple-reminders-mcp)](https://img.shields.io/github/license/bossjones/apple-reminders-mcp)

A Model Context Protocol (MCP) server that provides programmatic access to Apple Reminders through FastMCP. This server allows you to create, read, list, and delete reminders using AppleScript integration.

- **Github repository**: <https://github.com/bossjones/apple-reminders-mcp/>
- **Documentation** <https://bossjones.github.io/apple-reminders-mcp/>

## Features

- **Create Reminders**: Add new reminders with due dates, times, notes, and locations
- **Get Reminders**: Retrieve reminders from specific lists (completed or pending)
- **List Reminder Lists**: View all available reminder lists
- **Delete Reminders**: Remove reminders by name from specific lists or all lists
- **CLI Interface**: Command-line tools for version, dependencies, and diagnostics

## Prerequisites

- macOS (required for Apple Reminders and AppleScript)
- Python 3.7+
- Apple Reminders app
- [uv](https://github.com/astral-sh/uv) for dependency management

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bossjones/apple-reminders-mcp.git
cd apple-reminders-mcp
```

2. Set up the development environment:
```bash
make install
```

This will:
- Create a virtual environment with uv
- Install all dependencies
- Set up pre-commit hooks
- Generate the `uv.lock` file

3. Create a `.env` file in the project root (optional):
```env
LOG_LEVEL=INFO
ENV=development
```

## Usage

### Running the MCP Server

```bash
uv run python -m apple_reminders_mcp.server
```

The server will start and provide MCP tools for interacting with Apple Reminders.

### CLI Interface

The project includes a command-line interface:

```bash
# Show version information
uv run python -m apple_reminders_mcp --version

# Show dependencies
uv run python -m apple_reminders_mcp deps

# Run diagnostics
uv run python -m apple_reminders_mcp diag
```

### Available MCP Tools

#### 1. Create Reminder

Create a new reminder with specified details.

**Parameters:**
- `title` (required): The title of the reminder
- `due_date` (required): Due date as datetime.date object
- `due_time` (optional): Due time in HHMMSS format (default: 09:00:00)
- `notes` (optional): Additional notes for the reminder
- `list_name` (optional): Target list name (default: "Reminder Created using Agent")
- `location` (optional): Location for location-based reminders

**Example:**
```python
await create_reminder(
    title="Team Meeting",
    due_date=datetime.date(2024, 12, 25),
    due_time="143000",  # 2:30 PM
    notes="Discuss Q4 goals",
    list_name="Work"
)
```

#### 2. Get Reminders

Retrieve reminders from a specific list.

**Parameters:**
- `list_name` (required): The name of the reminder list
- `completed` (optional): Whether to fetch completed reminders (default: False)
- `limit` (optional): Maximum number of reminders to return (default: 20)

**Example:**
```python
await get_reminder(
    list_name="Work",
    completed=False,
    limit=10
)
```

**Returns:** JSON array of reminders with name, body, due_date, and completed status.

#### 3. List Reminder Lists

Get all available reminder lists.

**Example:**
```python
await list_reminder_lists()
```

**Returns:** JSON array of list names.

#### 4. Delete Reminder

Delete a reminder by name.

**Parameters:**
- `name` (required): The exact name of the reminder to delete
- `list_name` (optional): Specific list to search in (searches all lists if not provided)

**Example:**
```python
await delete_reminder(
    name="Team Meeting",
    list_name="Work"
)
```

## Development

### Essential Commands

- `make install` - Set up virtual environment with uv and pre-commit hooks
- `make check` - Run comprehensive code quality checks (pre-commit, pyright, deptry)
- `make test` - Run pytest with coverage reporting
- `make build` - Build wheel distribution
- `make docs` - Build and serve MkDocs documentation

### Quality Assurance

- **Linting**: `uv run pre-commit run -a`
- **Type checking**: `uv run pyright src`
- **Testing**: `uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml`
- **Dependency check**: `uv run deptry src`

## Architecture

The server uses:
- **FastMCP**: For creating the MCP server and exposing tools
- **AppleScript**: For interacting with the Apple Reminders app
- **Pydantic**: For configuration management and validation
- **Loguru**: For structured, thread-safe logging
- **AsyncTyper**: For the command-line interface
- **subprocess**: For executing AppleScript commands

### Project Structure

```
src/apple_reminders_mcp/
├── __init__.py
├── server.py          # FastMCP server with Apple Reminders tools
├── cli.py             # Command-line interface
├── env.py             # Pydantic-based settings management
├── logger_config/     # Thread-safe logging infrastructure
└── utils/             # Utility functions and helpers
```

## Error Handling

- All functions include try-catch blocks for error handling
- AppleScript errors are captured and returned as formatted error messages
- JSON responses include error fields when operations fail
- Thread-safe logging with sensitive data obfuscation

## Limitations

- Only works on macOS due to AppleScript dependency
- Requires Apple Reminders app to be installed
- Location-based reminders may require additional permissions
- Date/time formatting must match AppleScript expectations

## Security Considerations

- The server runs locally by default
- Uses Pydantic SecretStr for sensitive configuration values
- No authentication is implemented - add authentication if exposing externally
- AppleScript commands are constructed with user input - ensure proper sanitization in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `make check`
5. Test thoroughly: `make test`
6. Submit a pull request

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
