# Importar la libreria del socket
import socket
import hashlib
SIZE = 2048
cn=5
FORMAT = "utf-8"

# socket.AF_INET define la familia de protocolos IPv4. Socket.SOCK_STREAM define la conexión TCP.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Modificar direccion del servidor 
host = "192.168.56.1" # "192.168.1.2" # server address "localhost", 9879
port =12345 #server port

s.connect((host,port))
print(s.recv(SIZE))
buf = bytearray( 30) # buffer criado
print("Numero de bytes ",s.recv_into(buf))

# Numero de los clientes conectados
i=0
filename = "ArchivosRecibidos/Cliente"+str(i)+"-Prueba-"+str(i)
sizefile = s.recv(SIZE)
dataHash = s.recv(SIZE)
print(str(i)+"hash:"+dataHash.decode(FORMAT))
        
print(buf)

with open(filename, 'w') as f:
    f.write('Hola mundo\n')

s.send(b"Hello Server")
s.close()