# Writeup

We have been given a zip archive. If we try and open it we see that it is encrypted.

We can try extracting the hash using `zip2john` and cracking it but this yields no results.

Let's list the files (with technical information) using `7z l -slt zip_crypto.txt`:

```
Listing archive: zip_crypto.zip

--
Path = zip_crypto.zip
Type = zip
Physical Size = 3872651

----------
Path = zip_crypto
Folder = +
Size = 0
Packed Size = 0
Modified = 2021-07-28 05:32:14
Created = 2021-07-28 05:31:25
Accessed = 2021-07-28 05:32:14
Attributes = D
Encrypted = -
Comment = 
CRC = 
Method = Store
Host OS = FAT
Version = 20
Volume Index = 0

Path = zip_crypto/Coil_plastic_and_metal_zippers.jpg
Folder = -
Size = 3872075
Packed Size = 3872087
Modified = 2021-07-28 05:23:55
Created = 2021-07-28 05:32:06
Accessed = 2021-07-28 06:20:56
Attributes = A
Encrypted = +
Comment = 
CRC = C1DEFD8D
Method = ZipCrypto Store
Host OS = FAT
Version = 20
Volume Index = 0

Path = zip_crypto/flag.txt
Folder = -
Size = 44
Packed Size = 56
Modified = 2021-07-28 05:32:58
Created = 2021-07-28 05:32:11
Accessed = 2021-07-28 06:20:55
Attributes = A
Encrypted = +
Comment = 
CRC = FE5888ED
Method = ZipCrypto Store
Host OS = FAT
Version = 20
Volume Index = 0
```

Here we can see that the archive contains two files, `Coil_plastic_and_metal_zippers.jpg` and `flag.txt`. Both files use `ZipCrypto` encryption and `Store` (don't compress) compression.

Doing some research we can discover that `ZipCrypto` is susceptible to a known plaintext attack. The [`bkcrack`](https://github.com/kimci86/bkcrack) tool tells us we need at least 12 bytes of plaintext so unfortunately knowing that the flag starts with `WMG{` is not enough.

Let's consider `Coil_plastic_and_metal_zippers.jpg`. We could perhaps get enough plaintext by guessing the JPEG headers but it would be much easier to see if we can find the original file.

Googling the file name brings us to [here](https://commons.wikimedia.org/wiki/File:Coil_plastic_and_metal_zippers.jpg). Downloading the original file shows us that it has a size of 3,872,075 bytes which is exactly the same as that in the zip. This means we can use this image as our known plaintext.

Now we just need to crack it. With `bkcrack` installed we can run:

```bash
bkcrack -C zip_crypto.zip -c zip_crypto/Coil_plastic_and_metal_zippers.jpg -p Coil_plastic_and_metal_zippers.jpg
```

To get the keys (`a78cc90e 5b5e2c54 dd28b8e2`). Now we can run:

```bash
bkcrack -C zip_crypto.zip -c zip_crypto/flag.txt -k a78cc90e 5b5e2c54 dd28b8e2 -d flag.txt
```

To decrypt `flag.txt` and get the flag.