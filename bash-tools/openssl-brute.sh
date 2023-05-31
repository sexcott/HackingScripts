#!/bin/bash


for pass in $(cat /usr/share/wordlists/rockyou.txt); do
  openssl aes-256-cbc -d -in drupal.enc -out drupal.decrypt -pass pass:$pass &>/dev/null

  if [ $(echo $?) == '0' ]; then
    echo -e "\n [+] La contraseña es: $pass"
    exit 0
  fi
done
