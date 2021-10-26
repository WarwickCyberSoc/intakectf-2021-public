#can't be bothered how to fixPicture in bash so cope

import os

def untarEverything():
    os.system("for i in {1000..0}; do tar -xzvf $i.tar.gz; rm $i.tar.gz;done")

def fixPicture():
    with open("challenge.png","rb") as f:
        content = f.read()
    #fix the broken header. Replace only one instance since we only want to change header bytes
    fixedContent = content.replace(b"PNJ",b"PNG",1)

    with open("fixed_challenge.png","wb") as f:
        f.write(fixedContent)

untarEverything()
fixPicture()
