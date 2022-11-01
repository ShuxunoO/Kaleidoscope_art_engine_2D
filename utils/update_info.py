import os
from pathlib import Path
import utils.file_operations as fop
from tqdm import tqdm
# 更新json信息
def update_metadata(json_path, CONFIG):
    file_list =  os.listdir(json_path)
    for file_item in tqdm(file_list, desc='Updating Metadata ',unit= "个", postfix={'value': len(file_list)}):
        # 加载文件
        json_file = fop.load_json(json_path.joinpath(file_item))
        # 修改信息
        json_file["description"] = CONFIG["description"]
        token_ID = str(json_file["tokenID"])
        json_file["image"] = CONFIG["baseUri"] + "/" + token_ID + ".png"
        # 存储文件
        fop.save_json(json_path, token_ID, json_file)
    print("Done")

def count_layer_distribution():
    pass

def shuffle():
    pass