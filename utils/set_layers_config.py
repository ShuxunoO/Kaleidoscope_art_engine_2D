import os
from file_operations import save_json
base_path = os.getcwd()
layers_path = os.path.join(base_path,"layers")
print(layers_path)
data_path = os.path.join(base_path, "data")
layerdir_list = os.listdir(layers_path)
print(layerdir_list)

def add_layerinfos(item, layer_path):
    print("haha")
    layers_list = os.listdir(os.path.join(layer_path,item))
    print(layers_list)

    return {"trait_type" : item,
    "layers" : [
        {layer_name:{"path":os.path.join(layer_path, item, layer_name),
        "weight":1,
        "counter":10} for layer_name in layers_list}
    ]}


# 以{图层文件夹：[图层列表]}的形式读取图层信息并且存储为json文件
layer_list = [add_layerinfos(item, layers_path) for item in layerdir_list]
print(layer_list)
save_json(data_path, "layers_config", layer_list)







