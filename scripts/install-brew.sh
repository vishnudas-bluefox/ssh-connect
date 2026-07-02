#!/usr/bin/env bash
set -euo pipefail

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required. Install from https://brew.sh"
  exit 1
fi

FORMULA_URL="https://raw.githubusercontent.com/vishnudas-bluefox/ssh-connect/main/packaging/homebrew/ssh-connect.rb"

# Works immediately without a separate tap repo.
brew install "$FORMULA_URL"

echo ""
echo "Installed ssh-connect"
echo "Try: ssh-connect --version"
