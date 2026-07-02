# Packaging

How to publish **ssh-connect** via Homebrew and apt.

## Homebrew (macOS / Linux)

Homebrew formulas for third-party tools live in a **tap** — a separate GitHub repo with a `Formula/` directory.

### 1. Tag a release

```bash
git tag v0.1.0
git push origin v0.1.0
```

Create a GitHub release for `v0.1.0` (optional but recommended).

### 2. Update the formula checksum

```bash
curl -L https://github.com/vishnudas-bluefox/ssh-connect/archive/refs/tags/v0.1.0.tar.gz | shasum -a 256
```

Put the hash in `packaging/homebrew/ssh-connect.rb` (`sha256 "..."`).

### 3. Create a tap repo

```bash
# On GitHub, create: vishnudas-bluefox/homebrew-tap
mkdir -p homebrew-tap/Formula
cp packaging/homebrew/ssh-connect.rb homebrew-tap/Formula/ssh-connect.rb
cd homebrew-tap
git init && git add . && git commit -m "Add ssh-connect formula"
git remote add origin git@github.com:vishnudas-bluefox/homebrew-tap.git
git push -u origin main
```

### 4. Users install with

```bash
brew install vishnudas-bluefox/tap/ssh-connect
```

Or tap once:

```bash
brew tap vishnudas-bluefox/tap
brew trust vishnudas-bluefox/tap
brew install ssh-connect
```

Homebrew may require `brew trust` for third-party taps. See https://docs.brew.sh/Tap-Trust

### Getting into homebrew-core

That requires significant adoption and review. Start with your own tap; migrate later if the tool gains traction.

---

## apt (Debian / Ubuntu)

There are three practical levels, from fastest to broadest reach.

### Option A — Direct `.deb` install (fastest)

Build on Ubuntu/Debian:

```bash
sudo apt install build-essential debhelper devscripts
./scripts/build-deb.sh
sudo apt install ../ssh-connect_0.1.0-1_all.deb
```

Upload the `.deb` to GitHub Releases. Users install with:

```bash
curl -LO https://github.com/vishnudas-bluefox/ssh-connect/releases/download/v0.1.0/ssh-connect_0.1.0-1_all.deb
sudo apt install ./ssh-connect_0.1.0-1_all.deb
```

### Option B — Personal Package Archive (PPA) on Launchpad

Best for `apt install ssh-connect` on Ubuntu without manual `.deb` downloads.

1. Create a Launchpad account: https://launchpad.net
2. Create a PPA: https://launchpad.net/~vishnudas-bluefox/+archive/ubuntu/ssh-connect
3. Upload the source:

```bash
# Install tools
sudo apt install build-essential debhelper devscripts dput

# Build source package
cd /path/to/ssh-connect
debuild -S -sa

# Upload to PPA (replace with your PPA name)
dput ppa:vishnudas-bluefox/ssh-connect ../ssh-connect_0.1.0-1_source.changes
```

4. Users add the PPA and install:

```bash
sudo add-apt-repository ppa:vishnudas-bluefox/ssh-connect
sudo apt update
sudo apt install ssh-connect
```

### Option C — Official Debian/Ubuntu archive

Requires sponsoring, policy compliance, and a long review. Only worth it after sustained adoption.

### Option D — Self-hosted apt repository

For teams or CI, host your own `apt` repo with `reprepro` or `aptly`:

```bash
# After building .deb
reprepro includedeb stable ../ssh-connect_0.1.0-1_all.deb
```

Users add your repo GPG key and `sources.list` entry.

---

## Release checklist

1. Bump version in `pyproject.toml`, `ssh_connect/__init__.py`, `debian/changelog`, and the Homebrew formula
2. Update `CHANGELOG.md`
3. Tag `vX.Y.Z` and push
4. Run `./scripts/build-deb.sh` on Ubuntu
5. Update Homebrew formula `url`, `version`, and `sha256`
6. Publish GitHub Release with `.deb` attached
7. Push updated formula to `homebrew-tap`
8. Upload to PPA (if using Launchpad)
