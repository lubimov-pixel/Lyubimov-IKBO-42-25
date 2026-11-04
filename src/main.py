"""Command-line configuration and startup for the shell emulator."""

import argparse
from pathlib import Path

from shell import Shell
from vfs import VFS


def run_script(shell, path):
    """Execute commands from a script while echoing the interaction."""
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"script error: {exc}")
        return False
    success = True
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        print(f"{shell.prompt}{line}")
        if not shell.execute(line):
            print(f"script error: line {number}")
            success = False
        if not shell.running:
            break
    return success


def main():
    """Parse configuration, execute startup commands, and start REPL."""
    parser = argparse.ArgumentParser(description="UNIX shell emulator")
    parser.add_argument("--vfs", help="VFS directory on the host")
    parser.add_argument("--script", help="startup script containing commands")
    parser.add_argument("--no-interactive", action="store_true")
    args = parser.parse_args()
    print(f"[debug] vfs = {args.vfs or '<default>'}")
    print(f"[debug] script = {args.script or '<not set>'}")
    print(f"[debug] no_interactive = {args.no_interactive}")
    name = Path(args.vfs).name if args.vfs else "default"
    try:
        vfs = VFS(args.vfs)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"VFS error: {exc}\n")
    shell = Shell(name, vfs)
    message = vfs.motd()
    if message:
        print(message, end="" if message.endswith("\n") else "\n")
    if args.script:
        run_script(shell, args.script)
    if shell.running and not args.no_interactive:
        shell.repl()


if __name__ == "__main__":
    main()
