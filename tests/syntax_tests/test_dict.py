dict_1 = {"shuxun": "unknown", "xidian":"hahaha"}
# print(dict_1["shuxun"], type(dict_1["shuxun"]))

# dict_1["shuxun"] = 20
# print(dict_1["shuxun"], type(dict_1["shuxun"]))

# print("shuxun" in dict_1)

# for key, value in dict_1.items():
#     print(key, value)

print(list(dict_1.values()))
del dict_1["xidian"]
print(dict_1)