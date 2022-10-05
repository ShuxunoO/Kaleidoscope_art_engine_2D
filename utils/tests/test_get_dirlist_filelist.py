import sys
sys.path.append('../..')
from CONST_ENV import ENV_PATH as PATH
from pathlib import Path
sys.path.append('..')
from get_layers_info import get_dirlist_and_filelist

filepath = Path.joinpath(PATH.LAYER_PATH,"Music_Effect")
a, b = get_dirlist_and_filelist(filepath)
print(a)
print(b)