sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt upgrade

export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"

sudo apt install python3.11 -y
sudo apt install build-essential -y
sudo apt install python3.11-dev -y
sudo apt-get install libopenblas-dev -y
sudo apt-get install python3.11-dev default-libmysqlclient-dev libmysqlclient-dev build-essential -y

python3.11 get-pip.py

pip3.11 install --upgrade setuptools
pip3.11 install --upgrade setuptools-scm
pip3.11 install --upgrade wheel

pip3.11 install -r requeriments_base.txt  --break-system-packages --no-cache-dir
pip3.11 install -r requeriments_torch.txt --break-system-packages --no-cache-dir
pip3.11 install -r requeriments_ultralytics.txt --break-system-packages --no-cache-dir



