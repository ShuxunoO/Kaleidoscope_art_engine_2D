import sys
sys.path.append("../..")
from CONST_ENV import ENV_PATH as PATH
sys.path.append("..")
from get_layers_info import get_layersinfo, get_dirlist_and_filelist
from file_operations import load_lsyers_config, save_json

CONFIG = load_lsyers_config(PATH.CONFIG_PATH)
# print(CONFIG["layerConfigurations"])
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
        layers = item["layersOrder"]
        layer_info_subdict = {}
        for layer in layers:
            layer_info_subdict.update(get_layersinfo(PATH.LAYER_PATH, layer))
        layers_info.append(layer_info_subdict)
    # print(layers_info)
    save_json(PATH.DATA_PATH, "layers_config_V11", layers_info)


setup_layers_config(layer_configurations)
