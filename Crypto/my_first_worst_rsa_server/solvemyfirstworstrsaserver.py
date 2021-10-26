# solve my first worst rsa server

# e=7
# padding is static, prefixed to your message - and also the flag
# and we can encrypt as many messages as we want -
# so we should be able to do a franklin-reiter related message attack

# https://en.wikipedia.org/wiki/Coppersmith%27s_attack
# https://crypto.stackexchange.com/questions/30884/help-understanding-basic-franklin-reiter-related-message-attack

from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
from sage.all import *

# doit = process(["python3", "my_first_worst_rsa_server.py"])
doit = remote("localhost", 30002)

doit.recvuntil("> ")

doit.sendline("1")  # get public key
r = doit.recvuntil("> ").split(b"\n")

n = int(r[0].split(b": ")[1], 16)
e = int(r[1].split(b": ")[1], 16)

print(hex(n), hex(e))

# get two messages - the first one has nothing added, so it's just the flag
# the second one is the flag + cope

messages = [b"", b"cope"]
results = []

for message in messages:
    doit.sendline("2")
    doit.recvuntil(": ")
    doit.sendline(message)
    r = doit.recvuntil("> ").split(b"\n")

    results.append(int(r[0].split(b": ")[1], 16))

# print(results)

# thusly stolen from
# https://crypto.stackexchange.com/questions/30884/help-understanding-basic-franklin-reiter-related-message-attack

c1, c2 = results

# R.<X> = Zmod(n)[]
R = Zmod(n)["X"]
(X,) = R._first_ngens(1)
f1 = (X ** 7) - c1
f2 = ((X + bytes_to_long(b"cope")) ** 7) - c2


def my_gcd(a, b):
    return a.monic() if b == 0 else my_gcd(b, a % b)


flag = -my_gcd(f1, f2).coefficients()[0]
print(long_to_bytes(int(flag)))

# run this in sage via
# sage -python3 solvemyfirstworstrsaserver.py
