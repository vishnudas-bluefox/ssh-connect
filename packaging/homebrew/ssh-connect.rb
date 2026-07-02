class SshConnect < Formula
  desc "Named SSH connection manager"
  homepage "https://github.com/vishnudas-bluefox/ssh-connect"
  url "https://github.com/vishnudas-bluefox/ssh-connect/archive/refs/tags/v0.1.0.tar.gz"
  version "0.1.0"
  sha256 "6eff86bb64c1ee596f83a2b6b0bfcbfd57619d4bcfef570e4b02ec5e14b32a94"
  license "MIT"
  head "https://github.com/vishnudas-bluefox/ssh-connect.git", branch: "main"

  depends_on "python@3.12"

  def install
    libexec.install "ssh_connect"
    (lib/"ssh-connect").install_symlink libexec
    (bin/"ssh-connect").install "bin/ssh-connect"
  end

  test do
    assert_match "ssh-connect 0.1.0", shell_output("#{bin}/ssh-connect --version")
  end
end
