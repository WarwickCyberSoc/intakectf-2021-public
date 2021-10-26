
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

def encrypt(n, e, message, padding):
    padded_message = bytes_to_long(padding.encode()) + bytes_to_long(message.encode())
    #now it's padded, so I'm safe!
    #wait, is that how padding works? I don't google on company time
    
    c = pow(padded_message,e,n)
    
    return hex(c)
    

def decrypt(n, d, message):
    pass
    # TODO does anyone decrypt any more? I don't think so

p = getPrime(2048)
q = getPrime(2048)
n = p*q
e = 7 #it's a bit bigger than 3...

menu = """Enterprise Standard RSA Server
1) Get Public Key
2) Encrypt
3) Decrypt (NYI, not paid enough)
4) Quit
"""

with open("flag.txt", "r") as f:
    flag = f.read()



while True:
    print(menu)
    choice = input("> ")

    if choice == "1":
        print("n: {}\n e: {}".format(hex(n),hex(e)))
    elif choice == "2":
        message = input("Enter your message: ")
        #I'll just use the flag as padding...
        print("Result: {}".format(encrypt(n,e,message,flag)))
    elif choice == "3":
        print("nah")
    elif choice == "4":
        print("Ok goodbye 🗿")
        exit(0)
    else:
        print("??? bro please pick between 1 and 4 i'm on minimum wage don't make me program an error case") 



