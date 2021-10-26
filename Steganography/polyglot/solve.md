Extract the polyglot files via `binwalk -e`.

Take each of the RGB values of the pixels and use them to xor the data file.

```python
from PIL import Image

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

# pixel is a tuple of (R, G, B)
with Image.open("key.png") as im:
    for pixel in im.getdata():
        pixel_bytes.extend(pixel)

key = bytes(pixel_bytes)

xor = XOR(key)

with open("data", "rb") as data_file:
    print(xor.encrypt(data_file.read()))

```