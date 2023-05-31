#!/bin/bash

#Functions
function ctrl_c(){
  echo -e "\n\n[!] Saliendo..."
}

# ctrl + c
trap ctrl_c INT


hosts=(172.19.0 172.18.0)

for host in ${hosts[@]}; do
  echo -e "\n[+] Escaneo en el hosts: $host.0/24"
  for i in $(seq 1 254); do

    timeout 1 bash -c "ping -c 1 $host.$i" &>/dev/null && echo -e "\n[+] Host encontrado: $host.$i" &

  done; wait

done

