#!/bin/bash

podman machine start
ssh -i ~/.ssh/podman-machine-default -R 10000:$(hostname):22 -p $(podman machine --log-level=debug ssh -- exit 2>&1 | grep Executing | awk {'print $8'}) core@localhost sshfs -p 10000 $USER@127.0.0.1:/Volumes/Projects /mnt/Projects&
sleep 10
podman create -t --name blocks-build -v /mnt/Projects/blocks:/blocks fedora
podman start blocks-build
podman exec blocks-build dnf install -y python3 python3-pip binutils
podman exec blocks-build pip install pyinstaller pygame
podman stop blocks-build
podman machine stop
