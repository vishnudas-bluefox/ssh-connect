#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v dpkg-buildpackage >/dev/null 2>&1; then
  echo "dpkg-buildpackage not found."
  echo "Install on Ubuntu/Debian: sudo apt install build-essential debhelper devscripts"
  exit 1
fi

chmod +x debian/rules

# Build unsigned .deb in parent directory.
dpkg-buildpackage -us -uc -b

echo ""
echo "Built package(s) in $(dirname "$ROOT"):"
ls -1 ../*.deb 2>/dev/null || true
echo ""
echo "Install locally:"
echo "  sudo apt install ../ssh-connect_*.deb"
