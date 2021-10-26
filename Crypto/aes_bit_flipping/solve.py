# Fill the first 16 bytes with whatever
# We will then flip the d to an e (which is at position 5)
print("Send to the robot: AAAAAAAAAAAAAAAAAAAApdter_borris")
encrypted_input = input("What was the cipher text the robot gave: ")

aes_iv = bytearray.fromhex(encrypted_input[:16])
message = bytearray.fromhex(encrypted_input[16:])


def bitFlip(pos, bit, raw):
    list1 = list(raw)
    list1[pos] = chr(ord(list1[pos]) ^ bit)
    raw = "".join(list1)
    return raw


# Flip a single bit in the IV, causing a single bit flip in the message
aes_iv[5] = aes_iv[5] ^ 1

# Recombine the cipher text
print("Give the robot this: " + (aes_iv + message).hex())
