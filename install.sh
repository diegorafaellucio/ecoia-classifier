#!/bin/bash

# Add deadsnakes repo and update system
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt upgrade -y

# Set OpenSSL flags (if needed)
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"

# Install Python 3.11 and system dependencies
sudo apt install python3.11 -y
sudo apt install build-essential -y
sudo apt install python3.11-dev python3-dev -y
sudo apt-get install libopenblas-dev default-libmysqlclient-dev libmysqlclient-dev imagemagick -y

# Optionally install pip for python3.11 if needed
python3.11 get-pip.py

# Upgrade setuptools and wheel
pip3.11 install --upgrade setuptools setuptools-scm wheel

# Install Python requirements (classifier)
pip3.11 install -r requeriments_base.txt --break-system-packages --no-cache-dir
pip3.11 install -r requeriments_torch.txt --break-system-packages --no-cache-dir
pip3.11 install -r requeriments_ultralytics.txt --break-system-packages --no-cache-dir

# Install Python requirements (collector)
pip3.11 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --break-system-packages --user
pip3.11 install -r requeriments.txt --break-system-packages


# Collector-specific pip installs
pip3.11 install pypylon boto3 --break-system-packages
