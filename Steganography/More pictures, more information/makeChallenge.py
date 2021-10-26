#turns 30 pictures into flag
#solution: for i in $(seq 1 30); do exiftool $i.png | grep Artist; done
import os
flag="WMG{700_much_metadata_15_b4d}"

for i in range(1,30):
    artist=flag[i-1]
    os.system(f"exiftool -artist='{artist}' {i}.png")
    print(artist)