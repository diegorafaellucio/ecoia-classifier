sudo apt install build-essential -y
sudo apt install python3.11-dev -y

sudo apt-get install python3-dev default-libmysqlclient-dev build-essential -y

pip3.11 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --break-system-packages --user
pip3.11 install -r requeriments.txt --break-system-packages

