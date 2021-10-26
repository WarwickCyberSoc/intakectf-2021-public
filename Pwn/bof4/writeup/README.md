# Writeup

## Static Analysis

There are quite a few changes to the C source code this time.

There are two new global variables, `target` and `pointer`:

```c
char target[] = "cat flag.txt";
long pointer = 0;
```

There is a new `increment` function that increments `pointer`:

```c
void increment(void) {
    pointer++;
    return;
}
```

And a new `shift` function that left shifts `pointer` by 1:

```c
void shift(void) {
    pointer <<= 1;
    return;
}
```

Finally, `win` has changed so that it takes `pointer` as the argument rather than the usual `cat flag.txt` string:

```c
void win(void) {
    system((char *)pointer);
    return;
}
```

This means we will have to find a way of making `pointer` point to `target` so we can return to `win` and `cat flag.txt` will be executed.

## Dynamic Analysis

Let's do some investigation:

```
gdb ./vuln
r
CTRL+C
f 6
b 30
c
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
```

We started the program, set a breakpoint after the `fgets` line and entered our padding identifying sequence. Now that we have hit the breakpoint we can use `gdb` to modify the return address to the address of `increment` with `set *(void **)($rbp + 8) = increment`. `rbp` contains the address of the saved base pointer which sits just above the return address so `$rbp + 8` is the address of the return address. The `*(void **)` casts this address to a void pointer pointer and then dereferences it to a void pointer which allows us to set it to the address of `increment`.

After continuing with `c` the program crashes with a segmentation fault. `p pointer` shows that `pointer` has indeed been incremented by the `increment` function. We fault trying to return to `0x6e6d6c6b6a696867` (`ghijklmn`) which is 32 bytes into the sequence (8 more than with the first return). So it seems we can return to address after address by simply placing them consecutively on the stack. This is known as a ROP chain.

Using a ROP chain we can return to some sequence of `increment`s and `shift`s to make `pointer` point to `target` and then return to `win` to get the flag.

## Exploit

For this exploit we are going to use Pwntools which is a Python library for rapid exploit development. We can generate a template script with:

```
pwn template vuln --host 127.0.0.1 --port 42004 --quiet > exploit.py
```

Here `vuln` is the name of the local binary, `--host` and `--port` specify the remote host and port and `--quiet` reduces the number of comments that are produced. After generating the exploit we pipe it into the `exploit.py` file.

The template does some basic setup that makes it easy to interact with the program. For example, we can use `io.send`, `io.sendline`, `io.sendafter` and `io.sendlineafter` to send text to the program; we can use `io.recv`, `io.recvline` and `io.recvuntil` to receive text from the program.

It also makes it easy to get information about the binary. For example we can use `exe.sym.target` to get the address of the `target` symbol or `exe.sym.win` to get the address of the `win` symbol.

There are also various utility functions for converting data to bytes. `flat` is the most useful of these as it is automatically configured based on the program's architecture and can convert complex data structures such as nested lists and dictionaries.

If we take a binary number such as `0b10` and shift it left by 1 we get `0b100`. If we do it again we get `0b1000`. We observe that shifting left by 1 appends a 0 to the binary number.

Now, if we take `0b10`, shift it left by 1 and then add 1 we get `0b101`. If we do it again we get `0b1011`. We observe that shifting left by 1 and adding 1 appends a 1 to the binary number.

Using these two facts we can make `pointer` point to `target` by iterating over the binary address of `target` and calling `shift` if there is a 0 or `shift` followed by `increment` if there is a 1. The following Python code will build a list of addresses based on this principle:

```python
payload = []
for bit in f"{exe.sym.target:b}":
    payload.append(exe.sym.shift)
    if bit == "1":
        payload.append(exe.sym.increment)
```

Notice that it makes use of `exe.sym` to get addresses from the binary using Pwntools.

After this we need to call `win` so let's append that to the list:

```python
payload.append(exe.sym.win)
```

We have just contracted a ROP chain. If we overflow the buffer so that `vuln` returns to the start of the chain, each function will be executed and the flag will be displayed. This can be achieved using `io.sendlineafter` and `flat`:

```python
io.sendlineafter("Enter your name: ", flat({
    24: payload
}))
```

The completed exploit can be found in `exploit.py`. There are also Pwntools exploits for the previous challenges. It can be run locally with:

```
python exploit.py LOCAL
```

Or remotely with:

```
python exploit.py
```

