# Writeup

To examine what's going on, let's modify the program to encrypt a test message and output every step of the process:

```python
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
```

This gives us the output:

```
test
b'\x00t\x00e\x00s\x00t'
b'0000000001110100000000000110010100000000011100110000000001110100'
4e8963c8f294949fcf2bc737662d996fa59b58eea2c2def5d9f1b63e9b176216461145bb28fc7a1262c106a6605df1a74e8963c8f294949fcf2bc737662d996f
```

There are a few things to notice:

- After the UTF-16 encoding each character takes up 2 bytes.
- After converting this to binary each character takes up 16 bytes.
- The first 16 bytes of the result and the last 16 bytes of the result are identical.

Because AES has a block size of 16 and the program uses the ECB (raw) mode, identical characters in the input will be represented by identical 16-byte strings in the output.

We can use the fact that the program itself is included in the encrypted message to produce a lookup table and use this to recover the flag.

This is implemented in `solve.py`.