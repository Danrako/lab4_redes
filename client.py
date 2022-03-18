# Importar la libreria del socket
import socket
import hashlib
import threading
import time
from socket import error
from datetime import datetime
SIZE = 2048
cn = 5
FORMAT = "utf-8"
PORT = 12345
# socket.AF_INET define la familia de protocolos IPv4. Socket.SOCK_STREAM define la conexión TCP.
concurrent_clients = int(input("Escriba el número de clientes que desea tener: "))
prueba = int(input("Escriba el número de la prueba que esta: "))
clients = concurrent_clients


def on_create_client(id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    t1 = time.time()
    # Modificar direccion del servidor
    host = "192.168.56.1" #"192.168.85.1"  # "192.168.1.2" # server address "localhost", 9879 # Tomas: 192.168.85.1"
    port = PORT  # server port

    s.connect((host, port))
    print("Conectado")
    i=0
    print("Numero de bytes recibidos", s.recv(SIZE))

    # Numero de los clientes conectados
    filename = "ArchivosRecibidos/Cliente" + str(id) + "-Prueba-" + str(prueba)+".txt"
    # Recibo 4 cosas
    # 1. El tamaño del archivo
    sizefile = s.recv(SIZE)
    file_size = sizefile.decode(FORMAT)
    
    # 2. La informacion del hash
    hash_data = s.recv(SIZE)
    print(str(i) + "HASH recibido: " + hash_data.decode(FORMAT))
    
    # 3. El archivo recuperado por paquetes
    send_bytes = 0
    packets = 0
    file = open(filename, "wb")
    conexion=False
    while True:
        try:
            input_data = s.recv(SIZE)
            packets+=1
            conexion=True
        except error:
            print ("Error de lectura")
            conexion=False
            break
        else:
            if input_data:
                # Compatibilidad con Python 3.
                if input_data.endswith(b"Termino:200"):
                    #data+=input_data.replace(b"Termino:200",b"")
                    file.write(input_data.replace(b"Termino:200",b""))
                    file.close()
                    send_bytes+=len(input_data.replace(b"Termino:200",b""))
                    conexion=True
                    break
                else:
                    # Almacenar datos.
                    # data+=input_data.decode(FORMAT)
                    file.write(input_data)
                    send_bytes+=len(input_data)

    # Enviar mensaje de confirmacion de recibido
    s.send(b"Recibido")

    t2 = time.time()
    date = datetime.now()
    date_time = date.strftime("%m-%d-%Y-%H-%M-%S")
    text = "---------------------\n"
    text += "Tamaño del archivo: " + str(file_size) + " Bytes" + "\n"
    text += "Conectado con el cliente: " + str((host, port)) + "\n"
    text += "Conexion exitosa: " + str(conexion) + "\n"
    text += "El tiempo de transferencia es: " + str(t2 - t1) + " ms""\n"
    print(text)
    with open('logs_cliente/' + date_time + "-log.txt", 'a') as f:
        f.write(text)

    s.close()


class ClientThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_ID = thread_id

    def run(self):
        on_create_client(self.thread_ID)


while concurrent_clients > 0:
    thread = ClientThread(concurrent_clients)
    thread.start()
    concurrent_clients = concurrent_clients - 1

