dict_1 = {"shuxun": "unknown", "xidian":"hahaha"}
# print(dict_1["shuxun"], type(dict_1["shuxun"]))

# dict_1["shuxun"] = 20
# print(dict_1["shuxun"], type(dict_1["shuxun"]))

# print("shuxun" in dict_1)

# for key, value in dict_1.items():
#     print(key, value)

list1 = dict_1.values()
print(list1)

list1 = list(dict_1.values())
print(list1)