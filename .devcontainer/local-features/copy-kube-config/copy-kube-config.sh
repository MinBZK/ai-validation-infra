#!/bin/bash -i

# Copies localhost's ~/.kube/config file into the container and swap out localhost
# for host.docker.internal whenever a new shell starts to keep them in sync.
if [ -d "/usr/local/share/kube-localhost" ]; then
    mkdir -p $HOME/.kube
    sudo cp -r /usr/local/share/kube-localhost/* $HOME/.kube
    sudo chown -R $(id -u) $HOME/.kube
    sed -i -e "s/localhost/host.docker.internal/g" $HOME/.kube/config
    sed -i -e "s/127.0.0.1/host.docker.internal/g" $HOME/.kube/config
fi


if [ -d "/usr/local/share/pinniped-localhost/" ]; then
    mkdir -p $HOME/.config/pinniped/
    sudo cp -r /usr/local/share/pinniped-localhost/* $HOME/.config/pinniped/
    sudo chown -R $(id -u) $HOME/.config/pinniped/
fi
