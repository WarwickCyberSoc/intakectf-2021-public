import gmpy2
from Crypto.Util.number import long_to_bytes

# Enter the cipher text from output.txt
ct = 0x0A27256B2234CF39831350314B8C6B9ECC548A1E72327626E29F2882C0AADF7E985677A09410498DC510BE21CF3FD810BDB2C7ED345297EB82AAD8AE07E0354AF00352EFF39AAF41D8708FBF244F5D94052C0C54355CDF054E1EE2DCBBDEA7A8049799AEDD65

# Ensure gmpy2 doesn't cut off any precision
gmpy2.get_context().precision = 2000

# Take the e'th root (in this case, 3)
flag = gmpy2.root(ct, 3)

# Convert to bytes
flag = long_to_bytes(flag)

# This attack works due to the lack of padding and that the message length is less than the cube root of N
print(flag)
