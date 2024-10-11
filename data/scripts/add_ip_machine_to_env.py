import socket
from dotenv import load_dotenv, set_key
import os 
import argparse
import socket

def get_local_ip():
    try:
        # Cria uma conexão fictícia para determinar o IP da rede local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Tenta se conectar a um endereço IP público (Google DNS, por exemplo)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return f"Erro ao obter o IP: {e}"

env_file = '../../.env'

if os.path.exists(env_file):
    load_dotenv(env_file)

ip_address = get_local_ip()

set_key(env_file,'DB_HOST',ip_address)

