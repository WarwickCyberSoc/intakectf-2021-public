import os
import struct

with open("flag.png", "r") as f:
    data = f.read()

for height in range(1,1000):
    for width in range(1,1000):
        newwidth = struct.pack(">L", width)
        newheight = struct.pack(">L", height)

        newdata = data[:0x10] + newwidth + newheight + data[0x18:]

        with open("flag_fixed.png", "w") as f:
            f.write(newdata)

        res = os.popen("pngcheck -v flag_fixed.png").read()
        if "ERRORS DETECTED" in res:
            print(res)
            pass
        else:
            print("Got right width,height: %i,%i" % (width, height))
            exit(0)
