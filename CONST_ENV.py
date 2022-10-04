import os
import json
from pathlib import Path


class ENV_PATH:
    BASE_PATH = Path(__file__).parent
    LAYER_PATH = Path.joinpath(BASE_PATH,"layers")
    CONFIG_PATH = Path.joinpath(BASE_PATH, "config/config.json")

    def make_dir(file_path):
        if not Path(file_path).exists():
            Path.mkdir(file_path)
        return file_path

    DATA_PATH = make_dir(Path.joinpath(BASE_PATH, "data"))
