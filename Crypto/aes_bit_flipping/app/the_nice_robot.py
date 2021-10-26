#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


class AES_CBC_PKCS7:
    def __init__(self, aes_key: bytes, aes_iv: bytes):
        self.key = aes_key
        self.iv = aes_iv

    def encrypt(self, data: bytes) -> bytes:
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded_data = pad(data, 16, style="pkcs7")
        encrypted_data = aes.encrypt(padded_data)
        return encrypted_data

    def decrypt(self, encrypted_data: bytes) -> bytes:
        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        return aes.decrypt(encrypted_data)


encryptor = AES_CBC_PKCS7(get_random_bytes(16), get_random_bytes(16))

print(
    """
         __
 _(\    |@@|
(__/\__ \--/ __
   \___|----|  |   __
       \ }{ /\ )_ / _\\
       /\__/\ \__O (__
      (--/\--)    \__/
      _)(  )(_
     `---''---`
"""
)

magical_password = "peter_borris"

print("[Robot]: Welcome to the challenge! Enter the magical password...")
user_input = input("[You]: ")

if magical_password in user_input:
    print("[Robot]: No no no! Try again...")
    exit()

if len(user_input) > 512:
    print("[Robot]: That's way too long!")
    exit()

print("[Robot]: Well, here's your input encrypted...")
print("[Robot]: " + encryptor.encrypt(user_input.encode()).hex())
print("[Robot]: There's no way this can go wrong... Give me the cipher text back.")
print("[Robot]: I bet it still won't be the magical password...")
user_input = input("[You]: ")

if len(user_input) > 512:
    print("[Robot]: That's way too long!")
    exit()

try:
    user_input_hex = bytes.fromhex(user_input)
except Exception as e:
    print("[Robot]: I can't read this non-hex content, I'm a robot!")
    exit()

decrypted_content = encryptor.decrypt(user_input_hex)

if magical_password.encode() in decrypted_content:
    print("[Robot]: Well well well, good job... You fooled me!")

    with open("flag.txt", "r") as flag_file:
        print("[Robot]: " + flag_file.read())
else:
    print("[Robot]: Hahaha! I knew it!")
