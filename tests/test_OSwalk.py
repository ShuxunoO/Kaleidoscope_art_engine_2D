import os
import sys
sys.path.append('..')
from utils.file_operations import save_json
from CONST_ENV import ENV_PATH as PATH

a = []
for root, dirs, files in os.walk(os.path. PATH.LAYER_PATH):
    print (root,dirs,files)
    a.append({
        "root": root,
        "content":
        {
            "dirs": dirs,
            "files": files,
        }
    })


save_json(PATH.DATA_PATH, "osWalk", a)
