#!/usr/bin/env bash
# Taken from here (https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f)
# Install build tools
apt-get update
apt-get --assume-yes install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev

wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz
tar xf Python-3.6.4.tar.xz
cd Python-3.6.4
./configure
make
sudo make altinstall

