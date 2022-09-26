import os
import json

class ENV_PATH:
    BASE_PATH = os.path.dirname(__file__)

    LAYER_PATH = os.path.join(BASE_PATH,"layers")
    CONFIG_PATH = os.path.join(BASE_PATH, "config/config.json")

    def make_dir(file_path):
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        return file_path

    DATA_PATH = make_dir(os.path.join(BASE_PATH, "data"))




