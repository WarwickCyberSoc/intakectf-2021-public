from pwn import *
import rstr

#run again if doesn't work first time, I think ansi codes may break stuff
class Colours:
    FLAG = '\u001b[33;1m\u001b[41m'
    END = '\u001b[0m'
# p = process(["/usr/bin/python3","server.py"],level="error")
p=remote("127.0.0.1",8080)
p.recvline()
pattern = p.recvline()
p.recvuntil(b"Enter string:")
regexToMatch = pattern.decode().split("Pattern: ")[1]
log.info(f"Pattern to match: {regexToMatch}")
#generate matching string
generatedString=rstr.xeger(regexToMatch)

log.success(f"Generated String: {generatedString}")
p.sendline(generatedString.encode())
#print flag nicely since fat output
log.success(f"Output: {Colours.FLAG}{p.recvline().decode().strip()}{Colours.END}")