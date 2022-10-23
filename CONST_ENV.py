import os
import json
from pathlib import Path


class ENV_PATH:

    def make_dir(file_path):
        if not Path(file_path).exists():
            Path.mkdir(file_path)
        return file_path

    BASE_PATH = Path(__file__).parent
    LAYER_PATH = Path.joinpath(BASE_PATH,"layers")
    CONFIG_PATH = Path.joinpath(BASE_PATH, "config/config.json")
    DATA_PATH = make_dir(Path.joinpath(BASE_PATH, "data"))
    BUILD_PATH = make_dir(Path.joinpath(BASE_PATH, "build"))
    IMAGES_PATH = make_dir(Path.joinpath(BUILD_PATH, "images"))
    JSON_PATH = make_dir(Path.joinpath(BUILD_PATH, "json"))
    LOG_PATH = Path.joinpath(BASE_PATH, "src/balance_weights.log")

class CONSTANT:
    REPETITION_NUM_LIMIT = 20000


class AUTHOR_INFO:
    AUTHOR = "ShuxunoO"
    BLENDER = "Kaleidoscope_art_engine_2D"

