# ssh-connect

Save SSH profiles by short name and connect with one command.

## Install

Share these one-liners with friends:

### Homebrew (macOS / Linux)

```bash
brew install https://raw.githubusercontent.com/vishnudas-bluefox/ssh-connect/main/packaging/homebrew/ssh-connect.rb
```

Or one-liner:

```bash
curl -fsSL https://raw.githubusercontent.com/vishnudas-bluefox/ssh-connect/main/scripts/install-brew.sh | bash
```

After you create the [homebrew-tap](https://github.com/vishnudas-bluefox/homebrew-tap) repo, this also works:

```bash
brew install vishnudas-bluefox/tap/ssh-connect
```

### apt (Debian / Ubuntu)

```bash
curl -fsSL https://raw.githubusercontent.com/vishnudas-bluefox/ssh-connect/main/scripts/install-deb.sh | bash
```

Manual `.deb` install:

```bash
curl -LO https://github.com/vishnudas-bluefox/ssh-connect/releases/download/v0.1.4/ssh-connect_0.1.2-1_all.deb
sudo apt install ./ssh-connect_0.1.2-1_all.deb
```

### Manual install

```bash
git clone https://github.com/vishnudas-bluefox/ssh-connect.git
cd ssh-connect
./install.sh
```

This links `ssh-connect` into `~/.local/bin` and adds that directory to your PATH if needed.

You can also run it directly without installing:

```bash
/path/to/ssh-connect/bin/ssh-connect list
```

## Usage

```bash
# Connect (shorthand)
ssh-connect cp-sandbox

# Same as above
ssh-connect connect cp-sandbox

# Add a new profile (interactive)
ssh-connect add cp-sandbox

# Add non-interactively
ssh-connect add my-server \
  --host 203.0.113.10 \
  --user ubuntu \
  --pem ~/.ssh/my-server.pem

# List profiles
ssh-connect list

# Show details + generated ssh command
ssh-connect show cp-sandbox

# Delete a profile
ssh-connect rm cp-sandbox
```

## Config

Profiles are stored in:

```
~/.config/ssh-connect/connections.json
```

Override with:

```bash
export SSH_CONNECT_CONFIG_DIR=/path/to/custom/dir
```

## Example

```bash
ssh-connect add my-server \
  --host 203.0.113.10 \
  --user ubuntu \
  --pem ~/.ssh/my-server.pem
```

Then connect with:

```bash
ssh-connect my-server
```

Which runs:

```bash
ssh -i ~/.ssh/my-server.pem ubuntu@203.0.113.10
```

## Packaging

To publish via Homebrew or apt, see [packaging/README.md](packaging/README.md).
