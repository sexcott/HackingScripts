import requests
import re
import pdb
import signal
import time
import sys

def def_handler(sig, frame):
    print("\n[!] Saliendo...")
    sys.exit(1)

# ctrl + c
signal.signal(signal.SIGINT, def_handler)


if __name__ == "__main__":
    time.sleep(2)
