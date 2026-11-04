"""Unit tests for filesystem loading and virtual mutations."""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shell import Shell
from vfs import VFS


class VFSTests(unittest.TestCase):
    """Verify source preservation, commands and physical reset."""

    def execute(self, shell, command):
        """Capture a command's result without depending on host output."""
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            ok = shell.execute(command)
        return ok, output.getvalue()

    def test_command_sequence(self):
        """Test navigation, cat, uniq and memory-only mutations."""
        with tempfile.TemporaryDirectory() as root:
            source = Path(root)
            (source / "docs").mkdir()
            text = source / "docs" / "data.txt"
            text.write_text("a\na\nb\n", encoding="utf-8")
            shell = Shell("test", VFS(source))
            self.assertTrue(self.execute(shell, "cd docs")[0])
            self.assertEqual(shell.cwd, "/docs")
            self.assertEqual(self.execute(shell, "uniq data.txt")[1],
                             "a\nb\n")
            self.assertTrue(self.execute(shell, "mkdir tmp")[0])
            self.assertFalse((source / "docs" / "tmp").exists())
            self.assertTrue(self.execute(shell, "rm data.txt")[0])
            self.assertTrue(text.exists())
            self.assertFalse(self.execute(shell, "cat data.txt")[0])

    def test_reset_clears_explicit_source(self):
        """Reset must clear the host source only when explicitly requested."""
        with tempfile.TemporaryDirectory() as root:
            original = Path(root) / "data.txt"
            original.write_text("content", encoding="utf-8")
            shell = Shell("test", VFS(root))
            self.assertTrue(self.execute(shell, "vfs-init")[0])
            self.assertFalse(original.exists())
            self.assertIn("motd", shell.vfs.root.children)

    def test_errors(self):
        """Reject missing files and directory removal."""
        shell = Shell()
        self.assertFalse(self.execute(shell, "rm /home")[0])
        self.assertFalse(self.execute(shell, "cd /missing")[0])
        self.assertFalse(self.execute(shell, 'ls "broken')[0])
        self.assertTrue(self.execute(shell, "mkdir /new")[0])
        self.assertFalse(self.execute(shell, "mkdir /new")[0])

    def test_motd(self):
        """Read an optional message of the day."""
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / "motd").write_text("hello", encoding="utf-8")
            self.assertEqual(VFS(root).motd(), "hello")
