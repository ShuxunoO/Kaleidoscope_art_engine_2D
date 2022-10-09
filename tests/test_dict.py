# dict1 = {"shuxun" : "25"}
# dict2 = {"xiaobang" : "18"}
# def update_dict(dict1, dict2):
#     dict1.update(dict2)

# # print(dict1)
# # update_dict(dict1, dict2)
# # print(dict1)

# print("shuxun" in dict1)

layer_dict = {}
layer_list = {
    "Blue": {
                "layer_list": [
                    "Blue_Block",
                    "Blue_Chaos",
                    "Blue_Constellation",
                    "Blue_Deepmind",
                    "Blue_Honeycomb",
                    "Blue_Maze",
                    "Blue_Mirror",
                    "Blue_Neurons",
                    "Blue_Pixel",
                    "Blue_Recursion",
                    "Blue_Starburst",
                    "Blue_Vortex",
                    "Blue_Wave"
                ],
                "Blue_Block": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Block.png",
                    "weight": -1
                },
                "Blue_Chaos": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Chaos.png",
                    "weight": -1
                },
                "Blue_Constellation": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Constellation.png",
                    "weight": -1
                },
                "Blue_Deepmind": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Deepmind.png",
                    "weight": -1
                },
                "Blue_Honeycomb": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Honeycomb.png",
                    "weight": -1
                },
                "Blue_Maze": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Maze.png",
                    "weight": -1
                },
                "Blue_Mirror": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Mirror.png",
                    "weight": -1
                },
                "Blue_Neurons": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Neurons.png",
                    "weight": -1
                },
                "Blue_Pixel": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Pixel.png",
                    "weight": -1
                },
                "Blue_Recursion": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Recursion.png",
                    "weight": -1
                },
                "Blue_Starburst": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Starburst.png",
                    "weight": -1
                },
                "Blue_Vortex": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Vortex.png",
                    "weight": -1
                },
                "Blue_Wave": {
                    "path": "C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Pattern\\Blue\\Blue_Wave.png",
                    "weight": -1
                }
            }
}

for item in layer_list["Blue"]["layer_list"]:
    item_info = layer_list["Blue"][item]
    print(item_info["weight"])
    weight = item_info["weight"]
    weight = 100
    print(item_info["weight"])
    item_info["weight"] = 100
    print(item_info["weight"])
