with open("message.txt") as message_, open("encrypt.py") as program_:
    message = bytes.fromhex(message_.read())
    program = program_.read().replace("\r\n", "\n")

# Produce the lookup table.
flag_length = (len(message) // 16) - len(program) - 2
lookup = {}
for i, v in enumerate(program, start=flag_length + 2):
    block = message[i * 16:(i + 1) * 16]
    if block in lookup:
        assert lookup[block] == v
    else:
        lookup[block] = v

# Use the lookup table to recover the flag.
for i in range(flag_length):
    block = message[i * 16:(i + 1) * 16]
    print(lookup.get(block, "#"), end="")
