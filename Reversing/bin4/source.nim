#comments from other solution
import strformat
import base64

proc gimmeKey(): string {.discardable.} = 
    var b64d: string="AREUCw8APgwXHCwcBy0bFw46AQ0ICDsBEhEANwkREkAV"
    var cp: string = decode(b64d)
    var key: string="rtwyjtagresrhrtykevddddddtrhndw3f"
    var result=""
    for i in 0..<cp.len:
        result.add( chr(int(key[i]) xor int(cp[i])))
    return result

stdout.write("Enter password: ")
var key = readLine(stdin)
gimmeKey()
var flag: array[34,byte] = [byte 0x24, 0x28, 0x24, 0x09, 0x1d, 0x44, 0x2d, 0x5a, 0x0b, 0x1e, 0x00, 0x0a, 0x5f, 0x6c, 0x5a, 0x00, 0x42, 0x2b, 0x28, 0x5a, 0x02, 0x0f, 0x2d, 0x1c, 0x06, 0x31, 0x2d, 0x2c, 0x50, 0x00, 0x03, 0x15, 0x0e, 0x0a]
var result=""
for i in 0..<key.len:
    result.add( chr(int(key[i]) xor int(flag[i])))

echo fmt"Decrypted Secret: {result}"
