#!/usr/bin/env python3

import os, random, time, subprocess

menu = """

=====================================================================
Super Secure System Management System Shell Command Center (SSSMSSCC)
=====================================================================

Available actions:
[1] Print System's Hostname
[2] Print Running Processes
[3] Perform a System Check
[4] Read /etc/passwd file
[5] Ping

"""

try:
    while True:
        print(menu)
        option = input()
        if option == "1":
            os.system("hostname")
        if option == "2":
            os.system("ps au")
        if option == "3":
            c = 0
            while c < 100:
                c += random.randrange(20)
                time.sleep(random.randrange(4))
                print("System Check in progress: {}%".format(c))
            print("System Check in progress: 100%")
            print("All seems Goodie Good :)")
        if option == "4":
            os.system("vim /etc/passwd")
        if option == "5":
            print("Pong")
except KeyboardInterrupt:
    print("Goodbye!")
    exit()
