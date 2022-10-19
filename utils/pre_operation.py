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


for index in range(len(layer_config)):
    layerconfig_json = layer_config[index]
    layerinfo_json = layer_info[index]
    balance_layerweight(layerconfig_json, layerinfo_json)
