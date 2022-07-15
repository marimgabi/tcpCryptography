from email import message
import socket, sys
import tqdm
import os
import pickle
from datetime import datetime
from defs import *

# endereço ip
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

BUFFER_SIZE = 1000
SEPARATOR = "<SEPARATOR>"
blocos = 0

#generateKeys() #tem que ser executada uma vez para gerar as chaves

#carrega as chaves dos arquivos na pasta keys/
publicKey, privateKey = loadKeys()

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

#envia a chave pública para o cliente
pks = f"{loadPKasString()}"
client_socket.send(pks.encode('utf-8'))
# se executar é pq o remetente está conectado
tstart = datetime.now()
print(f"[+] {address} is connected.")

# recebe as informações o arquivo
# recebe usando o socket do client
received = client_socket.recv(BUFFER_SIZE)
messageDec = rsa.decrypt(received, privateKey).decode()
blocos += 1
filename, filesize = messageDec.split(SEPARATOR)
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
        bytesArray = bytearray(bytes_read)
        inicio = 0
        fim = 128
        for i in range(7):
            aux = bytesArray[inicio:fim]
            # print(len(aux))
            # print(aux)
            #decripta a mensagem
            messageDec = rsa.decrypt(aux, privateKey)
            # escreve no arquivo os bytes recebidos
            f.write(messageDec)
            inicio+=128
            fim+=128
        if not bytes_read:
            #se não recebe nada é pq já recebeu tudo
            break
        blocos += 1
        # atualiza a barra de progresso
        progress.update(len(bytes_read))

# fecha o socket do client e do server
client_socket.close()
s.close()
tend = datetime.now()
print (f"\nTempo total de transmissão: {tend - tstart}")
print(f"Quantidade de blocos recebidos: {blocos}")
