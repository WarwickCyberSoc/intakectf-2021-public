from pwn import remote
from z3 import BitVec, RotateLeft, Solver


class XoShiRo256StarStar:
    def __init__(self):
        self.state = [BitVec(f"state{i}", 64) for i in range(4)]

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


def main():
    io = remote("127.0.0.1", 42101)

    rng = XoShiRo256StarStar()
    s = Solver()

    for _ in range(32):
        io.sendlineafter("Enter your guesses: ", "0 0 0 0 0 0")
        io.recvuntil("My numbers were: ")

        numbers = [int(i) for i in io.recvuntil(".", drop=True).split()]
        random = 0
        for number in numbers[::-1]:
            random <<= 6
            random += number

        s.add(rng.next() % (2 ** (6 * 6)) == random)

    print(s.check())

    random = s.model().eval(rng.next()).as_long()
    numbers = []
    for _ in range(6):
        numbers.append(random & 0x3f)
        random >>= 6

    io.sendlineafter("Enter your guesses: ", " ".join(str(number) for number in numbers))

    io.interactive()


if __name__ == '__main__':
    main()
