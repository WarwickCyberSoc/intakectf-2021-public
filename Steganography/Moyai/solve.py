
"""
flag = u"WMG{🗿_🗿_🗿}".encode()
print(flag)
binstring = "".join(bin(i)[2:].zfill(8) for i in flag)
with open("moyai.txt", "w") as f:
    f.write(binstring.replace("1","\u200d").replace("0","🗿"))
"""
#the generation code

with open("moyai.txt", "r") as f:
    data = f.read()
    
moyai = "🗿"
zerowidth = u"\u200d"

binary = data.replace(moyai, "0").replace(zerowidth, "1")

print(binary)

res = ""
for i in range(0,len(binary)//8):
    res += hex(int("".join(binary[i*8:(i+1)*8]),2))[2:].zfill(2)

print(res)
print(bytes.fromhex(res).decode())