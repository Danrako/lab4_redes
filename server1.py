# https://gist.github.com/AlyoshaS/ecd9aa68a5358b467a70cf39aa681c00

# Importar la libreria del socket
import socket
import hashlib
import os
import time
from datetime import datetime
SIZE = 2048
FORMAT = "utf-8"
FILE_END = "FILE_END"

def main():
    # Modificar direccion del servidor
    host = "192.168.56.1" # "192.168.1.2" #Server address 
    port = 12345 #Port of Server

    # socket.AF_INET define la familia de protocolos IPv4. Socket.SOCK_STREAM define la conexión TCP.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # La instrucción s.bindhost, port toma solo un argumento. Vincule el socket al host y al número de puerto. La sentencia s.listen(2) escucha la conexión y espera al cliente.
    s.bind((host,port)) #bind server
    s.listen(2)

    # El ciclo while mantiene vivo el programa del servidor y no detiene la ejecución del código. 
    # Puede establecer un límite de conexión para el ciclo while; 
    # Por ejemplo, establezca while i > 10 e incremente 1 en i(i += 1) en cada conexión.

    # Mirar como cerrar servidor
    while True:
        # La instrucción conn, addr = s.accept() devuelve dos valores: conn y addr.
       
        conn, addr = s.accept()
        t1 = time.time()
        print(addr, "Usuario conectado")
        # Se pide la informacion del archivo que se desea enviar al usuario
        # 1 identifica al archivo de 100MB y 2 identifica al archivo de 250MB
        archivo = int(input("Escriba el id del archivo que quiere enviar, donde 1 es para el archivo de 100MB y 2 es para el archivo de 250MB: "))
        # Una vez se identifica la informacion, se abre el archivo correspondiente
        if archivo == 1:
            path = "100MB.txt"
            
        elif archivo == 2:
            path = "arch.txt"
        else:
            print("No se pudo leer el mensaje")
            path = open("/")
        
        # Se lee el archivo
        # breakpoint()
        file = open(path,"r")
        data = file.read()
        
        # Se saca la codfigicacion de hash del archivo
        dataEn=data.encode(FORMAT)
        dataHash = hashlib.md5(dataEn).hexdigest()
        sizefile = os.path.getsize(path)
        print(sizefile)
        sf = str(sizefile)
        conn.send(sf.encode(FORMAT))
        conn.send(dataHash.encode(FORMAT))
        print("Hash:",dataHash)
        
        while True:
            content_file = file.read(SIZE)
            while content_file:
                conn.send(content_file)
                bytes_enviados += len(content_file)
                content_file = file.read(SIZE)
                paquetes+=1
            break
        
        # La función conn.send() envía el mensaje al cliente. Finalmente, conn.close() cierra el socket.
        conn.send(b"Mensaje enviado")
        conn.close()
        t2 =time.time()
        print("-- Milisegundos --", t2-t1)

        fecha = datetime.now()
        date_time = fecha.strftime("%m-%d-%Y-%H-%M-%S")
        texto="---------------------\n"
        texto+="Nombre archivo "+ path + "\n"
        texto+="Tamaño del archivo "+ str(sizefile)+ "\n"
        texto+="Conectado con el usuario: "+str(addr) + "\n"
        texto+="El tiempo de transferencia es"+ str(t2-t1)+"\n"
        print(texto)
        with open('logs/'+date_time+"-log.txt", 'w') as f:
            f.write(texto)
    

if __name__ == "__main__":
    
    main()