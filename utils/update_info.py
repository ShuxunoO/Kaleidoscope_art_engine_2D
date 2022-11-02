import os
import random
import sys
import re
from pathlib import Path

from tqdm import tqdm

import utils.file_operations as fop

sys.path.append('..')
from CONST_ENV import ENV_PATH as PATH


# 更新json信息
def update_metadata(CONFIG):
    json_path = PATH.JSON_PATH
    file_list =  os.listdir(json_path)
    for file_item in tqdm(file_list, desc='Updating Metadata ',unit= "piece", postfix={'value': len(file_list)}):
        # 加载文件
        json_file = fop.load_json(json_path.joinpath(file_item))
        # 修改信息
        token_ID = str(json_file["tokenID"])
        json_file["name"] = CONFIG["namePrefix"] + " #" + token_ID
        json_file["description"] = CONFIG["description"]
        json_file["image"] = CONFIG["baseUri"] + "/" + token_ID + ".png"
        # 存储文件
        fop.save_json(json_path, token_ID, json_file)
    print("Done")

def count_layer_distribution():
    pass

# 打乱某一区间内的图像和json
def shuffle(start, end):
    json_path = PATH.JSON_PATH
    img_path = PATH.IMAGES_PATH
    file_list = list(range(start, end+1))
    length = len(file_list)
    file_list_shuffled = list(range(start, end+1))
    random.shuffle(file_list_shuffled)
    print(file_list)
    print(file_list_shuffled)
    for index in tqdm(range(length), desc='Shuffling',unit= "piece", postfix={'value': length}):
        original_ID = file_list[index]
        new_ID = file_list_shuffled[index]

        original_json_name = str(original_ID) + ".json"

        original_img_name = str(original_ID) + ".png"
        new_img_name = str(new_ID) + ".png"

        print(original_json_name, original_img_name)
        
        # 取出json文件
        json_file = fop.load_json(json_path.joinpath(original_json_name))
        # 修改json数据
        json_file["name"] = re.sub(r"""\#[0-9]*""", "#" + str(new_ID), json_file["name"])
        json_file["image"] = re.sub(r"""/[0-9]*.png""", "/" + str(new_ID) + ".png", json_file["image"])
        json_file["tokenID"] = new_ID
        # 存储
        fop.save_json(json_path, str(new_ID), json_file)
        # 修改对应图像的名字
        os.rename(img_path.joinpath(original_img_name),img_path.joinpath(new_img_name))


        # # 更改json 和对应图片的名字

