import os
import json
import sys
sys.path.append("..")
from CONST_ENV import ENV_PATH as PATH
from file_operations import get_layersinfos, save_json

with open(PATH.CONFIG_PATH) as f:
    CONFIG = json.load(f)

layer_configurations = CONFIG["layerConfigurations"]


def setup_layers_config(layer_configurations):
    """
    It takes a list of dictionaries, and for each dictionary in the list, it takes the value of the key
    "layersOrder" and appends it to a list
    
    @param layer_configurations a list of dictionaries, each dictionary contains a list of dictionaries,
    each dictionary contains a name and a list of dictionaries, each dictionary contains a name and a
    list of dictionaries, each dictionary contains a name and a list of dictionaries, each dictionary
    contains a name and a list of
    """
    layers_info = []
    print(len(layer_configurations))
    for item in layer_configurations:
        layer_info = []
        layers = item["layersOrder"]
        for layer in layers:
            layer_info.append(get_layersinfos(PATH.LAYER_PATH, layer["name"]))
            layers_info.append(layer_info)
            print(layers_info)

    save_json(PATH.DATA_PATH, "layers_config_V3", layers_info)



setup_layers_config(layer_configurations)