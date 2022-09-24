import os
import json
import CONST_ENV as CE
from file_operations import get_layersinfos, save_json

with open(CE.CONFIG_PATH) as f:
    CONFIG = json.load(f)

layer_configurations = CONFIG["layerConfigurations"]
def setup_layers_config(layer_configurations):
    layers_info = []
    for item in layer_configurations:
        layer_info = []
        layers = item["layersOrder"]
        for layer in layers:
            layer_info.append(get_layersinfos(CE.LAYER_PATH, layer["name"]))
            layers_info.append(layer_info)
            print(layers_info)

    save_json(CE.DATA_PATH, "layers_config_V2", layers_info)




setup_layers_config(layer_configurations)


