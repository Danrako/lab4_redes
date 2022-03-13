# https://gist.github.com/AlyoshaS/ecd9aa68a5358b467a70cf39aa681c00

# Importar la libreria del socket
import socket
import threading
import hashlib
import os
import time
from datetime import datetime
SIZE = 2048
FORMAT = "utf-8"
FILE_END = "FILE_END"
PORT = 12345


def main():
    # Modificar direccion del servidor
    host = "192.168.28.1"  # "192.168.1.2" #Server address #Tomas: 192.168.85.1
    port = PORT

    # socket.AF_INET define la familia de protocolos IPv4. Socket.SOCK_STREAM define la conexión TCP.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # La instrucción s.bindhost, port toma solo un argumento. Vincule el socket al host y al número de puerto.
    # La sentencia s.listen(2) escucha la conexión y espera al cliente.
    s.bind((host, port)) #bind server

    # El ciclo while mantiene vivo el programa del servidor y no detiene la ejecución del código. 
    # Puede establecer un límite de conexión para el ciclo while; 
    # Por ejemplo, establezca while i > 10 e incremente 1 en i(i += 1) en cada conexión.

    # Se pide la informacion del archivo que se desea enviar al usuario
    # 1 identifica al archivo de 100MB y 2 identifica al archivo de 250MB
    # Una vez se identifica la informacion, se abre el archivo correspondiente

    print("Server config:")

    selected_file = int(input("Escriba el id del archivo que quiere enviar, donde 1 es para el archivo de 100MB "
                        "y 2 es para el archivo de 250MB: "))

    concurrent_clients = int(input("Escriba el número de conecciones concurrentes que desea tener: "))

    s.listen(concurrent_clients+1)

    print("Server listening on port ", PORT)

    count = 0
    barrier = threading.Barrier(concurrent_clients)
    clientesFaltantes = concurrent_clients
    while clientesFaltantes > 0:

        conn, addr = s.accept()

        count += 1
        print("Accepted {} connections so far".format(count))

        thread = ClientThread(count, conn, addr, selected_file, barrier)

        thread.start()
        clientesFaltantes = clientesFaltantes-1


def on_new_client(conn, addr, selected_file, barrier):
    barrier.wait()
    t1 = time.time()
    print("Enviando archivo al usuario", addr)
    if selected_file == 1:
        path = "data/100MB.txt"
    elif selected_file == 2:
        path = "data/250MB.txt"
    else:
        print("No se pudo leer el archivo")
        path = open("/")

    # Se lee el archivo
    # breakpoint()
    file = open(path, "r")
    data = file.read()

    # Se saca la codificacion de hash del archivo
    data_encoded = data.encode(FORMAT)
    data_hash = hashlib.md5(data_encoded).hexdigest()
    file_size = os.path.getsize(path)
    sf = str(file_size)
    conn.send(sf.encode(FORMAT))
    conn.send(data_hash.encode(FORMAT))

    while True:
        file_content = file.read(SIZE)
        send_bytes = 0
        packets = 0
        while file_content:
            conn.send(file_content)
            send_bytes += len(file_content)
            file_content = file.read(SIZE)
            packets += 1
        break

    # La función conn.send() envía el mensaje al cliente. Finalmente, conn.close() cierra el socket.
    conn.send(b"Mensaje enviado")
    conn.close()
    t2 = time.time()

    date = datetime.now()
    date_time = date.strftime("%m-%d-%Y-%H-%M-%S")
    text = "---------------------\n"
    text += "Nombre archivo: " + path + "\n"
    text += "Tamaño del archivo: " + str(file_size) + " Bytes" + "\n"
    text += "Conectado con el cliente: " + str(addr) + "\n"
    text += "El tiempo de transferencia es: " + str(t2 - t1) + " ms""\n"
    print(text)
    with open('logs/' + date_time + "-log.txt", 'w') as f:
        f.write(text)


class ClientThread(threading.Thread):
    def __init__(self, thread_id, conn, addr, selected_file, barrier):
        threading.Thread.__init__(self)
        self.thread_ID = thread_id
        self.conn = conn
        self.addr = addr
        self.selected_file = selected_file
        self.barrier = barrier

    def run(self):
        on_new_client(self.conn, self.addr, self.selected_file, self.barrier)


if __name__ == "__main__":
    
    main()
