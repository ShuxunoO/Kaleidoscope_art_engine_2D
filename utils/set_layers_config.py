import os
from file_operations import save_json
import sys
sys.path.append('..')
from CONST_ENV import ENV_PATH as PATH

layerdir_list = os.listdir(PATH.LAYER_PATH)


def initialize_layerinfos(item, layer_path):
    """
    A function that takes in a directory and returns a dictionary.
    
    :param item: the name of the current directory
    :param layer_path: the path of the folder where the layers are stored
    :return: A dictionary with the following structure:
    """

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
layer_list = [initialize_layerinfos(item, PATH.LAYER_PATH)
              for item in layerdir_list]
print(layer_list)
save_json(PATH.DATA_PATH, "layers_config2", layer_list)
