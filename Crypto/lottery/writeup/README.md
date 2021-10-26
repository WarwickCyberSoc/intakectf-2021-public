# Writeup

## Analysis

Let's start by reviewing the code in the `main` function:

```python
def main():
    rng = XoShiRo256StarStar()

    print("Welcome to the lottery! Guess my six numbers to win the flag.")

    while True:
        random = rng.next()
        numbers = []
        for _ in range(6):
            numbers.append(random & 0x3f)
            random >>= 6
```

The program starts by instantiating a class called `XoShiRo256StarStar`. Looking this name up shows us that it is a psuedo-random number generator. The program then enters a loop. It generates a number with `rng.next()` and then uses a combination of shifts and masking to split the number into six parts.

```python
        try:
            guesses = [int(guess) for guess in input("Enter your guesses: ").split()]
        except ValueError:
            print("Please only enter integers.")
            continue

        if len(guesses) != 6:
            print("Please enter 6 numbers.")
            continue
```

Now the program takes input from the user in the form of six integers. Checks are done to ensure that the user's input is valid.

```python
        if numbers == guesses:
            print(f"""Well done! Here is your flag: {open("flag.txt").read().strip()}.""")
            break
        else:
            print(f"""Unlucky. My numbers were: {" ".join(str(number) for number in numbers)}.""")
```

For the final part of the loop, the program compares the user's inputs with the random six parts generated earlier. If they match then the flag is outputted. Otherwise the user is told the six random parts and can try again.

Now let's take a look at the `XoShiRo256StarStar` class:

```python
class XoShiRo256StarStar:
    def __init__(self):
        self.state = [randbits(64) for _ in range(4)]
```

It starts of by initializing its state with `secrets.randbits()` (a cryptographically secure random number generator).

```python
    def next(self):
        result = (rotate_left((self.state[1] * 5) & MASK, 7) * 9) & MASK

        temporary = (self.state[1] << 17) & MASK

        self.state[2] ^= self.state[0]
        self.state[3] ^= self.state[1]
        self.state[1] ^= self.state[2]
        self.state[0] ^= self.state[3]

        self.state[2] ^= temporary

        self.state[3] = rotate_left(self.state[3], 45) & MASK

        return result
```

Afterwards we have the `next` function which manipulates the state to produce a pseudo-random number. The use of `& MASK` keeps the number at 64 bits in line with the C implementation.

Taking a look at [this](https://prng.di.unimi.it/) webpage by the authors of the PRNG reveals that it is not cryptographically secure. This means it may be possible to predict the next output of the generator by observing previous outputs. There are several blog posts discussing how to crack other `Xo(Ro)ShiRo` family generators but none provide a solution for `XoShiRo256**`. This means we will have to get creative.

## Solution

Z3 is a theorem prover. If you can properly formulate a problem then there is a good chance that Z3 will be able to solve it. Luckily for us the `z3-solver` library provides Python bindings that make formulation a lot easier. We will also be using `pwntools` to communicate with the server.

We will start by recreating the `XoShiRo256StarStar` class in a way that Z3 can understand. Instead of initialising the state with random values, we can populate it with Z3 symbols that can later be solved. `BitVec` allows us to create a symbolic integer of a given size (in our case this is 64 bits). We also need to provide a name for each (we will use `state0` to `state3`):

```python
class XoShiRo256StarStar:
    def __init__(self):
        self.state = [BitVec(f"state{i}", 64) for i in range(4)]
```

The Z3 implementation of the `next` method should actually be simpler than the plain Python version; we don't need to worry about masking as the `BitVec`s are already limited to 64 bits and Z3 provides a `RotateLeft` function so we don't need to write our own. Normal python operations such as multiplying, left shifting and XORing also just work with Z3 symbols:

```python
    def next(self):
        result = RotateLeft(self.state[1] * 5, 7) * 9

        t = self.state[1] << 17

        self.state[2] ^= self.state[0]
        self.state[3] ^= self.state[1]
        self.state[1] ^= self.state[2]
        self.state[0] ^= self.state[3]

        self.state[2] ^= t

        self.state[3] = RotateLeft(self.state[3], 45)

        return result
```

Now we need to write the code that interacts with the server. We'll use `pwn.remote` as it is far easier than using Python sockets. We'll also instantiate our `XoShiRo256StarStar` class and create a Z3 `Solver` object:

```python
def main():
    io = remote("127.0.0.1", 42101)

    rng = XoShiRo256StarStar()
    s = Solver()
```

Following an incorrect guess, the server tells us what the numbers should of been. We can then reverse the shifting and masking to reveal the least significant 36 bits of the server's `random`. Using `s.add` we can tell the Z3 solver that the symbolic lowest 36 bits of our `rng.next()` should be equal to the reconstruction. Doing this enough times (we're doing 32) should allow the solver to deduce the initial state and thus the next output:

```python
    for _ in range(32):
        io.sendlineafter("Enter your guesses: ", "0 0 0 0 0 0")
        io.recvuntil("My numbers were: ")

        numbers = [int(i) for i in io.recvuntil(".", drop=True).split()]
        random = 0
        for number in numbers[::-1]:
            random <<= 6
            random += number

        s.add(rng.next() % (2 ** (6 * 6)) == random)
```

To make Z3 actually process our inputs we use `s.check()` which should return `sat` if all the conditions we added were satisfiable. Following that we can use the solver's model to evaluate the next `rng.next()` output and use the same code as the server to split it into 6 numbers. Sending these numbers to the server should then give the flag:

```python
    print(s.check())

    random = s.model().eval(rng.next()).as_long()
    numbers = []
    for _ in range(6):
        numbers.append(random & 0x3f)
        random >>= 6

    io.sendlineafter("Enter your guesses: ", " ".join(str(number) for number in numbers))

    io.interactive()
```

The full script can be found in `solve.py`.
