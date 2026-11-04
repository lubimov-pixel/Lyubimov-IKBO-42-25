#!/bin/sh
set -eu
cd "$(dirname "$0")/../.."
python3 src/main.py --no-interactive --script tests/startup/stage2.emu
