import os
from file_operations import save_json
base_path = os.getcwd()
layer_path = os.path.join(base_path, "layers")
data_path = os.path.join(base_path, "data")
layerdir_list = os.listdir(layer_path)
print(layerdir_list)


def initialize_layerinfos(item, layer_path):
    temp_dict = {}
    current_dir = os.path.join(layer_path, item)
    print(current_dir)
    layer_list = os.listdir(current_dir)  # 将当前文件夹中的文件列出来
    for tempt_item in layer_list:  # 遍历文件夹中的文件
        if os.path.isdir(os.path.join(current_dir, tempt_item)):
            print("dir")
            temp_dict ["trait_type"] = item
            sublayer_list = os.listdir(os.path.join(current_dir, tempt_item))  # current dir has subdir
            temp_dict[tempt_item] = [{tempt_sublayer:{
                "path" : os.path.join(current_dir, tempt_item, tempt_sublayer),
                "weight": 10,
                "counter" : 2,
                "conflictElements": "xxx"
            }} for tempt_sublayer in sublayer_list]
        else:
            print("file")
            temp_dict ["trait_type"] = item
            temp_dict["layers"] = [{tempt_sublayer: {
                "path": os.path.join(current_dir, tempt_sublayer),
                "weight": 10,
                "counter": 2,
                "conflictElements": "xxx"
            }} for tempt_sublayer in os.listdir(current_dir)]
    return temp_dict



# 以{图层文件夹：[图层列表]}的形式读取图层信息并且存储为json文件
layer_list = [initialize_layerinfos(item, layer_path)
              for item in layerdir_list]
print(layer_list)
save_json(data_path, "layers_config", layer_list)