#!/usr/bin/env bash
set -euo pipefail

RELEASE_TAG="${SSH_CONNECT_VERSION:-0.1.4}"
DEB="ssh-connect_0.1.2-1_all.deb"
REPO="vishnudas-bluefox/ssh-connect"
URL="https://github.com/${REPO}/releases/download/v${RELEASE_TAG}/${DEB}"

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This installer requires apt (Debian/Ubuntu)."
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading ${URL}"
curl -fsSL "$URL" -o "${TMP}/${DEB}"
sudo apt-get install -y "${TMP}/${DEB}"
echo ""
echo "Installed ssh-connect"
echo "Try: ssh-connect --version"
