#!/usr/bin/env bash

pipx install poetry
poetry install

cd /tmp/
curl -Lso pinniped https://get.pinniped.dev/v0.30.0/pinniped-cli-linux-amd64 \
  && chmod +x pinniped \
  && sudo mv pinniped /usr/local/bin/pinniped

wget https://github.com/aquasecurity/trivy/releases/download/v0.51.2/trivy_0.51.2_Linux-ARM64.deb
sudo dpkg -i trivy_0.51.2_Linux-ARM64.deb

curl -LO https://github.com/getsops/sops/releases/download/v3.8.1/sops-v3.8.1.linux.amd64 \
 && chmod +x sops-v3.8.1.linux.amd64  \
 && sudo mv sops-v3.8.1.linux.amd64 /usr/local/bin/sops
