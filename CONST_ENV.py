import os
import json
from pathlib import Path

# It creates a class called ENV_PATH that has a bunch of attributes that are paths to various
# directories. 
# 
# The class also has a method called make_dir that creates a directory if it doesn't exist. 
# 
# The make_dir method is used to create the DATA_PATH attribute. 
# 
# The DATA_PATH attribute is a path to a directory called data. 
# 
# The data directory is where we'll store our data. 
# 
# The make_dir method is used to create the DATA_PATH attribute because we want to make sure that the
# data directory exists before we try to save data to it. 
# 
# The make_dir method is used to create the DATA_PATH attribute because we want to make sure that the
# data directory exists before we try to save data to it. 
# 
# The make_dir method is used to create the DATA_PATH attribute because we want to make sure that the
# data directory exists before
class ENV_PATH:
    BASE_PATH = Path(__file__).parent
    LAYER_PATH = Path.joinpath(BASE_PATH,"layers")
    CONFIG_PATH = Path.joinpath(BASE_PATH, "config/config.json")

    def make_dir(file_path):
        if not Path(file_path).exists():
            Path.mkdir(file_path)
        return file_path

    DATA_PATH = make_dir(Path.joinpath(BASE_PATH, "data"))
