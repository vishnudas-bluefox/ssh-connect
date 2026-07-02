# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2026-07-02

### Added

- GitHub Actions workflow to build and publish `.deb` on tagged releases
- One-line install scripts: `scripts/install-brew.sh` and `scripts/install-deb.sh`
- Homebrew formula template in `packaging/homebrew/ssh-connect.rb`
- Debian packaging for apt (`.deb`) in `debian/` and `packaging/README.md`
- `scripts/build-deb.sh` to build Debian packages on Ubuntu/Debian
- MIT `LICENSE` for distribution

### Changed

- `bin/ssh-connect` wrapper resolves installed paths for brew/apt/Linuxbrew layouts

## [0.1.0] - 2026-07-02

### Added

- **ssh-connect CLI** — manage named SSH profiles and connect with a single command
- **Profile storage** — persist connections in `~/.config/ssh-connect/connections.json` (override with `SSH_CONNECT_CONFIG_DIR`)
- **Commands** — `add`, `rm`, `list`, `show`, and `connect` with shorthand `ssh-connect <name>`
- **Interactive and non-interactive add** — prompt for host, user, PEM path, and port, or pass flags directly
- **PEM key support** — resolve and validate private key paths; build `ssh -i` commands automatically
- **install.sh** — symlink `ssh-connect` into `~/.local/bin` and add it to PATH when needed
- **bin/ssh-connect wrapper** — run via system Python regardless of active virtualenv
