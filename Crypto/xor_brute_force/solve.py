#!/usr/bin/env python3

# As we know that the flag starts with WMG{, we can brute force the key
# until the first 4 characters are WMG{ and then decode the rest of the message

key = b""
flag = bytearray.fromhex(
    "83ec264f8c91136b9df20f608bf30475b8cd386b91cf22468dd13505e4cf5e05f5904049"
)

for i in range(256):
    if chr(flag[0] ^ i) == "W":
        key += bytes([i])

for i in range(256):
    if chr(flag[1] ^ i) == "M":
        key += bytes([i])

for i in range(256):
    if chr(flag[2] ^ i) == "G":
        key += bytes([i])

for i in range(256):
    if chr(flag[3] ^ i) == "{":
        key += bytes([i])

# At this point, we've found the entire XOR key and can decrypt the rest of the message
print("Found key: " + key.hex())

decrypted = b""

for i in range(len(flag)):
    decrypted += bytes([flag[i] ^ key[i % 4]])

print("Found flag: " + decrypted.decode())
