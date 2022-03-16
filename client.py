# Importar la libreria del socket
import socket
import hashlib
import threading
SIZE = 2048
cn = 5
FORMAT = "utf-8"
PORT = 12345
# socket.AF_INET define la familia de protocolos IPv4. Socket.SOCK_STREAM define la conexión TCP.
concurrent_clients = int(input("Escriba el número de clientes que desea tener: "))
clients = concurrent_clients


def on_create_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Modificar direccion del servidor
    host = "192.168.85.1"  # "192.168.1.2" # server address "localhost", 9879 # Tomas: 192.168.85.1"
    port = PORT  # server port

    s.connect((host, port))
    print("Conectado")

    print("Numero de bytes recibidos", s.recv(SIZE))

    # Numero de los clientes conectados
    i = 0
    filename = "ArchivosRecibidos/Cliente" + str(i) + "-Prueba-" + str(clients)
    hash_data = s.recv(SIZE)
    print(str(i) + "HASH recibido: " + hash_data.decode(FORMAT))
    file = s.recv(SIZE)
    print(file)
    file = s.recv(SIZE)
    print(file)
    file = s.recv(SIZE)
    print(file)
    i += 1

    with open(filename, 'w') as f:
        f.write('Hola mundo\n')

    s.close()


class ClientThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_ID = thread_id

    def run(self):
        on_create_client()


while concurrent_clients > 0:
    thread = ClientThread(concurrent_clients)
    thread.start()
    concurrent_clients = concurrent_clients - 1

