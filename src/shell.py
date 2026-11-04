"""Interactive shell entry point and execution loop."""

from parser import ParseError, parse_command
from vfs import VFS
from commands import (
    CommandError, command_cat, command_cd, command_ls,
    command_mkdir, command_rm, command_uniq, command_who,
)


class Shell:
    """Provide a simple REPL with initially stubbed commands."""

    def __init__(self, vfs_name="default", vfs=None):
        self.vfs_name = vfs_name
        self.running = True
        self.vfs = vfs if vfs is not None else VFS()
        self.cwd = "/"

    @property
    def prompt(self):
        """Return the current command prompt."""
        return f"{self.vfs_name}:{self.cwd}$ "

    def execute(self, line):
        """Execute one command and report success or failure."""
        try:
            parts = parse_command(line)
        except ParseError as exc:
            print(f"parse error: {exc}")
            return False
        if not parts:
            return True
        name, *args = parts
        if name == "exit":
            if args:
                print("exit: too many arguments")
                return False
            self.running = False
        elif name == "vfs-init":
            if args:
                print("vfs-init: no arguments expected")
                return False
            try:
                self.vfs.reset()
                self.cwd = "/"
                print("VFS reset to default")
            except (OSError, ValueError) as exc:
                print(f"vfs-init: {exc}")
                return False
        elif name in COMMANDS:
            try:
                COMMANDS[name](self, args)
            except (CommandError, OSError, ValueError) as exc:
                print(f"error: {exc}")
                return False
        else:
            print(f"{name}: command not found")
            return False
        return True

    def repl(self):
        """Read commands until exit or end of input."""
        while self.running:
            try:
                line = input(self.prompt)
            except (EOFError, KeyboardInterrupt):
                print()
                break
            self.execute(line)


def main():
    """Start the initial interactive shell."""
    Shell().repl()


if __name__ == "__main__":
    main()


COMMANDS = {
    "ls": command_ls,
    "cd": command_cd,
    "cat": command_cat,
    "who": command_who,
    "uniq": command_uniq,
    "mkdir": command_mkdir,
    "rm": command_rm,
}
