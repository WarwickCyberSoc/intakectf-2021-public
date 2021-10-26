# Writeup

## Static Analysis

Looking at the C source for the `vuln` function:

```c
void vuln(void) {
    char buffer[16];

    printf("Enter your name: ");
    fgets(buffer, 1024, stdin);
    printf("Hello, %s", buffer);

    return;
}
```

We see that this time the if statement has been completely removed. The `win` function is still present but it is never called. To exploit this program we will have to look deeper into the C stack layout.

## Dynamic Analysis

In Buffer Overflow 1 you may have noticed that after displaying the flag the program exited with a segmentation fault. Segmentation faults can occur when the program tries to execute code at a nonsense address. Let's investigate is the same thing occurs with Buffer Overflow 3:

```
gdb ./vuln
r
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

We see that a segmentation fault does indeed occur. Why? Looking at the disassembly it seems that the program is trying to return to the address `0x4141414141414141` (`AAAAAAAA`) which doesn't make sense as there are no instructions at that address so the program crashes.

From this we can learn that the `vuln` functions return address is stored on the stack and we can overwrite this address using our buffer overflow. This means that we can trick the program into returning to any address we choose including the address of the `win` function.

The first thing we need to work out is how much padding we will need to reach the return address. We can work this out by giving a sequence of characters as input and working out where in that sequence the program attempts to return to:

```
r
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
```

The program tries to return to `0x6665646362615a59` (`YZabcdef`) so we need 24 bytes of padding.

The second thing we need is the address of the `win` function. This is as simple as `p win` which gives `0x401152`.

## Exploit

Similarly to Buffer Overflow 2 we can use `printf` to deliver the exploit. `x86-64` addresses are 8 bytes so our `0x401152` address is really `0x0000000000401152`. Again we need to remember to reverse the bytes because of endianness:

```
printf 'AAAAAAAAAAAAAAAAAAAAAAAA\x52\x11\x40\x00\x00\x00\x00\x00\n' | ./vuln
```

Again, we can pipe to `nc` to exploit the remote target.