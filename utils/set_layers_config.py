import os
from file_operations import save_json
base_path = os.getcwd()
layer_path = os.path.join(base_path, "layers")
data_path = os.path.join(base_path, "data")
layerdir_list = os.listdir(layer_path)
print(layerdir_list)


def initialize_layerinfos(item, layer_path):
    current_dir = os.path.join(layer_path, item)
    if os.path.isdir(current_dir):
        print("dir")
        layer_list = os.listdir(os.path.join(layer_path, item))
        print(layer_list)
        return {"trait_type": item,
                "layers": [
                    {layer: {"path": os.path.join(layer_path, item, layer),
                             "weight": 1,
                             "counter": 10} for layer in layer_list}
                ]}
    else:
        print("file")
        return {"trait_type": item,
                "layers": [
                    {item: {"path": os.path.join(layer_path, item, item)}}
                ]}


# 以{图层文件夹：[图层列表]}的形式读取图层信息并且存储为json文件
layer_list = [initialize_layerinfos(item, layer_path)
              for item in layerdir_list]
print(layer_list)
save_json(data_path, "layers_config", layer_list)