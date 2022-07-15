import socket, sys
import tqdm
import os
from defs import *

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1000
#print(BUFFER_SIZE)

#Endereço ip e porta do server
host = "localhost"
#host = "10.81.68.251"
port = 5001

#publicKey, privateKey = loadKeys()

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

# recebe a chave pública para encriptar
received = s.recv(BUFFER_SIZE).decode('utf-8')
publicKey = rsa.PublicKey.load_pkcs1(received)

# enviando o nome do arquivo e o tamanho
message = f"{filename}{SEPARATOR}{filesize}"
messageEnc = rsa.encrypt(message.encode(), publicKey)
s.send(messageEnc)

#bufferContent = b''
bufferContent = bytearray()
blocos += 1

# enviando o arquivo
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        while len(bufferContent)<896:
            # lendo bytes do arquivo
            bytes_read = f.read(117)
            messageEnc = rsa.encrypt(bytes_read, publicKey)   
            bufferContent+=messageEnc
            if not bytes_read:
                # se acabou de transmitir os bytes do arquivo
                break
        while len(bufferContent)<1000:
            bufferContent+=b'0'
        # sendall para garantir a transmissão
        # print(bufferContent)
        s.sendall(bufferContent)
        blocos += 1
        #limpeza do buffer
        bufferContent=b''
        # atualização da barra de progresso
        progress.update(len(bytes_read))
# fecha o socket
s.close()
print(f"Quantidade de blocos enviados: {blocos}")