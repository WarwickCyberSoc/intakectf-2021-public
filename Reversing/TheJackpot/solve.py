import random
import os

import time

# so lets it's seeded with

while True:
    hex_val = os.urandom(8).hex()
    random.seed(hex_val)

    if (
        random.randint(1, 128) == 128
        and random.randint(1, 128) == 128
        and random.randint(1, 128) == 128
    ):
        print("Use this value to win: " + hex_val)
        print("You win!")
        break

# Win value: 8b9eb5c5bc1c6001
