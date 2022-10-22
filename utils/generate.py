import sys
from pathlib import Path
from pre_operation import preprocess_layer_info
import file_operations as fop
sys.path.append('..')
from CONST_ENV import ENV_PATH as PATH



CONFIG = fop.load_lsyers_config(PATH.CONFIG_PATH)
layer_config = CONFIG["layerConfigurations"]
preprocess_layer_info(layer_config)

