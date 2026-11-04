#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
python3 src/main.py --vfs tests/vfs/deep --no-interactive \
  --script tests/startup/stage3.emu
