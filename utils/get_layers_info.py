from CONST_ENV import ENV_PATH as PATH
import json
import os
from pathlib import Path
import sys
sys.path.append("..")
# load json file


def get_layersinfo(base_path, file_name):
    """
    It takes a file name and a base path, and returns a dictionary, which contains the
    file name as it's key and the layerinfo dictionary of it's value.

    :param base_path: the path to the folder containing the file
    :param file_name: the name of the file you want to get the layerinfo from
    """
    current_path = Path.joinpath(base_path, file_name)
    layer_list = os.listdir(current_path)  # find all files in the current_path
    layerinfo_dict = {}
    # pick out subfolders in current_path
    dir_list = [f.stem for f in current_path.iterdir() if f.is_dir()]
    # get the remaining files in current_path
    file_list = list(set(layer_list) - set(dir_list))
    # print(dir_list)
    # print(file_list)
    if len(dir_list):
        for item in dir_list:
            layerinfo_dict.update(get_layerinfo_in_subdir(current_path, item))
    for item in file_list:
        layerinfo_dict.update(get_layerinfo_foreach(base_path, item))
    return {file_name: layerinfo_dict}


def get_layerinfo_in_subdir(base_path, dir_name):
    """
    It takes a base path and a directory name, and returns a dictionary, which contains the
    dirctory name as it's key and the layerinfo dictionary of it's value.

    :param base_path: the path of the directory where the subdirectories are located
    :param dir_name: the name of the subdirectory
    """

    current_path = Path(Path.joinpath(base_path, dir_name)).resolve()
    # print(current_path)
    layer_list = os.listdir(current_path)
    # print(layer_list)
    layer_info_list = []
    for layer in layer_list:
        layer_name = layer[:-4]  # remove the suffix
        name, weight = get_purename_and_weight(layer_name)
        layer_info_list.append({name: {
            "path": str(current_path.joinpath(layer)),
            "weight": weight
        }})
    return {dir_name: layer_info_list}


def get_layerinfo_foreach(base_path, file_name):
    """
    This function takes a base path and a file name, and returns a dictionary with the layer name as
    the key and a dictionary of layer information as the value

    :param base_path: The path to the folder where the layer is stored
    :param file_name: The name of the layer
    :return: A dictionary with the layer name as the key and the layer infos as the value.
    """
    layer_name = file_name[:-4]  # remove the suffix
    name, weight = get_purename_and_weight(layer_name)
    layer_info = {
        "path": str(Path(base_path.joinpath(file_name)).resolve()),
        "weight": weight
    }
    return {name: layer_info}


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
        weight = -1
    else:
        weight = int(name_weight_list[1])
    return purename, weight


def equilibrium_layerweight():
    """
    Under normal circumstances,
    the sum of the weights of the layers in a layer folder should be equal to the total number of NFTs we set,
    but when the total number is more than or less than the total number of NFTs,
    we need to redistribute the weights according to the proportion of the layers.
    Of course, this The function is up to the user to decide whether to use it or not.
    """
    return
