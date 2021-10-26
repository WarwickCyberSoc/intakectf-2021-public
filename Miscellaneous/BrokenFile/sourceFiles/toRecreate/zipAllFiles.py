import os
os.system("tar -czvf folder.tar.gz challenge.png message.txt")
os.system("tar -czvf 0.tar.gz folder.tar.gz")

start="0.tar.gz"

lastFile = start
for i in range(1000):
    os.system(f"tar -czvf {str(i)}.tar.gz {lastFile}")
    os.remove(lastFile)
    lastFile=f"{i}.tar.gz"
