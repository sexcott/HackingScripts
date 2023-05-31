#!/bin/bash

echo -e "Las tareas pendientes son:\n\n" "\t"$(curl -s -X GET "https://uev.uadeo.mx/calendar/view.php" -H "cookie: MoodleSession=mk3r1ia8iovheq2kfk14iqeu1o" | html2text | grep -i "# Eventos próximos" -A 50 | grep -v "[.*?]" | grep -i "evento de curso" -A 50 | grep -vE "^\[|^\!|__" | grep -i "evento de curso" -A 4 | sed "s/\/n//g" | sed "s/--/apocosi/g" | sed "s/apocosi/\n/g")
