#!/usr/bin/env bash
set -euo pipefail

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required. Install from https://brew.sh"
  exit 1
fi

brew tap vishnudas-bluefox/tap
brew trust vishnudas-bluefox/tap
brew install ssh-connect

echo ""
echo "Installed ssh-connect"
echo "Try: ssh-connect --version"
