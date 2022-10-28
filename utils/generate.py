import random
import sys
import hashlib
import copy
from PIL import Image
from pathlib import Path
import file_operations as fop
sys.path.append('..')
from CONST_ENV import ENV_PATH as PATH
from PIL import Image

import file_operations as fop
from pre_operation import preprocess_layer_info


CONFIG = fop.load_lsyers_config(PATH.CONFIG_PATH)
layer_configs = CONFIG["layerConfigurations"]


layers_info_json = preprocess_layer_info(layer_configs)

def setup_images(layer_configs, layers_info_json):
    # 存放DNA 哈希值的集合
    dna_set = set({})
    # metadata 冲撞的次数
    repetition_num = 0
    for index in range(len(layer_configs)):
        layer_config = layer_configs[index]
        layer_info = layers_info_json[index]
        build_imgs_attributes(layer_config, layer_info,
                                dna_set, repetition_num)

def build_imgs_attributes(layer_config, layer_info, dna_set, repetition_num):
    totalNumber = layer_config["totalNumber"]
    # totalNumber = 8000
    token_ID = layer_config["startID"]
    counter = 0
    REPETITION_NUM_LIMIT = 20000
    layers = layer_config["layersOrder"]
    # 构建一个属性列表
    while counter < totalNumber and repetition_num < REPETITION_NUM_LIMIT:
        attribute_dict = build_metainfo_for_each_img(layers, layer_info)
        # print("attribute_dict:", attribute_dict)
        # 去掉冗余信息
        attribute_list = get_pure_metainfo(copy.deepcopy(attribute_dict))
        # print(attribute_list)
        # # 判断是否重复
        dna = hashlib.sha1(str(attribute_list).encode('utf-8')).hexdigest()
        if dna in dna_set:
            repetition_num += 1
            print("\n\n…………………………………………………………………………………………重复………………………………………………………………………………………………………………………………\n\n")
            continue
        else:
            # 不重复的话更新数值（返回一个图层对象的列表）
            layer_obj_list = update_layer_info(layer_info, attribute_dict)
            # 混合图像
            blend(layer_obj_list, token_ID)
            token_ID += 1

            # 组装metada

            # 把dna 添加到 dna_set
            print(dna)
            dna_set.add(dna)
            counter += 1
    print(len(dna_set))
    fop.save_file(PATH.DATA_PATH, "dna_set", str(dna_set))
    fop.save_json(PATH.DATA_PATH, "layers_info_after_generating", layer_info)


def build_metainfo_for_each_img(layers, layer_info):
    attributes = {}

    # 为了维持图层原有的顺序，先把各个图层的名字按照熟顺序添加到属性字典中
    for layer in layers:
        layer_name = layer["name"]
        current_layer_info = layer_info[layer_name]
        attributes.update({layer_name : None})

    # 先添加信标层的属性
    for layer in layers:
        layer_name = layer["name"]
        current_layer_info = layer_info[layer_name]
        if current_layer_info["isBeaconLayer"] == True:
            attributes.update(
                {layer_name : build_metainfo_for_each_layer(layer, current_layer_info, attributes)})
    # 最后添加从属子层的属性
    for layer in layers:
        layer_name = layer["name"]
        if attributes[layer_name] == None:
            current_layer_info = layer_info[layer_name]
            attributes.update(
                {layer_name : build_metainfo_for_each_layer(layer, current_layer_info, attributes)})
    return attributes

def build_metainfo_for_each_layer(layer, layer_info, attributes):
    # 不受任何约束的图层，完全随机
    if layer_info["existSubdir"] == False:
        return set_metainfo_for_free_layer(layer_info)
    # 纯信标层
    elif layer_info["isBeaconLayer"] == True and "groupBy" not in layer_info:
        return set_metainfo_for_beacon_layer(layer_info)
    # 纯从属子层
    elif layer_info["isBeaconLayer"] == False and "groupBy" in layer_info:
        return set_metainfo_for_subordinate_layer(layer_info, attributes)
    # 既是信标层又是从属子层
    else:
        return set_beacon_subordinate_layer(layer_info, attributes)

# 返回自由层的图层信息
def set_metainfo_for_free_layer(layer_info):
    beacon = None
    groupBy = None
    try:
        value = random.choice(layer_info["layer_list"])
        return {"trait_type": layer_info["name"],
                "groupBy": groupBy,
                "beacon": beacon,
                "value": value}
    except:
        print("The free layer list in folder {} Is empty, System exit.".format(
            layer_info["name"]))
        sys.exit(0)

# 返回信标层的图层信息
def set_metainfo_for_beacon_layer(layer_info):
    try:
        beacon = random.choice(layer_info["beacon_dir_list"])  # 信标是本图层指导其附属子层合成的指示器
        groupBy = None
        try:
            value = random.choice(layer_info[beacon]["layer_list"])
            return {"trait_type": layer_info["name"],
                    "groupBy": groupBy,
                    "beacon": beacon,
                    "value": value}
        except:
            print("The beacon layer list in folder {} of {} Is empty, System exit.".format(beacon, layer_info["name"]))
            sys.exit(0)
    except:
        print("The beacon folder list in {} is Empty, System exit.".format(layer_info["name"]))
        sys.exit(0)

# 返回从属层的图层信息
def set_metainfo_for_subordinate_layer(layer_info, attributes):
    groupBy = layer_info["groupBy"]
    beacon = attributes[groupBy]["beacon"]
    try:
        value = random.choice(layer_info[beacon]["layer_list"])
        return {"trait_type": layer_info["name"],
                "groupBy": groupBy,
                "beacon": beacon,
                "value": value}
    except:
        print("The subordinate layer list In folder {} of {} is empty, System exit.".format(beacon, layer_info["name"]))
        sys.exit(0)

# 返回既是信标层又是从属子层的图层信息
def set_beacon_subordinate_layer(layer_info, attributes):
    # 判断信标层的信标在不在自己的从属子层文件夹中，如果在按照常规常规从属层处理
    groupBy = layer_info["groupBy"]
    beacon = attributes[groupBy]["beacon"]
    if beacon in layer_info["subordinate_dir_list"]:
        return set_metainfo_for_subordinate_layer(layer_info, attributes)
    else:
        return set_metainfo_for_beacon_layer(layer_info)

def get_pure_metainfo(img_attributes):
    for value in img_attributes.values():
        del value["groupBy"]
        del value["beacon"]
    return list(img_attributes.values())


def update_layer_info(layer_info, attribute_dict):
    layer_obj_list = []
    for key, value in attribute_dict.items():
        current_layer_info = layer_info[key]
        # 更新纯信标层
        if value["groupBy"] == None and value["beacon"] != None:
            beacon = value["beacon"]
            layer_name = value["value"]
            layer = current_layer_info[beacon][layer_name]
            layer["weight"] -= 1
            layer_obj_list.append(layer["path"])
            if layer["weight"] <= 0:
                # 权值为0的元素要从图层列表中删掉
                current_layer_info[beacon]["layer_list"].remove(layer_name)
                if len(current_layer_info[beacon]["layer_list"]) == 0:
                    current_layer_info["beacon_dir_list"].remove(beacon)

        # 更新自由图层
        elif value["groupBy"] == None and value["beacon"] == None:
            layer_name = value["value"]
            layer = current_layer_info[layer_name]
            layer["weight"] -= 1
            layer_obj_list.append(layer["path"])
            if layer["weight"] <= 0:
                # 权值为0的元素要从图层列表中删掉
                current_layer_info["layer_list"].remove(layer_name)

        # 更新信标层或者从属子层信息
        elif value["groupBy"] != None and value["beacon"] != None:
            beacon = value["beacon"]
            layer_name = value["value"]
            layer = current_layer_info[beacon][layer_name]
            layer["weight"] -= 1
            layer_obj_list.append(layer["path"])
            if layer["weight"] <= 0:
                # 权值为0的元素要从图层列表中删掉
                current_layer_info[beacon]["layer_list"].remove(layer_name)
                if len(current_layer_info[beacon]["layer_list"]) == 0:
                    current_layer_info["subordinate_dir_list"].remove(beacon)
        # ambiguous layer
        else:
            groupBy == value["groupBy"]
            beacon = value["beacon"]
            layer_name = value["value"]
            layer = current_layer_info[beacon][layer_name]
            layer["weight"] -= 1
            layer_obj_list.append(layer["path"])
            if layer["weight"] <= 0:
                # 权值为0的元素要从图层列表中删掉
                current_layer_info[beacon]["layer_list"].remove(layer_name)
                if len(current_layer_info[beacon]["layer_list"]) == 0:
                    if value["groupBy"] == None:
                        current_layer_info["beacon_dir_list"].remove(beacon)
                    else:
                        current_layer_info["subordinate_dir_list"].remove(beacon)
    return layer_obj_list



    return attribute_list, img_obj_list
# 创建源数据
def generate_metadata(layer_configs, attribute_list):
    pass

# 准备图像的各个元素
def prepare_image_elements(img_attributes_list, layers_info_list):
    layer_obj_list = []
    for layer in img_attributes_list:
        trait_type = layer["trait_type"]
        value = layer["value"]
        img_path = layers_info_list[trait_type][value]["path"]
        try:
            layer_obj = Image.open(img_path)
            layer_obj_list.append(layer_obj)
        except:
            print("Img not exit")
    return layer_obj_list

# 正式混合

def blend(layer_obj_list, token_ID):
    print(layer_obj_list)
    background = Image.open(layer_obj_list[0]).convert("RGBA")
    for layer in layer_obj_list[1:]:
        img = Image.open(layer).convert("RGBA")
        background.paste(img, (0, 0), img)
    # background.show()
    path = PATH.IMAGES_PATH.joinpath(str(token_ID) + '.png')
    background.save(path)


setup_images(layer_configs, layers_info_json)