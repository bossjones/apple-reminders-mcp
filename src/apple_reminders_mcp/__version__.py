"""A module for storing version number."""

from __future__ import annotations

import sys
from importlib.metadata import version

__version__ = version("apple-reminders-mcp")
__version_info__ = tuple(map(int, __version__.split(".")))

PYENV = sys.version_info
