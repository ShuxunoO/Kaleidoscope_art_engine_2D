import sys
from pathlib import Path
sys.path.append("../..")
from CONST_ENV import ENV_PATH as PATH
sys.path.append('..')
from set_layers_weight import balance_layerweight
import file_operations as fop



CONFIG = fop.load_json(PATH.CONFIG_PATH)
layer_config = CONFIG["layerConfigurations"]
layer_info_path = Path.joinpath(PATH.DATA_PATH, "layers_config_V11.json")
layer_info = fop.load_json(layer_info_path)


for index in range(len(layer_config)):
    layerconfig_json = layer_config[index]
    layerinfo_json = layer_info[index]
    balance_layerweight(layerconfig_json, layerinfo_json)


fop.save_json(PATH.DATA_PATH, "layers_config_V11_after_balance", layer_info)