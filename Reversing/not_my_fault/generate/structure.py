from random import choice, randint, shuffle
from sys import argv
from uuid import uuid4

from pwn import asm, context, u32

flag = b"WMG{sigsegv_not_for_me_9fd9bd4d}"
replacements = {}

context.arch = "amd64"

# Calculate which pages can will cause segfaults.
prot_bits = 0x572039efb49fc8cb
valid_read_pages = []
invalid_read_pages = []
valid_write_pages = []
invalid_write_pages = []
for page in range(0, 0x1000 * 32, 0x1000):
    if prot_bits & 0b01:
        valid_read_pages.append(page)
    elif not prot_bits & 0b10:  # Write can imply read.
        invalid_read_pages.append(page)

    if prot_bits & 0b10:
        valid_write_pages.append(page)
    else:
        invalid_write_pages.append(page)

    prot_bits >>= 2

# Create the XOR variables.
xor_mask = bytes(randint(0, 255) for _ in range(32))
flag_ = []
for i in range(32):
    flag_.append(flag[i] ^ xor_mask[i])

for i in range(8):
    replacements[f"flag_{i // 4 + 1}_xor_{i % 4 + 1}"] = str(u32(xor_mask[i * 4:(i + 1) * 4], signed=True))

flag = bytes(flag_)
print(flag)

# Create the shuffle variables.
flag_ = [0] * 32
for flag_part in range(1, 3):
    shuffle_control_mask = list(range(16))
    shuffle(shuffle_control_mask)
    shuffle_control_mask = bytes(shuffle_control_mask)

    for i, v in enumerate(shuffle_control_mask):
        flag_[(flag_part - 1) * 16 + i] = flag[(flag_part - 1) * 16 + v]

    for shuffle_part in range(1, 5):
        replacements[f"flag_{flag_part}_shuffle_{shuffle_part}"] = str(u32(shuffle_control_mask[(shuffle_part - 1) * 4:shuffle_part * 4], signed=True))

flag = bytes(flag_)
print(flag)

# Create the compare variables.
for i in range(8):
    replacements[f"flag_{i // 4 + 1}_compare_{i % 4 + 1}"] = str(u32(flag[i * 4:(i + 1) * 4], signed=True))

# Assemble each block of the hidden assembly.
with open("hidden.asm") as f:
    hidden = f.read().replace("\r\n", "\n").replace("[", "ptr [").rstrip()

    # Set the dynamically created variables.
    for k, v in replacements.items():
        hidden = hidden.replace(k, v)

    hidden_blocks = [asm(hidden_block.split("  ;")[0] + "\n    ret") for hidden_block in hidden.split("\n\n")]

# Create the structure and structure code. Ordering is bizarre to make the assembly simpler.
structure = ["structure_base:"]
structure_code = []
for hidden_block in hidden_blocks:
    structure.append(f"    dq {len(hidden_block) * 8}")
    for hidden_byte in hidden_block[::-1]:
        for hidden_bit in f"{hidden_byte:08b}":
            uuid = f"s{uuid4().hex}"
            structure.append(f"    dq {uuid}")
            structure_code.append(f"{uuid}:")
            if hidden_bit == "1":
                if choice((True, False)):
                    structure_code.append(f"    mov r15, qword [rbx + {choice(valid_read_pages) + randint(0, 0x1000 - 8)}]")
                else:
                    structure_code.append(f"    mov qword [rbx + {choice(valid_write_pages) + randint(0, 0x1000 - 8)}], r15")
            else:
                if choice((True, False)):
                    structure_code.append(f"    mov r15, qword [rbx + {choice(invalid_read_pages) + randint(0, 0x1000 - 8)}]")
                else:
                    structure_code.append(f"    mov qword [rbx + {choice(invalid_write_pages) + randint(0, 0x1000 - 8)}], r15")
            structure_code.append("    ret")
            structure_code.append("")

structure.append("dq 0")

with open("structure.asm", "w") as f:
    f.write("\n".join(structure))

# Shuffle the structure code if not in debug mode.
if "--debug" not in argv:
    structure_code_shuffle = list(range(len(structure_code) // 4))
    shuffle(structure_code_shuffle)

    structure_code_ = [""] * len(structure_code)
    for i, v in enumerate(structure_code_shuffle):
        structure_code_[v * 4] = structure_code[i * 4]
        structure_code_[v * 4 + 1] = structure_code[i * 4 + 1]
        structure_code_[v * 4 + 2] = structure_code[i * 4 + 2]
        structure_code_[v * 4 + 3] = structure_code[i * 4 + 3]

    structure_code = structure_code_

with open("structure_code.asm", "w") as f:
    f.write("\n".join(structure_code))
