import random
import sys
from pathlib import Path
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
    dna_set = {}
    # metadata 冲撞的次数
    repetition_num = 0
    for index in range(len(layer_configs)):
        layer_config = layer_configs[index]
        layer_info = layers_info_json[index]
        build_imgs_attributes(layer_config, layer_info,
                              dna_set, repetition_num)

def build_imgs_attributes(layer_config, layer_info, dna_set, repetition_num):

    # totalNumber = layer_config["totalNumber"]
    totalNumber = 10
    token_ID = layer_config["startID"]
    counter = 0
    REPETITION_NUM_LIMIT = 20000
    layers = layer_config["layersOrder"]
    # 构建一个属性列表
    while counter < totalNumber and repetition_num < REPETITION_NUM_LIMIT:
        temp_attributes = build_metainfo_for_each_img(layers, layer_info)
        print(temp_attributes)
        counter += 1
        # 去掉冗余信息
        temp_pure_attributes = get_pure_metainfo(temp_attributes)
        print(temp_pure_attributes)



    get_pure_metainfo(temp_attributes)
    # 判断是否重复

    # 不重复的话更新数值


def build_metainfo_for_each_img(layers, layer_info):
    attributes = {}
    for layer in layers:
        attributes.update(
            {layer["name"]:  build_metainfo_for_each_layer(layer, layer_info, attributes)})
    return attributes

def build_metainfo_for_each_layer(layer, layer_info, attributes):
    layer_name = layer["name"]
    current_layer_info = layer_info[layer_name]
    # 不受任何约束的图层，完全随机
    if current_layer_info["existSubdir"] == False:
        return set_metainfo_for_free_layer(current_layer_info)
    # 纯信标层
    elif current_layer_info["isBeaconLayer"] == True and "groupBy" not in current_layer_info:
        return set_metainfo_for_beacon_layer(current_layer_info)
    # 纯从属子层
    elif current_layer_info["isBeaconLayer"] == False and "groupBy" in current_layer_info:
        return set_metainfo_for_subordinate_layer(current_layer_info, attributes)
    # 既是信标层又是从属子层
    else:
        return set_beacon_subordinate_layer(current_layer_info, attributes)

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
        print("Layer List in Folder {} Is Empty, System exit.".format(
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
            print("Layer List In Folder {} of {} Is Empty, System exit.".format(beacon, layer_info["name"]))
            sys.exit(0)
    except:
        print("Folder List in {} Is Empty, System exit.".format(layer_info["name"]))
        sys.exit(0)

# 返回从属层的图层信息
def set_metainfo_for_subordinate_layer(layer_info, attributes):
    beacon = None
    groupBy = layer_info["groupBy"]
    indicator = attributes[groupBy]["beacon"]
    try:
        value = random.choice(layer_info[indicator]["layer_list"])
        return {"trait_type": layer_info["name"],
                "groupBy": groupBy,
                "beacon": beacon,
                "value": value}
    except:
        print("Layer List In Folder {} of {} Is Empty, System exit.".format(indicator, layer_info["name"]))
        sys.exit(0)

def set_beacon_subordinate_layer(layer_info, attributes):
    # 判断信标层的信标在不在自己的从属子层文件夹中，如果在按照常规常规从属层处理
    groupBy = layer_info["groupBy"]
    indicator = attributes[groupBy]["beacon"]
    if indicator in layer_info["subordinate_dir_list"]:
        return set_metainfo_for_subordinate_layer(layer_info, attributes)
    else:
        return set_metainfo_for_beacon_layer(layer_info)

def get_pure_metainfo(img_attributes):
    for value in img_attributes.values():
        del value["groupBy"]
        del value["beacon"]
    return list(img_attributes.values())

def update_layer_info(attribute_dict):
    # 更新
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

#


def blend(img_obj_list):

    # Treat the first layer as the background
    bg = Image.open(os.path.join('assets', filepaths[0]))

    # Loop through layers 1 to n and stack them on top of another
    for filepath in filepaths[1:]:
        img = Image.open(os.path.join('assets', filepath))
        bg.paste(img, (0, 0), img)

    # Save the final image into desired location
    if output_filename is not None:
        bg.save(output_filename)
    else:
        # If output filename is not specified, use timestamp to name the image and save it in output/single_images
        if not os.path.exists(os.path.join('output', 'single_images')):
            os.makedirs(os.path.join('output', 'single_images'))
        bg.save(os.path.join('output', 'single_images',
                str(int(time.time())) + '.png'))



setup_images(layer_configs, layers_info_json)