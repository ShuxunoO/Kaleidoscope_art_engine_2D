dict_1 = {
    "Background": {
        "trait_type": "Background",
        "groupBy": "None",
        "beacon": "None",
        "value": "Dune"
    },
    "Holder": {
        "trait_type": "Holder",
        "groupBy": "None",
        "beacon": "White",
        "value": "White"
    },
    "Eggshell": {
        "trait_type": "Eggshell",
        "groupBy": "Holder",
        "beacon": "None",
        "value": "White_Milky"
    },
    "Pattern": {
        "trait_type": "Pattern",
        "groupBy": "Holder",
        "beacon": "None",
        "value": "White_Wave"
    },
    "Stroke": {
        "trait_type": "Stroke",
        "groupBy": "None",
        "beacon": "mouse",
        "value": "Resignedly"
    },
    "Halo": {
        "trait_type": "Halo",
        "groupBy": "Holder",
        "beacon": "None",
        "value": "White_Angel"
    },
    "Music_Effect": {
        "trait_type": "Music_Effect",
        "groupBy": "Holder",
        "beacon": "None",
        "value": "White_Sonic"
    },
    "Base": {
        "trait_type": "Base",
        "groupBy": "Holder",
        "beacon": "None",
        "value": "White_Gear"
    }
}
# print(dict_1["shuxun"], type(dict_1["shuxun"]))

# dict_1["shuxun"] = 20
# print(dict_1["shuxun"], type(dict_1["shuxun"]))

# print("shuxun" in dict_1)

# for key, value in dict_1.items():
#     print(key, value)
for value in dict_1.values():
    del value["groupBy"]
    del value["beacon"]

print(list(dict_1.values()))
