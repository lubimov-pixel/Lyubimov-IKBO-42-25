#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
python3 src/main.py --no-interactive --vfs tests/vfs/simple \
  --script tests/startup/stage2.emu
