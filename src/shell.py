"""Interactive shell entry point and execution loop."""

from parser import ParseError, parse_command


class Shell:
    """Provide a simple REPL with initially stubbed commands."""

    def __init__(self, vfs_name="default"):
        self.vfs_name = vfs_name
        self.running = True

    @property
    def prompt(self):
        """Return the current command prompt."""
        return f"{self.vfs_name}:/$ "

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
        elif name in {"ls", "cd"}:
            print(f"{name}: args={args}")
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
