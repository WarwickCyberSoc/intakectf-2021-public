#!/bin/bash

menu="

=====================================================================
Super Secure System Management System Shell Command Center (SSSMSSCC)
=====================================================================

Available actions:
[1] Print System's Hostname
[2] Print Running Processes
[3] Perform a System Check
[4] Read /etc/passwd file
[5] Ping

"

while true; do
    echo "$menu"
    read input

    if [ "$input" = "1" ]; then
        hostname
    elif [ "$input" = "2" ]; then
        ps au
    elif [ "$input" = "3" ]; then
        c=0
        while [ $c -lt 100 ]; do
            echo "System Check in progress: $c%"
            sleep $(shuf -i 1-3 -n 1)
            c=$((c + $(shuf -i 1-20 -n 1)))
        done
        echo "System Check in progress: 100%"
        echo "All seems Goodie Good :)"
    elif [ "$input" = "4" ]; then
        vim /etc/passwd
    elif [ "$input" = "5" ]; then
        echo "Pong"
    fi 
done
