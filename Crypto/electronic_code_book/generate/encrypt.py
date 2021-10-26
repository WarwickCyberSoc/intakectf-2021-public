from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

with open("flag.txt") as flag, open(__file__) as program:
    message = flag.read() + "\n\n" + program.read()  # Include a copy of the program for reference.

message = message.replace("\r\n", "\n")  # Make sure the message is the same on all systems.
message = message.encode("utf_16_be")  # Convert the message to bytes so it can be encrypted.
message = "".join(f"{i:08b}" for i in message).encode()  # Cryptography only works with binary data, right?

cipher = AES.new(get_random_bytes(16), AES.MODE_ECB)  # Nobody could ever guess a random key.

with open("message.txt", "w") as f:
    f.write(cipher.encrypt(message).hex())
