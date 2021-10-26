#!/usr/bin/env python3
import time
import string
import random 
import warnings
import re
warnings.simplefilter("ignore",FutureWarning)
letters=list(string.ascii_letters+string.digits)
punc = [char for char in "%&!,:£%_`;@=><~#'"]
#can only concatenate list to list
special = ["[a-z]","[a-zA-Z]",".","\\w","\\W","\\s","\\S","\\d","\\D","\\."]
#some charactrers that break stuff
evenSpecialer = ["\\{","\\}","\\[","\\]","\\(","\\)"]

alphabet=letters+punc+special
specialAlphabet = alphabet+evenSpecialer

modifiers=["?","*","+","()","[]","{}",None]
weights = (4,12,14,20,15,15,10)

pattern="^"
length = 60
backreferences=0
currentNum = 1
while currentNum<length:

    if currentNum%2==0:
        selection=""
        selected = str((random.choices(modifiers,weights=weights,k=1))[0])
        if selected=="None":
            currentNum+=1
            pass
        elif selected=="()":
            backreferences+=1
            charset = ''.join([i for i in random.choices(alphabet,k=random.randint(4,8)) if i in alphabet])
          
            selection=f"({charset})"
            for i in range(5):
                alphabet.append(f"\\{backreferences} ")

  
        elif selected=="{}":
            first = random.randint(2,9)
            second= random.randint(2,18)
            if second%3==0:
                second=""
            else:
                second=first+second
            selection="{"+str(first)+","+ str(second) + "}"
        elif selected=="[]":
            charset = ''.join(random.choices(alphabet,k=random.randint(3,6)))
            if random.randint(0,1)==0:
                selection = "["+charset+"]"
            else:
                selection="[^"+charset+"]"
        else:
            selection=selected
    else:
        selection=random.choice(specialAlphabet)
    
    pattern+=selection
    currentNum+=1


pattern+="$"

print("Match the pattern to get the flag")

print(f"Pattern: {pattern}")
userInput = input("Enter string: ")

if re.match(pattern,userInput):
    print("Flag: WMG{t00_much_r3g3x_pl345e_St0p}")
else:
    print("Invalid string")
