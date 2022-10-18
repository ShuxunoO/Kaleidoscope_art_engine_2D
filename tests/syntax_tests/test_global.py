from glob import glob

path = "../../layers/**"
list1 = glob(path,recursive=True)
for item in list1:
    print(item)