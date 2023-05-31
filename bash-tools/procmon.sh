#!/bin/bash

function ctrl_c(){
  echo -e "\n\n[+] Saliendo..."
  exit 1
}


#ctrl + c 
trap ctrl_c INT

old_process=$(ps -eo command)

while true; do

  new_process=$(ps -eo command)
  diff <(echo $old_process) <(echo $new_process) | grep "[\<\>]" | grep -vE "command|procmon"
  old_process=$new_process

done
