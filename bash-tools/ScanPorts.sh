#!/bin/bash

#Functions
function ctrl_c(){
  echo -e "\n\n[!] Saliendo..."
}

# ctrl + c
trap ctrl_c INT


for host in 172.19.0.4 172.19.0.3 172.19.0.2 172.19.0.1 172.18.0.2 172.18.0.1; do
  echo -e "\n[+] Escaneo en el hosts: $host.0/24"
  for i in $(seq 1 10000); do

    timeout 1 bash -c "echo ' ' > /dev/tcp/$host/$i" &>/dev/null && echo -e "\n[+] Puerto encontrado: $i > $host" &

  done; wait

done

