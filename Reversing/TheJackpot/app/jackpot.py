#!/usr/bin/env python3
import time
import random

icons = {
    "seven": [],
    "cherry": [],
    "diamond": [],
    "lemon": [],
    "melon": [],
    "plum": [],
}

padding_char = "\x1b[38;5;123;48;5;232m "
clear_char = "\x1b[0m"
width = 40
height = 30

for icon in icons.keys():
    with open(f"ans_files/{icon}.ans", "r") as ans_file:
        icon_art = ans_file.read().strip()

        lines = len(icon_art.split("\n"))
        padding_top = (height - lines) // 2
        padding_bottom = ((height - lines) // 2) + (lines % 2)

        for _ in range(padding_top):
            icons[icon].append((padding_char * width) + clear_char)

        for line in icon_art.split("\n"):
            icons[icon].append(line.strip())

        for _ in range(padding_bottom):
            icons[icon].append((padding_char * width) + clear_char)

column = "\x1b[38;5;123;48;5;233m " * 3


def print_sequence(icon1, icon2, icon3):
    for line in range(height):
        print(
            icons[icon1][line]
            + column
            + icons[icon2][line]
            + column
            + icons[icon3][line]
            + clear_char
        )


def print_random_sequence(sleep, reset_cursor_pos=True):
    icon_list = list(icons.keys())
    while True:
        # no winners for the random!!!
        random1, random2, random3 = (
            random.choice(icon_list),
            random.choice(icon_list),
            random.choice(icon_list),
        )
        if not (random1 == "seven" and random2 == "seven" and random3 == "seven"):
            break

    print_sequence(
        random.choice(icon_list),
        random.choice(icon_list),
        random.choice(icon_list),
    )
    time.sleep(sleep)
    if reset_cursor_pos:
        reset_cursor()


def reset_cursor():
    print("\033[1000D\033[30A", end="")


username = ""
while username == "":
    username = input(
        "Please enter your name so we can give you your jackpot if you win: "
    )

# Lets get those wheels spinning

for _ in range(7):
    print_random_sequence(0.5)

for _ in range(4):
    print_random_sequence(0.75)

for _ in range(3):
    print_random_sequence(1)

random.seed(username)

if (
    random.randint(1, 128) == 128
    and random.randint(1, 128) == 128
    and random.randint(1, 128) == 128
):
    print_sequence("seven", "seven", "seven")
    print("You win!")
    with open("flag.txt", "r") as flag:
        print(flag.read())
else:
    print_random_sequence(1, reset_cursor_pos=False)
    print("You lose :(")
