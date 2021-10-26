#!/usr/bin/env python3
from PIL import Image

data_message = b"""do we exist? must we exist? does it even matter? oh well, here is your flag i guess WMG{p0lYgl07_fIL35_AR3_GR3A7_F0r_HIDINg_Da7A_fr0M_5crU82}"""


class XOR:
    def __init__(self, key: bytes):
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        xored = b""
        for i in range(len(data)):
            xored += bytes([data[i] ^ self.key[i % len(self.key)]])
        return xored

    def decrypt(self, data: bytes) -> bytes:
        return self.encrypt(data)


pixel_bytes = []

with Image.open("key.png") as im:
    for pixel in im.getdata():
        pixel_bytes.extend(pixel)

key = bytes(pixel_bytes)

xor = XOR(key)

with open("data", "wb") as data_file:
    data_file.write(xor.encrypt(data_message))
