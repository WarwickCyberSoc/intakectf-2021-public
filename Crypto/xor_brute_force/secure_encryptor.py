#!/usr/bin/env python3
import os

with open("flag.txt", "rb") as flag_file:
    flag = flag_file.read()

key_length = 4
key = os.urandom(key_length)

encrypted = b""

for i in range(len(flag)):
    encrypted += bytes([flag[i] ^ key[i % key_length]])

print("Encrypted message: " + encrypted.hex())
