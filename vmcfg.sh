#!/usr/bin/bash

sudo ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
sudo dpkg-reconfigure -f noninteractive tzdata

sudo apt-get update\
    && sudo apt-get install -y curl git emacs

## Git:
git config --global user.name "Ricardo Alves Brandao"
git config --global user.email "rbrandao22@gmail.com"

## Docker:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
