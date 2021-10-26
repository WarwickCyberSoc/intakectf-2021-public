If we decompile the .exe in dnSpy, we get the main function and another function, which we can see is doing AES encryption/decryption.

```c#
private static byte[] PTKQNxlAmQQQ(string HNNNnacxXXxz, byte[] hBTQQQQ, byte[] FNFNnanAAA)
{
    if (HNNNnacxXXxz == null || HNNNnacxXXxz.Length <= 0 || hBTQQQQ == null || hBTQQQQ.Length == 0 || FNFNnanAAA == null || FNFNnanAAA.Length == 0)
    {
        throw new Exception();
    }
    byte[] FnbhaDqqqq;
    using (Aes fHaQjTAf = Aes.Create())
    {
        fHaQjTAf.Key = hBTQQQQ;
        fHaQjTAf.IV = FNFNnanAAA;
        fHaQjTAf.Mode = CipherMode.ECB;
        ICryptoTransform gFBGaqqq = fHaQjTAf.CreateEncryptor(fHaQjTAf.Key, fHaQjTAf.IV);
        using (MemoryStream GAWcccAAqq = new MemoryStream())
        {
            using (CryptoStream GHSadssAAAA = new CryptoStream(GAWcccAAqq, gFBGaqqq, CryptoStreamMode.Write))
            {
                using (StreamWriter IUYmwmlfagq = new StreamWriter(GHSadssAAAA))
                {
                    IUYmwmlfagq.Write(HNNNnacxXXxz);
                }
                FnbhaDqqqq = GAWcccAAqq.ToArray();
            }
        }
    }
    return FnbhaDqqqq;
}
```

The first argument is the plaintext, second argument is key and the third argument is the AES. This function is used to encrypt the user's password input and then compared to `hHVVaaaaQQ`.

```c#
string tHQHNNAA = Console.ReadLine();
...
byte[] jhs = Program.PTKQNxlAmQQQ(tHQHNNAA, gxxx, QTQSss);

if (jhs.SequenceEqual(hHVVaaaaQQ) && 432 > QTQSss.Length && hGAXXQAqqq.Next(0, NHAAqq.Length) > 4745)
{
    for (int ggrwe = 0; ggrwe < GnQNAA.Length; ggrwe++)
    {
        Console.Write(Convert.ToChar((int)((char)GnQNAA[ggrwe] ^ tHQHNNAA[ggrwe % tHQHNNAA.Length])));
    }
}
```

We can take `hHVVaaaaQQ` and decrypt it with the AES Key/IV.

AES Key = `gxxx` = `113 109 168 112 209 58 221 109 155 133 249 199 54 132 226 25` = `71 6d a8 70 d1 3a dd 6d 9b 85 f9 c7 36 84 e2 19`

AES IV = `QTQSss` = `137 142 36 84 16 29 199 68 117 141 232 17 95 210 173 53` = `89 8e 24 54 10 1d c7 44 75 8d e8 11 5f d2 ad 35`

We can then put this into Cyberchef with AES in ECB mode:

https://gchq.github.io/CyberChef/#recipe=From_Decimal('Space',false)AES_Decrypt(%7B'option':'Hex','string':'716da870d13add6d9b85f9c73684e219'%7D,%7B'option':'Hex','string':'898e2454101dc744758de8115fd2ad35'%7D,'ECB','Raw','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)&input=NjMgODIgMjQwIDUzIDcgMjU0IDE4OCA4MCAyNDggMzUgMTczIDE3MSA4IDUwIDkxIDkxIDIxOCA4NCA1IDYyIDkyIDU2IDE4OSA2MCA0MyA5OCAzIDExMCAxOSAxMjggODIgMTI1

This yields the password `BishBashBosh_NiceJob`. This is then used to XOR `GnQNAA` which can be done in CyberChef:

https://gchq.github.io/CyberChef/#recipe=From_Decimal('Space',false)XOR(%7B'option':'UTF8','string':'BishBashBosh_NiceJob'%7D,'Standard',false)&input=MjEgMzYgNTIgMTkgNTMgODUgNTggOTUgMjkgMzQgMTAgNTUgMTA2IDEyNiA2MCA0OSAzOCAxMjEgNDggMTEgMTE5IDU0IDM3IDEgMTE5IDggNzUgNCAxMTMgNDggNzYgNzMgMCAxMjYgMzMgNjAgMTEgMTIyIDc4IDMx

Which gives us the flag `WMG{w4I7_My_50URC3_i5_Vi5i8l3_?!_0H_n0!}`.
