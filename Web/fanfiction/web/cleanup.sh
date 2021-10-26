#!/bin/bash

# Reset redis settings
printf 'config set dir ./\n' | netcat -w 1 localhost 6379
printf 'config set dbfilename dump.rdb\n' | netcat -w 1 localhost 6379
printf 'save\n' | netcat -w 1 localhost 6379

# Remove redis files
rm /var/www/html/redis/*
