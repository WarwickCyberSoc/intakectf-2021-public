#!/usr/bin/env python3
from Crypto.Util.number import getPrime, long_to_bytes, inverse


class TextbookRSA:
    def __init__(self):
        self.p = getPrime(1024)
        self.q = getPrime(1024)
        self.e = 3
        self.n = self.p * self.q
        self.d = inverse(self.e, (self.p - 1) * (self.q - 1))

    def encrypt(self, data: bytes) -> bytes:
        pt = int(data.hex(), 16)
        ct = pow(pt, self.e, self.n)
        return long_to_bytes(ct)

    def decrypt(self, data: bytes) -> bytes:
        ct = int(data.hex(), 16)
        pt = pow(ct, self.d, self.n)
        return long_to_bytes(pt)


rsa = TextbookRSA()

with open("flag.txt", "rb") as flag_file:
    flag = flag_file.read().strip()

print("n =", rsa.n)
print("e =", rsa.e)
print("flag =", rsa.encrypt(flag).hex())
