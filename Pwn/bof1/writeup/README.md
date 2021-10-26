# Writeup

## Static Analysis

Looking at the C source code we see that there are 3 functions: `main`, `vuln` and `win`. If we take a look at the `win` function:

```c
void win(void) {
    system("cat flag.txt");
    return;
}
```

we see that it uses `cat` to display the flag. This means that our objective is to find a way of running this function.

Now let's look at `main`:

```c
int main(int argc, char *argv[]) {
    // Disable buffering.
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    vuln();
    return 0;
}
```

The `setvbuf` calls are just to make sure that the program outputs data as soon as it is available. After these we have a call to `vuln` and `main` returns which exits the program.

Finally we can analyse the `vuln` function:

```c
void vuln(void) {
    long check = 0x0123456789abcdef;
    char buffer[16];

    printf("Enter your name: ");
    fgets(buffer, 1024, stdin);
    printf("Hello, %s", buffer);

    if (check != 0x0123456789abcdef) {
        win();
    }

    return;
}
```

which does the following:

- Declare two variables, `check` (a long integer) and `buffer` (a 16 character array).
- Output the message `Enter your name: ` using `printf`.
- Accept user input of up to 1024 characters and store them in `buffer`.
- Output `Hello, ` followed by the users input.
- Test if the `check` variable is different to the initial value; if it is then run the `win` function.

Since the `win` function outputs the flag our objective must be to modify the `check` value in order to pass the if condition. There is, however, no obvious way of doing this since there are no lines that modify `check` after its declaration.

One oddity does exist in the code; `buffer` is only declared to hold 16 characters however the user can populate it with up to 1024.  We can use this bug as the basis of our exploit.

## Dynamic Analysis

We will be using `gdb` with the `pwndbg` plug-in for our analysis.

We'll start by opening the `vuln` binary in `gdb` with `gdb ./vuln`. Now let's run it with `r` (short for `run`). We are greeted with the prompt asking for our name.

At this point we can hit `CTRL+C` break into the debugger. We are given a lot of information by `pwndbg` but since we broke in the middle of a `libc` function it is not overly useful. We can use `f 6` (short for `frame 6`) followed by `context` to switch to the `vuln` stack frame and see what is going on.

Now we can take a look at our two variables; `p buffer` (short for `print buffer`) shows us that `buffer` is currently just filled with gibberish and `p/x check` (the `x` is for hexadecimal) shows us that `check` is indeed  still `0x0123456789abcdef`.

We can now set a breakpoint on line 17 (the next line) with `b 17` (short for `break 17`) and continue execution until that point with `c` (short for `continue`). The program presents us with a blank line as it is sill waiting for us to input our name. We will just input `AAAA` for now and press return.

Now if we print our variables we see that `buffer` now holds `AAAA` and `check` still holds `0x0123456789abcdef`. We can check the locations of these variables in memory with `p &buffer` which gives `0x7fffffffdf30` and `p &check` which gives `0x7fffffffdf48`. The addresses you get but the difference between them (`0x18 = 24`) should be the same. This means that if we fill the buffer with more than 24 characters we can overwrite `check` and therefore pass the if condition.

`gdb` can be exited with `q` (short for `quit`).

## Exploit

Let's first try to exploit the program locally. We can run it with `./vuln` and when prompted enter 32 `A`s which should be more than enough to overwrite `check`. We see that our exploit has worked as we get `WMG{not_that_easy}` (the contents of `flag.txt`) in the output.

To test that our exploit also works in the remote environment we can run the docker container with the instructions provided at the top of `Dockerfile`:

```
sudo docker build -t wmg_ctf_2021_pwn_bof_1 .
sudo docker run -d -p 42001:42001 wmg_ctf_2021_pwn_bof_1
```

Connecting to this with `nc 127.0.0.1 42001` and entering 32 `A`s shows us that the exploit also works remotely. We now just need to connect to the challenge server and do the same thing to get the flag.