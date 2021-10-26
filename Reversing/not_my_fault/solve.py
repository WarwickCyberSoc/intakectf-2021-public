#solve oshawks "not_my_fault" challenge

#reversing challenge, and we're given just the oshawk_not_my_fault binary

#it's compiled (assembled?) assembly, as opposed to being compiled from a higher level language

#the very first thing it does is a syscall,

"""
│           0x00401000      b809000000     mov eax, 9                  ; [01] -r-x section size 40521 named .text
│           0x00401005      bf00000000     mov edi, 0
│           0x0040100a      be00100200     mov esi, 0x21000
│           0x0040100f      ba00000000     mov edx, 0
│           0x00401014      41ba22000000   mov r10d, 0x22              ; '"' ; 34
│           0x0040101a      49c7c0ffffff.  mov r8, 0xffffffffffffffff
│           0x00401021      41b900000000   mov r9d, 0
│           0x00401027      0f05           syscall
"""

#this is syscall 9, mmap
#specifically, mmap(0, 0x21000, 0, 0x22, -1, 0)

#so, address is specified as 0 - this means it chooses a (pseudo)random location, page aligned
#the length is 0x21000

#the permissions are 0 - PROT_NONE
#so right now you can't do anything to it

#https://man7.org/linux/man-pages/man2/mmap.2.html
#https://elixir.bootlin.com/linux/latest/source/include/uapi/linux/mman.h#L16
#for flags,
#hm
#not all the flags are there
#it's something and MAP_PRIVATE
#https://elixir.bootlin.com/linux/latest/source/include/uapi/asm-generic/mman-common.h

#0x22 = MAP_ANONYMOUS | MAP_PRIVATE

#alright
#-1 for no file descriptor, and 0 for no offset

#so it's just mapping a big chunk at some address - the address is returned by the mmap syscall
#│           0x00401029      4889c3         mov rbx, rax
#and placed into rbx

#│           0x0040102c      49bccbc89fb4.  movabs r12, 0x572039efb49fc8cb
#obviously important constant here

#this is the next block

"""
│           0x00401036      4989dd         mov r13, rbx
│       ┌─> 0x00401039      4d31f6         xor r14, r14
│       ╎   0x0040103c      4d89e7         mov r15, r12
│       ╎   0x0040103f      4983e701       and r15, 1
│      ┌──< 0x00401043      7404           je 0x401049
│      │╎   0x00401045      4983ce01       or r14, 1
│      └──> 0x00401049      49d1ec         shr r12, 1
│       ╎   0x0040104c      4d89e7         mov r15, r12
│       ╎   0x0040104f      4983e701       and r15, 1
│      ┌──< 0x00401053      7404           je 0x401059
│      │╎   0x00401055      4983ce02       or r14, 2
│      └──> 0x00401059      b80a000000     mov eax, 0xa
│       ╎   0x0040105e      4c89ef         mov rdi, r13
│       ╎   0x00401061      be00100000     mov esi, 0x1000
│       ╎   0x00401066      4c89f2         mov rdx, r14
│       ╎   0x00401069      0f05           syscall
│       ╎   0x0040106b      4981c5001000.  add r13, 0x1000
│       ╎   0x00401072      49d1ec         shr r12, 1
│       └─< 0x00401075      75c2           jne 0x401039
"""
#a loop

#r13 holds the base address that was mmap'd going into the loop and r12 holds the "magic constant"

#it clears r14 and obtains the lowest bit of the magic constant via & 1 (it's a 1, it's odd) in r15
#if it's 0, it jumps past the or - otherwise it sets the lowest bit of r14 to 1 as well

#it then shifts the magic constant right by 1, removing the lowest bit
#it agains ands to retrieve the lowest byte, 
#if the lowest byte is a 0, it sets another bit in r14

#then, a syscall
#this time it's mprotect
#it uss r13, the base address
#and r14 as the protections
#then it calls mprotect and adds 0x1000 to the base address
#and shifts the magic constant right again

#so, here's what the loop does
#every iteration, it uses 2 bits from the magic constant
#the first bit representing whether it's PROT_READ and the second whether it's PROT_WRITE

#so, every 0x1000 (page sized) chunk of the mmap'd area is going to have no permissions, be R__ or RW_
#interesting
#lets see what happens next

"""
│           0x00401077      4c8da3000002.  lea r12, [rbx + 0x20000]
│           0x0040107e      b80a000000     mov eax, 0xa
│           0x00401083      4c89e7         mov rdi, r12
│           0x00401086      be00100000     mov esi, 0x1000
│           0x0040108b      ba07000000     mov edx, 7
│           0x00401090      0f05           syscall
"""
#it loads in the last chunk (0x1000 before the end of the mmap'd area)
#and mprotects it to RWX

"""
|           0x00401092      b80d000000     mov eax, 0xd                ; 13
│           0x00401097      bf0b000000     mov edi, 0xb                ; 11
│           0x0040109c      48be00b04000.  movabs rsi, segment.LOAD2   ; 0x40b000
│           0x004010a6      ba00000000     mov edx, 0
│           0x004010ab      41ba08000000   mov r10d, 8
│           0x004010b1      0f05           syscall
"""

#this is interesting
#this is sys_rt_sigaction - a signal handler
#the signal is signal 11 - SIGSEGV
#hmm
#it points to the top of segment.LOAD2 for the sigaction struct
#I don't know what the oact struct is, but that's null anyway so it doesn't matter
#it also specifies the sigsetsize as 8 bytes 

#so lets look at there
"""
0x0040b000  0x00000000004011ef  0x0000000004000000   ..@.............
0x0040b010  0x00000000004011f0  0x0000000000000000   ..@.............
0x0040b020  0x0000000000000000  0x0000000000000000   ................
0x0040b030  0x0000000000000000  0x0000000000000000   ................
0x0040b040  0x0000000000000000  0x0000000000000000   ................
0x0040b050  0x0000000000000000  0x0000000000000000   ................
0x0040b060  0x0000000000000000  0x0000000000000000   ................
0x0040b070  0x0000000000000000  0x0000000000000000   ................
0x0040b080  0x0000000000000000  0x0000000000000000   ................
0x0040b090  0x0000000000000000  0x0000000000000060   ........`.......
"""
#https://man7.org/linux/man-pages/man2/sigaction.2.html
"""
struct sigaction {
#ifndef __ARCH_HAS_IRIX_SIGACTION
	__sighandler_t	sa_handler;
	unsigned long	sa_flags;
#else
	unsigned int	sa_flags;
	__sighandler_t	sa_handler;
#endif
#ifdef __ARCH_HAS_SA_RESTORER
	__sigrestore_t sa_restorer;
#endif
	sigset_t	sa_mask;	/* mask last for extensibility */
};
"""
#so, the SIGSEGV handler is at 0x00000000004011ef, and the mask is 8 bytes away
#https://elixir.bootlin.com/linux/latest/source/include/uapi/asm-generic/signal-defs.h
#the flag is the obsolete SA_RESTORER

"""           This flag is used by C
              libraries to indicate that the sa_restorer field contains
              the address of a "signal trampoline".  See sigreturn(2)
              for more details.
"""
#so the signal trampoline is 0x00000000004011f0

#alright
#0x00000000004011ef is a ret - which will just return immediately

"""
        ╎   0x004011f0      48c78424a800.  mov qword [rsp + 0xa8], 0x401203 ; [0x401203:8]=0xfffed6e908c48348
        ╎   0x004011fc      b80f000000     mov eax, 0xf                ; 15
        ╎   0x00401201      0f05           syscall
"""
#0x00000000004011f0 is a sigreturn syscall, which I think just sets RIP to 0x401203

#we'll look more at that later

#after setting the signal handler, it enters a large loop

"""
           0x004010b3      49bc98b04000.  movabs r12, 0x40b098
│           ; CODE XREF from entry0 @ 0x4011de
│       ┌─> 0x004010bd      4d8b2c24       mov r13, qword [r12]
│       ╎   0x004010c1      4d85ed         test r13, r13
│      ┌──< 0x004010c4      0f8419010000   je 0x4011e3
│      │╎   0x004010ca      4983c408       add r12, 8
│     ┌───> 0x004010ce      49ffcd         dec r13
│     ╎│╎   0x004010d1      4d8b3424       mov r14, qword [r12]
│     ╎│╎   0x004010d5      4983c408       add r12, 8
│     ╎│╎   0x004010d9      4831c0         xor rax, rax
│     ╎│╎   0x004010dc      41ffd6         call r14
│     ╎│╎   0x004010df      48ffc0         inc rax
│     ╎│╎   0x004010e2      4d89ee         mov r14, r13
│     ╎│╎   0x004010e5      49c1ee03       shr r14, 3
│     ╎│╎   0x004010e9      4c8dbb000002.  lea r15, [rbx + 0x20000]
│     ╎│╎   0x004010f0      438a0c37       mov cl, byte [r15 + r14]
│     ╎│╎   0x004010f4      48d1e1         shl rcx, 1                  ; arg4
│     ╎│╎   0x004010f7      4801c1         add rcx, rax                ; arg4
│     ╎│╎   0x004010fa      43880c37       mov byte [r15 + r14], cl
│     ╎│╎   0x004010fe      4d85ed         test r13, r13
│     └───< 0x00401101      75cb           jne 0x4010ce
│      │╎   0x00401103      48870425d85e.  xchg qword [segment.LOAD3], rax
│      │╎   0x0040110b      48870c25e05e.  xchg qword [0x415ee0], rcx  ; arg4
│      │╎   0x00401113      48871425e85e.  xchg qword [0x415ee8], rdx
│      │╎   0x0040111b      48873c25f05e.  xchg qword [0x415ef0], rdi
│      │╎   0x00401123      48873425f85e.  xchg qword [0x415ef8], rsi
│      │╎   0x0040112b      4c870425005f.  xchg qword [0x415f00], r8
│      │╎   0x00401133      4c870c25085f.  xchg qword [0x415f08], r9
│      │╎   0x0040113b      4c871425105f.  xchg qword [0x415f10], r10
│      │╎   0x00401143      4c871c25185f.  xchg qword [0x415f18], r11
│      │╎   0x0040114b      4c872425205f.  xchg qword [0x415f20], r12
│      │╎   0x00401153      4c872c25285f.  xchg qword [0x415f28], r13
│      │╎   0x0040115b      4c873425305f.  xchg qword [0x415f30], r14
│      │╎   0x00401163      50             push rax
│      │╎   0x00401164      488b0425385f.  mov rax, qword [0x415f38]   ; [0x415f38:8]=0
│      │╎   0x0040116c      50             push rax
│      │╎   0x0040116d      9d             popfq
│      │╎   0x0040116e      58             pop rax
│      │╎   0x0040116f      41ffd7         call r15
│      │╎   0x00401172      50             push rax
│      │╎   0x00401173      9c             pushfq
│      │╎   0x00401174      58             pop rax
│      │╎   0x00401175      48890425385f.  mov qword [0x415f38], rax   ; [0x415f38:8]=0
│      │╎   0x0040117d      58             pop rax
│      │╎   0x0040117e      48870425d85e.  xchg qword [segment.LOAD3], rax
│      │╎   0x00401186      48870c25e05e.  xchg qword [0x415ee0], rcx  ; arg4
│      │╎   0x0040118e      48871425e85e.  xchg qword [0x415ee8], rdx
│      │╎   0x00401196      48873c25f05e.  xchg qword [0x415ef0], rdi
│      │╎   0x0040119e      48873425f85e.  xchg qword [0x415ef8], rsi
│      │╎   0x004011a6      4c870425005f.  xchg qword [0x415f00], r8
│      │╎   0x004011ae      4c870c25085f.  xchg qword [0x415f08], r9
│      │╎   0x004011b6      4c871425105f.  xchg qword [0x415f10], r10
│      │╎   0x004011be      4c871c25185f.  xchg qword [0x415f18], r11
│      │╎   0x004011c6      4c872425205f.  xchg qword [0x415f20], r12
│      │╎   0x004011ce      4c872c25285f.  xchg qword [0x415f28], r13
│      │╎   0x004011d6      4c873425305f.  xchg qword [0x415f30], r14
│      │└─< 0x004011de      e9dafeffff     jmp 0x4010bd
│      └──> 0x004011e3      b83c000000     mov eax, 0x3c               ; '<' ; 60
│           0x004011e8      bf00000000     mov edi, 0
│           0x004011ed      0f05           syscall
"""
#the end of this loop is the exit syscall

#lets look at the first, smaller loop at the start
"""
           0x004010b3      49bc98b04000.  movabs r12, 0x40b098
│           ; CODE XREF from entry0 @ 0x4011de
│       ┌─> 0x004010bd      4d8b2c24       mov r13, qword [r12]
│       ╎   0x004010c1      4d85ed         test r13, r13
│      ┌──< 0x004010c4      0f8419010000   je 0x4011e3
│      │╎   0x004010ca      4983c408       add r12, 8
│     ┌───> 0x004010ce      49ffcd         dec r13
│     ╎│╎   0x004010d1      4d8b3424       mov r14, qword [r12]
│     ╎│╎   0x004010d5      4983c408       add r12, 8
│     ╎│╎   0x004010d9      4831c0         xor rax, rax
│     ╎│╎   0x004010dc      41ffd6         call r14
│     ╎│╎   0x004010df      48ffc0         inc rax
│     ╎│╎   0x004010e2      4d89ee         mov r14, r13
│     ╎│╎   0x004010e5      49c1ee03       shr r14, 3
│     ╎│╎   0x004010e9      4c8dbb000002.  lea r15, [rbx + 0x20000]
│     ╎│╎   0x004010f0      438a0c37       mov cl, byte [r15 + r14]
│     ╎│╎   0x004010f4      48d1e1         shl rcx, 1                  ; arg4
│     ╎│╎   0x004010f7      4801c1         add rcx, rax                ; arg4
│     ╎│╎   0x004010fa      43880c37       mov byte [r15 + r14], cl
│     ╎│╎   0x004010fe      4d85ed         test r13, r13
│     └───< 0x00401101      75cb           jne 0x4010ce
"""
#so, first it looks at 0x40b098
#this holds at first, 0x60
#and then a whole bunch of addresses
#i.e.
"""
0x0040b098  0x0000000000000060  0x0000000000408e69   `.......i.@.....
0x0040b0a8  0x0000000000407189  0x0000000000409ec1   .q@.......@.....
0x0040b0b8  0x00000000004035d4  0x000000000040519c   .5@......Q@.....
"""
#part of the large .rodata section

#it moves the value there into r13,
#if it's 0, the program exits
#otherwise we continue

#it adds 8 to r12 - moving across to the next value
#it decreases r13 by one, then moves the next value from that data section (at r12) into r14
#it adds 8 to r12 again, clears rax, and calls r14

#after it's been called, it increments rax by 1

#so, for example
#the first thing it'll call is 0x0000000000408e69
"""
            0x00408e69      4c8bbb9b8300.  mov r15, qword [rbx + 0x839b]
            0x00408e70      c3             ret
"""
#it looks like all the addresses point to one of these -
#what's important here is that rbx is still the base address from mmap all that time ago
#so these are offsets within those sections - but all these sections are empty
#I assume some of these calls will segfault, triggering the segfault handler
#because some areas are still under PROT_NONE

#after doing this, 
#it moves r13 (current pos in the data section) into r14, and shifts it right by 8
#it then loads in an address from the start of the RWX section at rbx+0x20000 into r15
#it uses r14 as an offset into that section, taking a single byte from r15+r14
#it shifts this byte left by 1, adds rax to it, and moves it back into that RWX section
#if r13 is now null, it ends

#so, here's what's happening
#this is a loop, happening 0x60 times - that's the first value in the data section

#this loop is loading something into the RWX section
#so if I had to guess, it's probably loading the code it intends to execute into that section

#what's interesting is that it can jump back up here at the bottom of the larger loop, meaning it might be loading multiple lots of code
#but lets ignore that for now


#it looks like it uses the third segment and onwards as scratch space - 
#it saves most registers (except important state registers like RSP and RBP) into there

"""
│      │╎   0x00401103      48870425d85e.  xchg qword [segment.LOAD3], rax
│      │╎   0x0040110b      48870c25e05e.  xchg qword [0x415ee0], rcx  ; arg4
│      │╎   0x00401113      48871425e85e.  xchg qword [0x415ee8], rdx
│      │╎   0x0040111b      48873c25f05e.  xchg qword [0x415ef0], rdi
│      │╎   0x00401123      48873425f85e.  xchg qword [0x415ef8], rsi
│      │╎   0x0040112b      4c870425005f.  xchg qword [0x415f00], r8
│      │╎   0x00401133      4c870c25085f.  xchg qword [0x415f08], r9
│      │╎   0x0040113b      4c871425105f.  xchg qword [0x415f10], r10
│      │╎   0x00401143      4c871c25185f.  xchg qword [0x415f18], r11
│      │╎   0x0040114b      4c872425205f.  xchg qword [0x415f20], r12
│      │╎   0x00401153      4c872c25285f.  xchg qword [0x415f28], r13
│      │╎   0x0040115b      4c873425305f.  xchg qword [0x415f30], r14
│      │╎   0x00401163      50             push rax
│      │╎   0x00401164      488b0425385f.  mov rax, qword [0x415f38]   ; [0x415f38:8]=0
│      │╎   0x0040116c      50             push rax
│      │╎   0x0040116d      9d             popfq
│      │╎   0x0040116e      58             pop rax
│      │╎   0x0040116f      41ffd7         call r15
"""

#this also serves to clear these registers on the first call, as initially this area is zeroed, and it's performing an exchange

#it pushes rax, then moves in something past the end of the scratch space, and pushes it again
#then, popfq
#this pops RFLAGS from the stack
#that's moved into RAX
#and finally, r15 is called

#finally, all registers are restored in roughly the same way and it jumps back to the top
#hmmm
#and we're done!

#ok
#so the key is what's in r15
#it looks like each time this loop runs, a different set of code is loaded into the RWX page
#it then preserves state, jumps to it to execute it, then jumps back

#so this entire thing is to obfuscate the code running
#I could reverse it directly, or I could be lazy and intercept each call with radare

import r2pipe
import os
import struct

def debug():
    a = input()
    while a:
        print(r.cmd(a))
        a = input()

r = r2pipe.open("./oshawk_not_my_fault",  flags=["-2"])
#-2 closes stderr, so I don't receive output from the running process
'''
with open("oshawk_profile.rr2", "w") as f:
    f.write("#!/usr/local/bin/rarun2\nstdin=oshawk_input.txt\n")
with open("oshawk_input.txt", "w") as f:
    f.write("WMG{cope}\n")

r.cmd("e dbg.profile=oshawk_profile.rr2") # lazy way to do stdin
r.cmd("ood") #reopen in debugging mode, so the profile is applied

r.cmd("db 0x0040116f") # the call r15 instruction

#first issue, the intentional segfaults
#how do I make radare follow the signal handler?
#huh...
#well
#I think I worked out that all the signal handler does is jump to 0x401203
#via some boujee sigreturn stuff

#I can do that manually, I suppose
#to imitate the signal handler happening

#so, lets break on the call r14
#and determine whether it will segfault - if it will, we do that jump ourselves

r.cmd("db 0x004010dc")


#to work out which addresses will cause a segfault and which won't,
#I could read the segment table after it's done setting it up
#but lets work it out properly, using the magic constant

r.cmd("db 0x00401036")
r.cmd("dc")
#after the mmap, value is in rbx
base = int(r.cmd("dr?rbx"),16)

print("mmap'd base: " + hex(base))

magic_constant = 0x572039efb49fc8cb

chunks = {}
#make a list of all the chunks and their permissions

for i in range(base, base+0x21000, 0x1000):
    rbit = magic_constant & 1
    magic_constant = magic_constant >> 1
    wbit = (magic_constant & 1) << 1
    magic_constant = magic_constant >> 1

    chunks[i] = rbit | wbit
    
"""
for address, prot in chunks.items():
    print(hex(address), hex(prot))
"""

r.cmd("dc")

#print(r.cmd("dm"))

for i in range(0x60):
    # step once
    r.cmd("ds 1")
    # check the instruction (very boujee)
    res = r.cmdj("pdj 1")[0]
    if res["type"] != "mov":
        print("not a mov, ???")
    #print(res["disasm"])
    offset = int(res["disasm"].split("[")[1].split("]")[0].split(" + ")[1],16)
    real_address = offset + base
    #print("base + {}: {}".format(offset, real_address))
    
    #now, work out whether this address will cause a segfault or not
    
    #get the chunk by removing the lower 3 nibbles
    chunk_base = (real_address >> 12) << 12

    #print(hex(chunk_base), chunks[chunk_base])
    
    
    #mov qword [rbx + 0xd4be], r15
    #or
    #mov r15, qword [rbx + 0x839b]
    #either requires PROT_READ or PROT_WRITE
    #now, it's cheeky
    #but I think PROT_WRITE implies PROT_READ
    #so PROT_WRITE on its own may still allow me to read
    #i'm not sure
    #i'll allow it to read even when only PROT_WRITE is set
    
    if res["disasm"].split(" ")[1] == "qword" and not chunks[chunk_base] & 2: #so boujee, but this is a write
        #we'll segfault, pretend to be the handler
        #print("this is gonna segfault on write, hell no")
        r.cmd("dr rip = 0x401203")
    
    elif not chunks[chunk_base]: #& 1: #PROT_READ not set
        #we'll segfault, pretend to be the handler
        #print("this is gonna segfault on read, hell no")
        r.cmd("dr rip = 0x401203")

    r.cmd("dc")
    
    #debug()

res = r.cmdj("pdj 0x60 @ r15")

for instruction in res:
    #remove the ending nulls, nobody uses 0000 anyway
    if instruction["bytes"] == "0000":
        continue
    print(instruction["disasm"])
'''

#so, the very first instruction set -

"""
mov qword [rbx + 0x20800], 0x65746e45
ret
"""

#perfect
#this is loading "Ente" into some scratch space (as in the first part of Enter flag:)

#now I know how it works, I can combine the code
#I don't need to dynamically debug any more

#when it recovers from the segfault, it recovers one instruction below the inc rax (and adds 8 to rsp)
#so if there's no segfault, add 1 to rax
#is that how it works?

#ah, I get it
#it's extracting the instructions bitwise

#so, an address that causes a segfault is a 0
#and an address that doesn't cause a segfault is a 1
#now that's ingenious

#and so 0x60 is how many bits the total number of instructions are
#so, I can parse all the instructions out like this

#hm
#is it just the bits in order?
#I don't think so
#it's doing something fancy before it writes the bit

"""
│     ╎│╎   0x004010e2      4d89ee         mov r14, r13
│     ╎│╎   0x004010e5      49c1ee03       shr r14, 3
│     ╎│╎   0x004010e9      4c8dbb000002.  lea r15, [rbx + 0x20000]
│     ╎│╎   0x004010f0      438a0c37       mov cl, byte [r15 + r14]
│     ╎│╎   0x004010f4      48d1e1         shl rcx, 1                  ; arg4
│     ╎│╎   0x004010f7      4801c1         add rcx, rax                ; arg4
│     ╎│╎   0x004010fa      43880c37       mov byte [r15 + r14], cl
"""

#rax is the 1 or 0,
#it moves in the current number of bits to write from r13 and shifts it right by three -
#this is dividing by 8, so it works out the current byte position, since you can't address bits
#it then reads the current byte from that address, shifts it left by 1 to make room for the new bit, and adds the new bit

#it's doing it in reverse, starting at the last byte
#but I think the bits in that byte are in order
#alright
#so we reverse it at the end

magic_constant = 0x572039efb49fc8cb

chunks = {}
#make a list of all the chunks and their permissions

for i in range(0, 0x21000, 0x1000):
    rbit = magic_constant & 1
    magic_constant = magic_constant >> 1
    wbit = (magic_constant & 1) << 1
    magic_constant = magic_constant >> 1

    chunks[i] = rbit | wbit

address = 0x40b098

#it's always the number of bits, followed by that many addresses

instruction_bytes = b""

while True:
    num_of_bits = r.cmdj("pxqj 8 @ {}".format(address))[0]
    print("total number of instruction bits: " + hex(num_of_bits))
    address += 8
    
    if num_of_bits == 0:
        break

    addresses = r.cmdj("pxqj {} @ {}".format(num_of_bits*8, address))

    current_instruction_chunk = ""

    for instruction_address in addresses:
        instruction = r.cmdj("pdj 1 @ {}".format(instruction_address))[0]
        
        offset = int(instruction["disasm"].split("[")[1].split("]")[0].split(" + ")[1],16)
        offset = (offset >> 12) << 12
        
        if instruction["disasm"].split(" ")[1] == "qword" and not chunks[offset] & 2:
            #segfault on write
            res = "0"
        elif not chunks[offset]:# & 1:
            #segfault on read
            res = "0"
        else:
            res = "1"

        current_instruction_chunk = current_instruction_chunk + res

    address += (num_of_bits*8)
    
    #reverse the bytes of the chunk before adding it in
    #https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
    #appropriated

    #print(instruction_bits)
    #instruction_bytes += int(current_instruction_chunk, 2).to_bytes((len(current_instruction_chunk) + 7) // 8, 'big')[::-1]
    #print(instruction_bits)

    #they're all split up with rets, since they're executed one instruction at a time
    #this is always the last byte, a \xc3
    #so remove it
    instruction_bytes += int(current_instruction_chunk, 2).to_bytes((len(current_instruction_chunk) + 7) // 8, 'big')[::-1][:-1]

#looks good, now



with open("oshawk_extracted_asm", "wb") as f:
    f.write(instruction_bytes)

#debug()
r.quit()
os.system("killall oshawk_not_my_fault")

#and there we have the actual code

"""
           0x00000000      48c783000802.  mov qword [rbx + 0x20800], 0x65746e45 ; 'Ente'
│                                                                      ; [0x65746e45:8]=-1
│           0x0000000b      48c783040802.  mov qword [rbx + 0x20804], 0x6c662072 ; 'r fl'
│                                                                      ; [0x6c662072:8]=-1
│           0x00000016      48c783080802.  mov qword [rbx + 0x20808], 0x203a6761 ; 'ag: '
│                                                                      ; [0x203a6761:8]=-1
│           0x00000021      48c7c0010000.  mov rax, 1
│           0x00000028      48c7c7010000.  mov rdi, 1
│           0x0000002f      488db3000802.  lea rsi, [rbx + 0x20800]
│           0x00000036      48c7c20c0000.  mov rdx, 0xc
│           0x0000003d      0f05           syscall
│           0x0000003f      48c7c0000000.  mov rax, 0
│           0x00000046      48c7c7000000.  mov rdi, 0
│           0x0000004d      488db3000802.  lea rsi, [rbx + 0x20800]
│           0x00000054      48c7c2200000.  mov rdx, 0x20               ; " H\xc7\xc0\x01"
│           0x0000005b      0f05           syscall
│           0x0000005d      0f2883000802.  movaps xmm0, xmmword [rbx + 0x20800]
│           0x00000064      0f288b100802.  movaps xmm1, xmmword [rbx + 0x20810]
│           0x0000006b      48c783000802.  mov qword [rbx + 0x20800], 0x6f22ecec ; [0x6f22ecec:8]=-1
│           0x00000076      48c783040802.  mov qword [rbx + 0x20804], 0xc577cb ; [0xc577cb:8]=-1
│           0x00000081      48c783080802.  mov qword [rbx + 0x20808], 0x261c7fbd ; [0x261c7fbd:8]=-1
│           0x0000008c      48c7830c0802.  mov qword [rbx + 0x2080c], 0xffffffffc1521493
│           0x00000097      48c783100802.  mov qword [rbx + 0x20810], 0xffffffffcd8a4abc
│           0x000000a2      48c783140802.  mov qword [rbx + 0x20814], 0x6603e8b0 ; [0x6603e8b0:8]=-1
│           0x000000ad      48c783180802.  mov qword [rbx + 0x20818], 0xffffffffed18b686
│           0x000000b8      48c7831c0802.  mov qword [rbx + 0x2081c], 0x7f37c70c ; [0x7f37c70c:8]=-1
│           0x000000c3      660fef830008.  pxor xmm0, xmmword [rbx + 0x20800]
│           0x000000cb      660fef8b1008.  pxor xmm1, xmmword [rbx + 0x20810]
│           0x000000d3      48c783000802.  mov qword [rbx + 0x20800], 0xc090d ; [0xc090d:8]=-1
│           0x000000de      48c783040802.  mov qword [rbx + 0x20804], 0x20f0b04 ; [0x20f0b04:8]=-1
│           0x000000e9      48c783080802.  mov qword [rbx + 0x20808], 0x6080a01 ; [0x6080a01:8]=-1
│           0x000000f4      48c7830c0802.  mov qword [rbx + 0x2080c], 0x305070e ; [0x305070e:8]=-1
│           0x000000ff      48c783100802.  mov qword [rbx + 0x20810], 0xd04030e ; [0xd04030e:8]=-1
│           0x0000010a      48c783140802.  mov qword [rbx + 0x20814], 0xf070001 ; [0xf070001:8]=-1
│           0x00000115      48c783180802.  mov qword [rbx + 0x20818], 0x8060c05 ; [0x8060c05:8]=-1
│           0x00000120      48c7831c0802.  mov qword [rbx + 0x2081c], 0xb09020a ; [0xb09020a:8]=-1
│           0x0000012b      660f38008300.  pshufb xmm0, xmmword [rbx + 0x20800]
│           0x00000134      660f38008b10.  pshufb xmm1, xmmword [rbx + 0x20810]
│           0x0000013d      48c783000802.  mov qword [rbx + 0x20800], 0xffffffffbbfd187b
│           0x00000148      48c783040802.  mov qword [rbx + 0x20804], 0x659e79b8 ; [0x659e79b8:8]=-1
│           0x00000153      48c783080802.  mov qword [rbx + 0x20808], 0xffffffffa2d86aa1
│           0x0000015e      48c7830c0802.  mov qword [rbx + 0x2080c], 0x141e7326 ; [0x141e7326:8]=-1
│           0x00000169      48c783100802.  mov qword [rbx + 0x20810], 0xfffffffff3dd9253
│           0x00000174      48c783140802.  mov qword [rbx + 0x20814], 0x25fda25 ; [0x25fda25:8]=-1
│           0x0000017f      48c783180802.  mov qword [rbx + 0x20818], 0xffffffffe05c688d
│           0x0000018a      48c7831c0802.  mov qword [rbx + 0x2081c], 0xffffffff8fd2f821
│           0x00000195      660fef830008.  pxor xmm0, xmmword [rbx + 0x20800]
│           0x0000019d      660fef8b1008.  pxor xmm1, xmmword [rbx + 0x20810]
│           0x000001a5      4831c0         xor rax, rax
│           0x000001a8      660f3817c0     ptest xmm0, xmm0
│       ┌─< 0x000001ad      7404           je 0x1b3
│       │   0x000001af      4983cc01       or r12, 1
│       │   ; CODE XREF from fcn.00000000 @ 0x1ad
│       └─> 0x000001b3      660f3817c9     ptest xmm1, xmm1
│       ┌─< 0x000001b8      7404           je 0x1be
│       │   0x000001ba      4983cc01       or r12, 1
│       │   ; CODE XREF from fcn.00000000 @ 0x1b8
│       └─> 0x000001be      48c783000802.  mov qword [rbx + 0x20800], 0x72726f43 ; 'Corr'
│                                                                      ; [0x72726f43:8]=-1
│           0x000001c9      48c783040802.  mov qword [rbx + 0x20804], 0x21746365 ; 'ect!'
│                                                                      ; [0x21746365:8]=-1
│           0x000001d4      48c783080802.  mov qword [rbx + 0x20808], 0x6e6f7257 ; 'Wron'
│                                                                      ; [0x6e6f7257:8]=-1
│           0x000001df      48c7830c0802.  mov qword [rbx + 0x2080c], 0x283a2067 ; 'g :('
│                                                                      ; [0x283a2067:8]=-1
│           0x000001ea      48c7c0010000.  mov rax, 1
│           0x000001f1      48c7c7010000.  mov rdi, 1
│           0x000001f8      4a8db4e30008.  lea rsi, [rbx + r12*8 + 0x20800]
│           0x00000200      48c7c2080000.  mov rdx, 8
│           0x00000207      0f05           syscall
│           0x00000209      48c783000802.  mov qword [rbx + 0x20800], 0xa
│           0x00000214      48c7c0010000.  mov rax, 1
│           0x0000021b      48c7c7010000.  mov rdi, 1
│           0x00000222      488db3000802.  lea rsi, [rbx + 0x20800]
│           0x00000229      48c7c2010000.  mov rdx, 1
└           0x00000230      0f05           syscall
"""

#it's quite long
#in fact it's very long
#but hey

#still, what kind of sicko would write this code
#especially the mov qwords overwriting each other

#first, it writes Enter flag:

#then, it takes 0x20 characters of input and writes them to mmap_base_place_whatever+0x20800

#it stores the first 16 bytes of it in xmm0 and the next 16 bytes in xmm1
#so our flag is split up between xmm0 and xmm1

#then it loads some constants in to xor with it, shuffles the bytes, and another xor

#once it's done, it wants it to be 0
#so our flag is combination of both xors
#and the shuffle - using https://www.felixcloutier.com/x86/pshufb

#PSHUFB performs in-place shuffles of bytes in the destination operand (the first operand) according to the shuffle control mask in the source operand (the second operand).

#https://stackoverflow.com/questions/28837647/assembly-x86-pshufb-128bit-implementation-in-another-language
#damn you harold

#alright, lets get our constants and get going

xor_one_xmm0 = struct.pack("<I", 0x6f22ecec) + struct.pack("<I", 0xc577cb) + \
               struct.pack("<I", 0x261c7fbd) + struct.pack("<I", 0xc1521493)
xor_one_xmm1 = struct.pack("<I", 0xcd8a4abc) + struct.pack("<I", 0x6603e8b0) + \
               struct.pack("<I", 0xed18b686) + struct.pack("<I", 0x7f37c70c)

xor_two_xmm0 = struct.pack("<I", 0xbbfd187b) + struct.pack("<I", 0x659e79b8) + \
               struct.pack("<I", 0xa2d86aa1) + struct.pack("<I", 0x141e7326)
xor_two_xmm1 = struct.pack("<I", 0xf3dd9253) + struct.pack("<I", 0x25fda25) + \
               struct.pack("<I", 0xe05c688d) + struct.pack("<I", 0x8fd2f821)
#the xor constants for first and second xor

#shuffle masks
shuffle_mask_xmm0 = struct.pack("<I", 0xc090d) + struct.pack("<I", 0x20f0b04) + \
               struct.pack("<I", 0x6080a01) + struct.pack("<I", 0x305070e)
shuffle_mask_xmm1 = struct.pack("<I", 0xd04030e) + struct.pack("<I", 0xf070001) + \
               struct.pack("<I", 0x8060c05) + struct.pack("<I", 0xb09020a)

print(xor_one_xmm0.hex())
print(xor_two_xmm0.hex())
print(shuffle_mask_xmm0.hex())

#so, if I shuffle both of the first xor constants appropriately and xor with the second ones
#like magic, the flag will appear

#pshuf is actually very simple
#it's just a mapping for which bytes to put where
#i.e. if it starts 0201, the second byte is placed first, and the first byte is placed second

def pshuf(const, mask):

    new_const = bytearray(const) # no shallow copy for sure definitely
    for i in range(16): #xmmN width = 16 bytes
        new_const[i] = 0 if (mask[i] & 0x80) else const[mask[i] & 15]

    return bytes(new_const)

def inv_pshuf(const, mask):

    new_const = bytearray(const) # no shallow copy for sure definitely
    for i in range(16): #xmmN width = 16 bytes
        new_const[mask[i] & 15] = const[i]

    return bytes(new_const)

def xor(one, two):

    return bytes(a^b for a,b in zip(one,two))

flag_half_one = xor(pshuf(xor_one_xmm0, shuffle_mask_xmm0), xor_two_xmm0)
flag_half_one = inv_pshuf(flag_half_one, shuffle_mask_xmm0)

flag_half_two = xor(pshuf(xor_one_xmm1, shuffle_mask_xmm1), xor_two_xmm1)
flag_half_two = inv_pshuf(flag_half_two, shuffle_mask_xmm1)

print(flag_half_one + flag_half_two)

#I can also do this
#append the mmap instruction bytes to the start
#to jury-rig this
'''
mmap_code = bytes.fromhex("b809000000bf00000000be00100200ba0700000041ba2200000049c7c0ffffffff41b9000000000f054889c3")

with open("oshawk_extracted_asm_rigged", "wb") as f:
    f.write(mmap_code+instruction_bytes)
'''
#that might help testing, if the above didn't work




