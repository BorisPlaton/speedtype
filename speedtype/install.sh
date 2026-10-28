#!/usr/bin/env bash

set -euo pipefail

SPEEDTYPE_URL="git+https://github.com/BorisPlaton/speedtype#subdirectory=speedtype"

echo "Installing 'speedtype'."

if ! command -v uv >/dev/null 2>&1; then
    echo "'uv' is missing. Installing 'uv'."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

uv tool install --reinstall --python 3.14 "$SPEEDTYPE_URL"

echo ""
echo "'speedtype' is installed!"
echo "If 'speedtype' is not found, restart your shell or run: uv tool update-shell"
echo "Run 'speedtype' to launch."
