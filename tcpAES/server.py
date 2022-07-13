import socket, sys
import tqdm
import os
from datetime import datetime
import hashlib
from Crypto.Cipher import AES
import ssl

# endereço ip
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

#BUFFER_SIZE = int(sys.argv[1])
BUFFER_SIZE = 1000
SEPARATOR = "<SEPARATOR>"
blocos = 0
# criando socket do server
# TCP socket
s = socket.socket()

# ligando o socket ao endereço local
s.bind((SERVER_HOST, SERVER_PORT))

# (n) n-> número de conexões não aceitas permitidas
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# se existe conexão, aceita
client_socket, address = s.accept()

#Criando chave
KEY = hashlib.sha256(b"chega disso aqui").digest()
#print(f"chave {KEY}")

IV = b"abcdefghijklmnop"
#Objeto para encriptação
obj_enc = AES.new(KEY, AES.MODE_CFB, IV)
#Objeto para decriptação
obj_dec = AES.new(KEY, AES.MODE_CFB, IV)

#Envia chave para o cliente
client_socket.send(KEY)

# se executar é pq o remetente está conectado
tstart = datetime.now()
print(f"[+] {address} is connected.")

# recebe as informações o arquivo
# recebe usando o socket do client
received = client_socket.recv(BUFFER_SIZE)
message_dec = obj_dec.decrypt(received)
blocos += 1
filename, filesize = message_dec.decode('utf-8').split(SEPARATOR)
#print(f"filename: {filename} --- filesize: {filesize}")
# remove o caminho absoluto
#filename = os.path.basename(filename)
filename = "teste1.txt"

filesize = int(filesize)

# recebe o arquivo do socket e escreve no arquivo
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # lê 1024 bytes do socket
        bytes_read = client_socket.recv(BUFFER_SIZE)
        message_dec = obj_dec.decrypt(bytes_read)
        if not bytes_read:
            #se não recebe nada é pq já recebeu tudo
            break
        # escreve no arquivo os bytes recebidos
        f.write(message_dec)
        blocos += 1
        # atualiza a barra de progresso
        progress.update(len(bytes_read))

# fecha o socket do client e do server
client_socket.close()
s.close()
tend = datetime.now()
print (f"\nTempo total de transmissão: {tend - tstart}")
print(f"Quantidade de blocos recebidos: {blocos}")
