#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT
printf 'temporary data\n' > "$TEMP_DIR/test.txt"
python3 src/main.py --vfs "$TEMP_DIR" --no-interactive \
  --script tests/startup/reset.emu
if [ -e "$TEMP_DIR/test.txt" ]; then
  echo "ERROR: vfs-init did not clear physical VFS" >&2
  exit 1
fi
