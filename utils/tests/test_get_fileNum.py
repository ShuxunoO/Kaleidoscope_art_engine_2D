import sys
sys.path.append('../..')
from CONST_ENV import ENV_PATH as PATH
from pathlib import Path
sys.path.append('..')
from get_layers_info import get_fileNum

print(get_fileNum(Path.joinpath(PATH.LAYER_PATH, "Pattern")))