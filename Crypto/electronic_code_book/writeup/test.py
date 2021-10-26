from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

message = "test"

message = message.replace("\r\n", "\n")
print(message)
message = message.encode("utf_16_be")
print(message)
message = "".join(f"{i:08b}" for i in message).encode()
print(message)

cipher = AES.new(get_random_bytes(16), AES.MODE_ECB)
print(cipher.encrypt(message).hex())
