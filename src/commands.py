"""Read-only UNIX-like commands for the in-memory filesystem."""

import getpass
import os

from vfs import VFS


class CommandError(ValueError):
    """Represent an invalid command argument or filesystem operation."""


def resolve(shell, argument):
    """Resolve a command argument to an absolute virtual path."""
    return VFS.normalize(argument, shell.cwd)


def command_ls(shell, args):
    """List the children of a virtual directory or name a single file."""
    if len(args) > 1:
        raise CommandError("ls: expected at most one path")
    path = resolve(shell, args[0] if args else ".")
    node = shell.vfs.lookup(path)
    if node.directory:
        print("  ".join(sorted(node.children)))
    else:
        print(path.rsplit("/", 1)[-1])


def command_cd(shell, args):
    """Change the current virtual working directory."""
    if len(args) > 1:
        raise CommandError("cd: expected at most one path")
    path = resolve(shell, args[0] if args else "/")
    node = shell.vfs.lookup(path)
    if not node.directory:
        raise NotADirectoryError(path)
    shell.cwd = path


def read_text(shell, filename):
    """Read a virtual file as UTF-8, replacing invalid characters."""
    path = resolve(shell, filename)
    node = shell.vfs.lookup(path)
    if node.directory:
        raise IsADirectoryError(path)
    return node.data.decode("utf-8", errors="replace")


def command_cat(shell, args):
    """Print the contents of one or more virtual files."""
    if not args:
        raise CommandError("cat: expected a file path")
    for name in args:
        value = read_text(shell, name)
        print(value, end="" if value.endswith("\n") else "\n")


def command_who(shell, args):
    """Show the host's current user as a simple login entry."""
    if args:
        raise CommandError("who: no arguments expected")
    user = getpass.getuser()
    print(f"{user}  console  (host: {os.name})")


def command_uniq(shell, args):
    """Remove consecutive duplicate lines from one virtual text file."""
    if len(args) != 1:
        raise CommandError("uniq: expected one file path")
    lines = read_text(shell, args[0]).splitlines()
    previous = None
    for line in lines:
        if line != previous:
            print(line)
        previous = line
