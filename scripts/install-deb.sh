#!/usr/bin/env bash
set -euo pipefail

VERSION="${SSH_CONNECT_VERSION:-0.1.0}"
RELEASE_TAG="v${VERSION}"
DEB="ssh-connect_${VERSION}-1_all.deb"
REPO="vishnudas-bluefox/ssh-connect"
URL="https://github.com/${REPO}/releases/download/${RELEASE_TAG}/${DEB}"

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
