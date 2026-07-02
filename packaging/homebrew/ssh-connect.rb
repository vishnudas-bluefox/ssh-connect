class SshConnect < Formula
  desc "Named SSH connection manager"
  homepage "https://github.com/vishnudas-bluefox/ssh-connect"
  url "https://github.com/vishnudas-bluefox/ssh-connect/archive/refs/tags/v0.1.1.tar.gz"
  version "0.1.1"
  sha256 "72450df3af64114690366e7f6c173ea7861162114d7d19603d28d19ff8f9f9d3"
  license "MIT"
  head "https://github.com/vishnudas-bluefox/ssh-connect.git", branch: "main"

  depends_on "python@3.12"

  def install
    libexec.install "ssh_connect"
    (lib/"ssh-connect").install_symlink libexec
    (bin/"ssh-connect").install "bin/ssh-connect"
  end

  test do
    assert_match "ssh-connect 0.1.1", shell_output("#{bin}/ssh-connect --version")
  end
end
