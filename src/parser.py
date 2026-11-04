"""Parse shell commands and expand variables from the host environment."""

import os
import shlex


class ParseError(ValueError):
    """Raised when a command cannot be parsed."""


def parse_command(line):
    """Split a command while expanding real environment variables."""
    expanded = os.path.expandvars(line)
    try:
        return shlex.split(expanded, posix=True)
    except ValueError as exc:
        raise ParseError(str(exc)) from exc
