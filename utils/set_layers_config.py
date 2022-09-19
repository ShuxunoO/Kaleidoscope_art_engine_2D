import os
from file_operations import save_json
base_path = os.getcwd()

layers_path = os.path.join(base_path,"layers")
data_path = os.path.join(base_path, "data")
layerdir_list = os.listdir(layers_path)
# print(layerdir_list)   #用列表列举当前目录中的文件名

# 以{图层文件夹：[图层列表]}的形式读取图层信息并且存储为json文件
layer_list = [{"trait_type" : item, "layers" : os.listdir(os.path.join(layers_path,item))} for item in layerdir_list]
print(layer_list)
save_json(data_path, "layers_config", layer_list)







