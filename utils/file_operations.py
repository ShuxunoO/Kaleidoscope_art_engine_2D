import json
import os
from pathlib import Path
import sys
sys.path.append("..")
from CONST_ENV import ENV_PATH as PATH
# load json file


def save_json(save_path, filename, data):
    """
    It takes a path, a filename, and some data, and saves the data to a file with the given filename in
    the given path
    
    :param save_path: The path to the folder where you want to save the file
    :param filename: The name of the file to save
    :param data: The data to be saved
    """
    file_path = Path.joinpath(save_path, filename + ".json")
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# get_layersinfos


def get_layersinfos(base_path, file_name):
    """
    It takes a file name and a base path, and returns a list of dictionaries, each of which contains the
    name of a layer, the number of features in that layer, and the number of features in the layer that
    are null.
    
    :param base_path: the path to the folder containing the file
    :param file_name: the name of the file you want to get the layers from
    """
    current_path = Path.joinpath(base_path, file_name)
    layer_list = os.listdir(current_path)
    layer_dict = {}
    for item in layer_list:
        sub_path = Path.joinpath(current_path, item)
        if os.path.isdir(sub_path):
            print("Dir")
            sublayer_list = os.listdir(sub_path)
            sublayer_dict = {}
            sublayer_dict[item] = [{tempt_sublayer: {
                "path": os.path.join(sub_path, tempt_sublayer),
                "weight": 10,
                "counter": 2,
                "conflictElements": "xxx"
            }} for tempt_sublayer in sublayer_list]
            layer_dict[file_name] = sublayer_dict
            return layer_dict
        else:
            print("File")
            layer_dict[file_name] = [{layer: {
                "path": os.path.join(current_path, layer),
                "weight": 10,
                "counter": 2,
                "conflictElements": "xxx"
            }} for layer in layer_list]
            return layer_dict




def get_layersinfo(base_path, file_name):
    """
    It takes a file name and a base path, and returns a list of dictionaries, each of which contains the
    name of a layer, the number of features in that layer, and the number of features in the layer that
    are null.
    
    :param base_path: the path to the folder containing the file
    :param file_name: the name of the file you want to get the layers from
    """
    current_path = Path.joinpath(base_path, file_name)
    layer_list = os.listdir(current_path)
    layer_dict = {}
    dir_list = [f.stem for f in current_path.iterdir() if f.is_dir()]
    print(dir_list)
    if len(dir_list):
        for item in dir_list:
            layer_dict.update(get_layerinfo(current_path, item))
        return file_name, layer_dict
    else:
        return get_layerinfo(base_path, file_name)



def get_layerinfo(base_path, layer_name):
    """
    Count the layer information under the current folder.
    At this time the current folder does not contain subfolders
    
    Each dictionary in the list has the layer_name as the key, and a dictionary as the value.

    :param base_path: the base path to the folder containing the layers
    :param layer_name: the name of the layer
    :return: A dictionary with the key being the file_name and the value  dictionarie of attributes.
    """
    current_path = Path(Path.joinpath(base_path, layer_name)).resolve()
    print(current_path)
    layer_list = os.listdir(current_path)
    layer_dict = []
    print(layer_list)
    for layer in layer_list:
        layer_dict.append({layer[:-4]: {    # remove the suffix
                "path": str(current_path.joinpath(layer)),
                "weight": 10,
                "counter": 2,
                "conflictElements": "xxx"
            }})
    return layer_name, layer_dict


# get_layersinfo_2(PATH.LAYER_PATH, "Stroke")



print(get_layerinfo(Path.joinpath(PATH.LAYER_PATH, "Eggshell"), "Blue"))