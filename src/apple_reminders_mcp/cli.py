# pylint: disable=no-name-in-module
"""apple_reminders_mcp.cli"""

# pyright: reportMissingTypeStubs=false
# pylint: disable=no-member
# pylint: disable=no-value-for-parameter
# pylint: disable=no-name-in-module
# SOURCE: https://github.com/tiangolo/typer/issues/88#issuecomment-1732469681
from __future__ import annotations

# main.py or boss-bot application entry point
from apple_reminders_mcp.logging import early_init

# 🔥 STEP 1: Call early_init() FIRST - before ANY other imports
early_init()

import asyncio
import inspect
import json
import logging
import os
import signal
import subprocess
import sys
import tempfile
import traceback
import typing
from collections.abc import Awaitable, Callable, Iterable, Sequence
from enum import Enum
from functools import partial, wraps
from importlib import import_module, metadata
from importlib.metadata import version as importlib_metadata_version
from pathlib import Path
from re import Pattern
from types import FrameType
from typing import TYPE_CHECKING, Annotated, Any, Dict, List, NoReturn, Optional, Set, Tuple, Type, Union

import bpdb
import pysnooper
import rich
import typer
from rich.console import Console

import apple_reminders_mcp
from apple_reminders_mcp.__version__ import __version__

# 🔥 STEP 3: Configure full logging features after imports
from apple_reminders_mcp.env import McpSettings
from apple_reminders_mcp.logging import setup_apple_reminders_mcp_logging
from apple_reminders_mcp.utils.asynctyper import AsyncTyper

# Initialize boss-bot settings
settings = McpSettings()

# Configure logging with boss-bot integration
LOGGER = setup_apple_reminders_mcp_logging(settings)


# Set up logging
# LOGGER = logging.getLogger(__name__)

APP = AsyncTyper()
console = Console()
cprint = console.print


# Load existing subcommands
def load_commands(directory: str = "subcommands"):
    script_dir = Path(__file__).parent
    subcommands_dir = script_dir / directory

    # Check if subcommands directory exists
    if not subcommands_dir.exists():
        LOGGER.debug(f"Subcommands directory {subcommands_dir} does not exist, skipping")
        return

    LOGGER.info(f"Loading subcommands from {subcommands_dir}")

    try:
        for filename in os.listdir(subcommands_dir):
            if filename.endswith("_cmd.py"):
                module_name = f"{__name__.split('.')[0]}.{directory}.{filename[:-3]}"
                module = import_module(module_name)
                if hasattr(module, "app"):
                    APP.add_typer(module.app, name=filename[:-7])
    except Exception as e:
        LOGGER.error(f"Error loading subcommands: {e}")


def version_callback(version: bool) -> None:
    """Print the version of apple_reminders_mcp."""
    if version:
        rich.print(f"apple_reminders_mcp version: {__version__}")
        raise typer.Exit()


@APP.command()
def version() -> None:
    """Version command"""
    rich.print(f"apple_reminders_mcp version: {__version__}")


@APP.command()
def deps() -> None:
    """Deps command"""
    rich.print(f"apple_reminders_mcp version: {__version__}")
    rich.print(f"langchain_version: {importlib_metadata_version('langchain')}")
    rich.print(f"langchain_community_version: {importlib_metadata_version('langchain_community')}")
    rich.print(f"langchain_core_version: {importlib_metadata_version('langchain_core')}")
    rich.print(f"langchain_openai_version: {importlib_metadata_version('langchain_openai')}")
    rich.print(f"langchain_text_splitters_version: {importlib_metadata_version('langchain_text_splitters')}")
    rich.print(f"chromadb_version: {importlib_metadata_version('chromadb')}")
    rich.print(f"langsmith_version: {importlib_metadata_version('langsmith')}")
    rich.print(f"pydantic_version: {importlib_metadata_version('pydantic')}")
    rich.print(f"pydantic_settings_version: {importlib_metadata_version('pydantic_settings')}")
    rich.print(f"ruff_version: {importlib_metadata_version('ruff')}")


@APP.command()
def about() -> None:
    """About command"""
    typer.echo("This is BossBot CLI")


@APP.command()
def show() -> None:
    """Show command"""
    cprint("\nShow apple_reminders_mcp", style="yellow")


@APP.command()
def logtree() -> None:
    """Display the current logging hierarchy using logging_tree"""
    try:
        from logging_tree import printout

        cprint("\n[bold blue]📊 Logging Tree Hierarchy[/bold blue]", style="bold blue")
        cprint("=" * 50, style="blue")
        cprint("")
        printout()
        cprint("")
        cprint("[dim]This shows the current logger hierarchy and configuration[/dim]")
    except ImportError:
        cprint("[red]❌ logging_tree is not installed[/red]")
        cprint("[yellow]Install with: pip install logging-tree[/yellow]")
        raise typer.Exit(1)


@APP.command()
def go() -> None:
    """Main entry point for Apple Reminders MCP"""
    typer.echo("Starting up Apple Reminders MCP Server")
    # TODO: Implement server startup logic
    cprint("[yellow]Server startup not yet implemented[/yellow]")


def handle_sigterm(signo: int, frame: FrameType | None) -> NoReturn:
    """Handle SIGTERM signal by exiting with the appropriate status code.

    Args:
        signo: The signal number received
        frame: The current stack frame (may be None)

    Returns:
        Never returns, always exits
    """
    sys.exit(128 + signo)  # this will raise SystemExit and cause atexit to be called


signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == "__main__":
    APP()
