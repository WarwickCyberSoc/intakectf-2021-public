
from Crypto.Util.number import getPrime, inverse, bytes_to_long

p = getPrime(2048)
q = getPrime(2048)

n = p*q

d = 13371337

phi = (p-1)*(q-1)
e = inverse(d, phi)

m = bytes_to_long(b"WMG{its_about_how_you_use_it}")
c = pow(m,e,n)

with open("output.txt","w") as f:
    f.write("n: " + hex(n) + "\n")
    f.write("e: " + hex(e) + "\n")
    f.write("c: " + hex(c) + "\n")






