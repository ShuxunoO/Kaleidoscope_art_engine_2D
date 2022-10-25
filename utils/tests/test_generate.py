import random
import sys
from pathlib import Path
from PIL import Image
sys.path.append("../..")
from CONST_ENV import ENV_PATH as PATH
sys.path.append('..')
from pre_operation import preprocess_layer_info
from generate import setup_images

CONFIG = fop.load_lsyers_config(PATH.CONFIG_PATH)
layer_configs = CONFIG["layerConfigurations"]
