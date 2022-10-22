import sys
from pathlib import Path
import cv2
import file_operations as fop
from get_layers_info import get_layers_info
from set_layers_weight import balance_layer_weight
sys.path.append('..')
from CONST_ENV import ENV_PATH as PATH

"""
    1. 按照配置文件读取图层信息并返回
    2. 按照特定规则将图层的权重进行均衡
    3. 拿到均衡后的文件创建一个包含所有图层信息的字典
"""

def preprocess_layer_info(layer_configs):
    layers_info_json = read_layers_info(layer_configs)
    fop.save_json(PATH.DATA_PATH, "layers_info", layers_info_json)
    balance(layer_configs, layers_info_json)
    fop.save_json(PATH.DATA_PATH, "layers_info_after_balancing", layers_info_json)
    layer_info_list = build_layer_info_list(layers_info_json)
    fop.save_json(PATH.DATA_PATH, "layer_info_list", layer_info_list)


def read_layers_info(layer_configs):
    """
    It takes a list of dictionaries, and for each dictionary in the list, it takes the value of the key
    "layersOrder" and appends it to a list
    
    @param layer_configs a list of dictionaries, each dictionary contains a list of dictionaries,
    each dictionary contains a name and a list of dictionaries, each dictionary contains a name and a
    list of dictionaries, each dictionary contains a name and a list of dictionaries, each dictionary
    contains a name and a list of
    """
    layers_info = []
    for layer_config_item in layer_configs:
        layers = layer_config_item["layersOrder"]
        layer_info_subdict = {}
        for layer in layers:
            layer_info_subdict.update(get_layers_info(PATH.LAYER_PATH, layer))
        layers_info.append(layer_info_subdict)
    return layers_info


def balance(layer_configs, layers_info_json):
    layer_info_list = []
    for index in range(len(layer_configs)):
        layer_config = layer_configs[index]
        layer_info = layers_info_json[index]
        balance_layer_weight(layer_config, layer_info)


def build_layer_info_list(layers_info_json):
    layer_info_list = []
    for index in range(len(layers_info_json)):
        layer_info = layers_info_json[index]
        layer_info_list.append(build_layer_info_dict(layer_info))
    return layer_info_list


# 构建一个图层信息字典
def build_layer_info_dict(layer_info):
    layer_info_data = {}
    for key,value in layer_info.items():
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
def build_layer_info_binary_obj(layer_info):
    layer_info_data = {}
    for key,value in layer_info.items():
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
