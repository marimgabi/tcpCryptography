from email import message
import socket, sys
import tqdm
import os
import hashlib
from Crypto.Cipher import AES
import ssl

SEPARATOR = "<SEPARATOR>"
#BUFFER_SIZE = int(sys.argv[2])
BUFFER_SIZE = 1000



#Endereço ip e porta do server
host = "localhost"
#host = "10.81.68.251"
port = 5001

# arquivo a se enviado
#filename = "teste.txt"
filename = sys.argv[1]
# tamanho do arquivo
filesize = os.path.getsize(filename)
blocos = 0

# criando o socket do client
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

KEY = s.recv(BUFFER_SIZE)
#print(f"KEY {bytes_read}")

IV = b"abcdefghijklmnop"
#Objeto para encriptação
obj_enc = AES.new(KEY, AES.MODE_CFB, IV)
#Objeto para decriptação
obj_dec = AES.new(KEY, AES.MODE_CFB, IV)

# enviando o nome do arquivo e o tamanho
message = f"{filename}{SEPARATOR}{filesize}"
message_enc = obj_enc.encrypt(message.encode('utf-8'))
s.send(message_enc)
blocos += 1

# enviando o arquivo
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # lendo bytes do arquivo
        bytes_read = f.read(BUFFER_SIZE)
        message_enc = obj_enc.encrypt(bytes_read)
        if not bytes_read:
            # se acabou de transmitir os bytes do arquivo
            break
        # sendall para garantir a transmissão
        s.sendall(message_enc)
        blocos += 1
        # atualização da barra de progresso
        progress.update(len(bytes_read))
# fecha o socket
s.close()
print(f"Quantidade de blocos enviados: {blocos}")