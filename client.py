# Importar la libreria del socket
import socket
import hashlib
SIZE = 2048
cn = 5
FORMAT = "utf-8"
PORT = 12345
# socket.AF_INET define la familia de protocolos IPv4. Socket.SOCK_STREAM define la conexión TCP.
concurrent_clients = int(input("Escriba el número de clientes que desea tener: "))
while concurrent_clients > 0:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Modificar direccion del servidor 
    host = "192.168.28.1"  # "192.168.1.2" # server address "localhost", 9879 # Tomas: 192.168.85.1"
    port = PORT  # server port

    s.connect((host, port))
    print("Conectado")
    s.close()
    concurrent_clients = concurrent_clients-1
print("Numero de bytes recibidos",  s.recv(SIZE))

# Numero de los clientes conectados
i = 0
filename = "ArchivosRecibidos/Cliente"+str(i)+"-Prueba-"+str(i)
file_size = s.recv(SIZE)
hash_data = s.recv(SIZE)
print(str(i)+"HASH recibido: "+hash_data.decode(FORMAT))

with open(filename, 'w') as f:
    f.write('Hola mundo\n')