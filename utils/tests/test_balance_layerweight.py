import sys
from pathlib import Path
sys.path.append("../..")
from CONST_ENV import ENV_PATH as PATH
sys.path.append('..')
from get_layers_info import balance_layerweight
from file_operations import load_lsyers_config


CONFIG = load_lsyers_config(PATH.CONFIG_PATH)
layer_config = CONFIG["layerConfigurations"]
layer_info_path = Path.joinpath(PATH.DATA_PATH, "layers_config_V6.json")
layer_info = load_lsyers_config(layer_info_path)




for index in range(len(layer_config)):

    layerconfig_json = layer_config[index]
    layerinfo_json = layer_info[index]
    balance_layerweight(layerconfig_json, layerinfo_json)






