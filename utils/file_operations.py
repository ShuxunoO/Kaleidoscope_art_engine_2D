import json
import os
from pathlib import Path
import sys
sys.path.append("..")
from CONST_ENV import ENV_PATH as PATH



def save_json(save_path, filename, data):
    """
    Saves the data to a file with the given filename in the given path
    
    :param save_path: The path to the folder where you want to save the file
    :param filename: The name of the file to save
    :param data: The data to be saved
    """
    file_path = Path.joinpath(save_path, filename + ".json")
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# load json file
def load_lsyers_config(config_path):
    """
    It loads a JSON file and returns the contents as a Python dictionary
    
    :param config_path: The path to the config file
    :return: A dictionary
    """
    with open(config_path) as f:
        return json.load(f)

# print(get_layersinfo(PATH.LAYER_PATH, "Eggshell"))
# save_json(PATH.DATA_PATH, "temp", get_layersinfo(PATH.LAYER_PATH, "Background"))

# print(get_layerinfo(Path.joinpath(PATH.LAYER_PATH, "Eggshell"), "Blue"))