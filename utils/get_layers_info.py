import os
import sys
import re
sys.path.append("..")
from pathlib import Path
from CONST_ENV import ENV_PATH as PATH
from file_operations import load_lsyers_config, save_json



def get_dirlist_and_filelist(file_path):

    """
    It takes a file path and returns a files list and a subfolders list in the path
    
    :param file_path: the path to the folder containing the files you want to rename
    :return: A tuple of two lists.
    """

    file_list = os.listdir(file_path)  # find all files in the file_path
    # pick out subfolders in file_path
    dir_list = [f.stem for f in file_path.iterdir() if f.is_dir()]
    # get the remaining files in file_path
    layer_list = list(set(file_list) - set(dir_list))

    return layer_list, dir_list


def get_layersinfo(base_path, layer_name):
    """
    It takes a file name and a base path, and returns a dictionary, which contains the
    file name as it's key and the layerinfo dictionary of it's value.

    :param base_path: the path to the folder containing the file
    :param layer_name: the name of the file you want to get the layerinfo from
    """
    current_path = Path.joinpath(base_path, layer_name)
    layer_list, dir_list = get_dirlist_and_filelist(current_path)
    print(layer_list, dir_list)
    layerinfo_dict = {}  # a dictionary to store the layers infomation in base path
    layerinfo_dict.update({
        "existSubdir": len(dir_list) > 0,
        "layer_list": [re.split("[#.]", layer)[0] for layer in layer_list],  # remove the suffix and weight to get purename
        "dir_list": dir_list})
    if len(layer_list):
        get_layerinfo_in_currentdir(current_path, layer_list, layerinfo_dict)
    if len(dir_list):
        get_layerinfo_in_subdir(current_path, dir_list, layerinfo_dict)
    return {layer_name: layerinfo_dict}


def get_layerinfo_in_subdir(base_path, dir_list, layerinfo_dict):

    """
    It takes a base path and a directory name, and returns a dictionary, which contains the
    dirctory name as it's key and the layerinfo dictionary of it's value.
    When "existSubdir" is True, it means there existing subdirectory in current base path.

    :param base_path: the path of the directory where the subdirectories are located
    :param dir_name: the name of the subdirectory
    """
    layer_list, dir_list = get_dirlist_and_filelist(base_path)
    for dir_item in dir_list:
        sub_path = Path(base_path.joinpath (dir_item)).resolve()
        sublayer_list = os.listdir(sub_path)
        sublayer_info_list = []
        for layer in sublayer_list:
            layer_name = layer[:-4]  # remove the suffix
            name, weight = get_purename_and_weight(layer_name)
            sublayer_info_list.append({name: {
                "path": str(sub_path.joinpath(layer)),
                "weight": weight
            }})
        layerinfo_dict.update({dir_item : sublayer_info_list})



def get_layerinfo_in_currentdir(file_path, layer_name, layerinfo_dict):
    """
    This function takes a base path and a file name, and returns a dictionary with the layer name as
    the key and a dictionary of layer information as the value
    When "existSubdir" is False, it means there is no subdirectory in current base path.

    :param base_path: The path to the folder where the layer is stored
    :param file_name: The name of the layer
    :return: A dictionary with the layer name as the key and the layer infos as the value.
    """
    layer_list, dir_list = get_dirlist_and_filelist(file_path)
    for layer in layer_list:
        item_name = layer[:-4]  # remove the suffix
        name, weight = get_purename_and_weight(item_name)
        layer_info = {
            "path": str(Path(file_path.joinpath(layer)).resolve()),
            "weight": weight
        }
        layerinfo_dict.update({name: layer_info})


def get_purename_and_weight(layer_name):

    """
    It takes a string of the form "layer_name#weight" and returns a tuple of the form (layer_name,
    weight).

    :param layer_name: the name of the layer, such as 'conv1_1#1'
    :return: A tuple of the purename and weight.
    """

    name_weight_list = layer_name.split('#')
    purename = name_weight_list[0]
    if len(name_weight_list) == 1:
        weight = -1  # user doesn't assign a weight of this layer
    else:
        weight = int(name_weight_list[1])
    return purename, weight


def balance_layerweight(layerconfig_json, layerinfo_json):
    """
    Under normal circumstances,
    the sum of the weights of the layers in a layer folder should be equal to the total number of NFTs we set,
    but when the total number is more than or less than the total number of NFTs,
    we need to redistribute the weights according to the proportion of the layers.
    Of course, this The function is up to the user to decide whether to use it or not.

    The policy for adjusting the weights is quite sample: 
    When the sum of the weights is more or less than the total number of NFTs, 
    each layer's weight will be adjust to (total number * (weight / sum of the weights)).
    When we do not specify weights for some layers, 
    the weights of these layers will be divided equally from the total number of NFTs minus the assigned weights

    """

    # print(layerconfig_json ,"\n\n")
    # print(layerinfo_json , "\n\n")
    sum = layerconfig_json["totalNumber"]
    layers = layerconfig_json["layersOrder"]

    for layer in layers:
        layer_name = layer["name"]
        dir_list = layerinfo_json[layer_name]["dir_list"]
        layer_list = layerinfo_json[layer_name]["layer_list"]
        counter = 0  # Sum of cumulative weights
        num_of_noweight_layers = 0  # Record the number of layers with no assigned weights


    # layer_configs = load_lsyers_config(layer_config_path)
    # for config_item in layer_configs:
    #     print(type(config_item).__name__ == "dict")
    #     for key, value in config_item.items():
    #         print("key: ", key)
    #         print("value: ", value)
