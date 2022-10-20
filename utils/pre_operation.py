import sys
from pathlib import Path
import cv2

from file_operations import load_lsyers_config, save_json, serialize_save, serialize_load
from set_layers_weight import balance_layerweight

sys.path.append('..')
from CONST_ENV import ENV_PATH as PATH

CONFIG = load_lsyers_config(PATH.CONFIG_PATH)
layer_config = CONFIG["layerConfigurations"]
layer_info_path = Path.joinpath(PATH.DATA_PATH, "layers_config_V11.json")
layer_info = load_lsyers_config(layer_info_path)


# 构建一个图层信息字典
def build_layer_info(layerinfo_json):
    layer_info_data = {}
    for key,value in layerinfo_json.items():
        if value["existSubdir"]:
            layer_info_dict = {}
            for dir_item in value["dir_list"]:
                sublayer_info = value[dir_item]
                sublayer_list = sublayer_info["layer_list"]
                for layer in sublayer_list:
                    layer_info_dict.update({layer:sublayer_info[layer]})
            layer_info_data.update({key:layer_info_dict})
        else:
            layer_list = value["layer_list"]
            layer_info_dict = {}
            for layer in layer_list:
                layer_info_dict.update({layer:value[layer]})
            layer_info_data.update({key:layer_info_dict})
    return layer_info_data


# 构建一个图层信息字典对象
def build_layer_info_obj(layerinfo_json):
    layer_info_data = {}
    for key,value in layerinfo_json.items():
        if value["existSubdir"]:
            layer_info_dict = {}
            for dir_item in value["dir_list"]:
                sublayer_info = value[dir_item]
                sublayer_list = sublayer_info["layer_list"]
                for layer in sublayer_list:
                    layer_info_item = {
                        "img":cv2.imread(sublayer_info[layer]["path"], 0),
                        "weight":sublayer_info[layer]["weight"]
                    }
                    layer_info_dict.update({layer:layer_info_item})
            layer_info_data.update({key:layer_info_dict})
        else:
            layer_list = value["layer_list"]
            layer_info_dict = {}
            for layer in layer_list:
                layer_info_item = {
                        "img":cv2.imread(value[layer]["path"], 0),
                        "weight":value[layer]["weight"]
                    }
                layer_info_dict.update({layer:layer_info_item})
            layer_info_data.update({key:layer_info_dict})
    return layer_info_data

layer_info_list = []
for index in range(len(layer_config)):
    layerconfig_json = layer_config[index]
    layerinfo_json = layer_info[index]
    balance_layerweight(layerconfig_json, layerinfo_json)
    layer_info_list.append(build_layer_info_obj(layerinfo_json))

print(sys.getsizeof(layer_info_list))
# serialize_save(layer_info_list,str(Path.joinpath(PATH.DATA_PATH, "layer_info_list_obj")))
# save_json(PATH.DATA_PATH, "layer_info_list_obj", layer_info_list)

