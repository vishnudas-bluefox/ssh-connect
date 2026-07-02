#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$ROOT/bin"
LINK_DIR="${HOME}/.local/bin"

chmod +x "$BIN_DIR/ssh-connect"
mkdir -p "$LINK_DIR"

ln -sf "$BIN_DIR/ssh-connect" "$LINK_DIR/ssh-connect"

case ":$PATH:" in
  *":$LINK_DIR:"*) ;;
  *)
    SHELL_RC=""
    if [[ -n "${ZSH_VERSION:-}" ]] || [[ "$SHELL" == *zsh* ]]; then
      SHELL_RC="${HOME}/.zshrc"
    elif [[ -n "${BASH_VERSION:-}" ]] || [[ "$SHELL" == *bash* ]]; then
      SHELL_RC="${HOME}/.bashrc"
    fi
    if [[ -n "$SHELL_RC" ]] && ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC" 2>/dev/null; then
      {
        echo ""
        echo "# ssh-connect CLI"
        echo 'export PATH="$HOME/.local/bin:$PATH"'
      } >> "$SHELL_RC"
      echo "Added ~/.local/bin to PATH in $SHELL_RC"
    fi
    ;;
esac

echo "Installed ssh-connect -> $LINK_DIR/ssh-connect"
echo ""
echo "Reload shell or run: export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "Example:"
echo "  ssh-connect add cp-sandbox --host 3.108.133.130 --user ubuntu --pem ~/Desktop/programs/clearprompt/server/clearprompt-sandbox.pem"
echo "  ssh-connect cp-sandbox"
