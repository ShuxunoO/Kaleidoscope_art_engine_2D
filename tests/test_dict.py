# dict1 = {"shuxun" : "25"}
# dict2 = {"xiaobang" : "18"}
# def update_dict(dict1, dict2):
#     dict1.update(dict2)

# # print(dict1)
# # update_dict(dict1, dict2)
# # print(dict1)

# print("shuxun" in dict1)

layer_dict = {}
layer_list = [
                {
                    "Blue_Green": {
                        "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Eggshell\\Blue\\Blue_Green.png",
                        "weight": -1
                    }
                },
                {
                    "Blue_Purple": {
                        "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Eggshell\\Blue\\Blue_Purple.png",
                        "weight": -1
                    }
                }
]

for item in layer_list:
    print(list(item.values())[0]["weight"])