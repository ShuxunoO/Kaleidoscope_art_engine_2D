import re
str1 = "shuxun#20.png"
str2 = "ipfs://16551651sgsgf/54561511585.png"
str3 = "BanaCat #1564"
# print(re.split("[#.]", str1))
str2 = re.sub(r"""/[0-9]*.png""", "/3333.png", str2)
print(str2)
str3 = re.sub(r"""\#[0-9]*""", "#3333", str3)
print(str3)