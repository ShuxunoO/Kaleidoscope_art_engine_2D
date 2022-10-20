import sys
from pathlib import Path
from set_layers_weight import balance_layerweight
from file_operations import load_lsyers_config, save_json
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

layer_info_list = []
for index in range(len(layer_config)):
    layerconfig_json = layer_config[index]
    layerinfo_json = layer_info[index]
    balance_layerweight(layerconfig_json, layerinfo_json)
    layer_info_list.append(build_layer_info(layerinfo_json))

save_json(PATH.DATA_PATH, "layer_info_list", layer_info_list)

