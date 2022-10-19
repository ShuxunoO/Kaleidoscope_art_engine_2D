import os
import sys
from pathlib import Path
sys.path.append('..')
from CONST_ENV import ENV_PATH as PATH
from utils.file_operations import save_json




print(PATH.DATA_PATH)


a = []
for root, dirs, files in os.walk(PATH.LAYER_PATH):
    print (root,dirs,files)
    a.append({
        "root":  str(Path(root).resolve()),
        "content":
        {
            "dirs": dirs,
            "files": files,
        }
    })


# save_json(PATH.DATA_PATH, "osWalk2", a)
