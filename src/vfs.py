"""In-memory filesystem populated from an optional host directory."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Node:
    """Represent a file or directory inside a virtual filesystem."""

    directory: bool
    data: bytes = b""
    children: dict = field(default_factory=dict)


class VFS:
    """Manage a file tree without persisting ordinary shell mutations."""

    def __init__(self, source=None):
        self.source = Path(source).resolve() if source else None
        self.root = self._read_source() if source else self._default_root()

    @staticmethod
    def _default_root():
        """Create the initial in-memory filesystem."""
        return Node(True, children={
            "motd": Node(False, b"Welcome to virtual shell!\n"),
            "home": Node(True),
            "tmp": Node(True),
        })

    def _read_source(self):
        """Read an existing directory into memory, rejecting symlinks."""
        if not self.source.is_dir():
            raise ValueError(f"VFS directory not found: {self.source}")
        return self._read_dir(self.source)

    def _read_dir(self, directory):
        """Recursively read a host directory without changing its files."""
        node = Node(True)
        for item in sorted(directory.iterdir()):
            if item.is_symlink():
                raise ValueError(f"symbolic links are not supported: {item}")
            if item.is_dir():
                node.children[item.name] = self._read_dir(item)
            elif item.is_file():
                node.children[item.name] = Node(False, item.read_bytes())
            else:
                raise ValueError(f"unsupported filesystem entry: {item}")
        return node

    @staticmethod
    def normalize(path, cwd="/"):
        """Resolve absolute and relative UNIX paths to canonical paths."""
        parts = [] if path.startswith("/") else cwd.strip("/").split("/")
        parts = [part for part in parts if part]
        for part in path.split("/"):
            if part in ("", "."):
                continue
            if part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)
        return "/" + "/".join(parts)

    def lookup(self, path):
        """Find a node by canonical path or raise a useful error."""
        node = self.root
        for part in path.strip("/").split("/") if path != "/" else []:
            if not node.directory:
                raise NotADirectoryError(path)
            if part not in node.children:
                raise FileNotFoundError(path)
            node = node.children[part]
        return node

    def parent(self, path):
        """Return the parent directory and filename of a canonical path."""
        if path == "/":
            raise ValueError("cannot modify root directory")
        folder, _, name = path.rpartition("/")
        node = self.lookup(folder or "/")
        if not node.directory:
            raise NotADirectoryError(folder)
        return node, name

    def motd(self):
        """Return the optional root motd as decoded UTF-8 text."""
        item = self.root.children.get("motd")
        if item is None or item.directory:
            return ""
        return item.data.decode("utf-8", errors="replace")

    def reset(self):
        """Reset virtual files and explicitly clear the source directory."""
        if self.source is not None:
            self._clear_disk()
        self.root = self._default_root()

    def _clear_disk(self):
        """Remove all children of the explicitly selected source directory."""
        source = self.source
        if source is None or source.is_symlink() or not source.is_dir():
            raise ValueError("unsafe VFS source")
        if source == Path(source.anchor) or source == Path.home():
            raise ValueError("refusing to reset a root or home directory")
        for item in source.iterdir():
            self._remove_disk_item(item)

    def _remove_disk_item(self, item):
        """Remove an entry without following directory symbolic links."""
        if item.is_symlink() or item.is_file():
            item.unlink()
        elif item.is_dir():
            for child in item.iterdir():
                self._remove_disk_item(child)
            item.rmdir()
        else:
            raise ValueError(f"cannot remove unknown file type: {item}")
