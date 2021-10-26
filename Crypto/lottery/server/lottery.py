from secrets import randbits

MASK = 2 ** 64 - 1


def rotate_left(x, k):
    return ((x << k) | (x >> (64 - k))) & MASK


class XoShiRo256StarStar:
    def __init__(self):
        self.state = [randbits(64) for _ in range(4)]

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


def main():
    rng = XoShiRo256StarStar()

    print("Welcome to the lottery! Guess my six numbers to win the flag.")

    while True:
        random = rng.next()
        numbers = []
        for _ in range(6):
            numbers.append(random & 0x3f)
            random >>= 6

        try:
            guesses = [int(guess) for guess in input("Enter your guesses: ").split()]
        except ValueError:
            print("Please only enter integers.")
            continue

        if len(guesses) != 6:
            print("Please enter 6 numbers.")
            continue

        if numbers == guesses:
            print(f"""Well done! Here is your flag: {open("flag.txt").read().strip()}.""")
            break
        else:
            print(f"""Unlucky. My numbers were: {" ".join(str(number) for number in numbers)}.""")


if __name__ == '__main__':
    main()
