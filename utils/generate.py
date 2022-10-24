import sys
from pathlib import Path
from random import randint
from PIL import Image
from pre_operation import preprocess_layer_info
import file_operations as fop
sys.path.append('..')
from CONST_ENV import ENV_PATH as PATH
CONFIG = fop.load_lsyers_config(PATH.CONFIG_PATH)
layer_configs = CONFIG["layerConfigurations"]


layers_info_json, layers_info_list = preprocess_layer_info(layer_configs)


def setup_images(layer_configs, layers_info_json):
    # 存放DNA 哈希值的集合
    dna_set = {}
    # metadata 冲撞的次数
    repetition_num = 0
    for index in range(len(layer_configs)):
        layer_config = layer_configs[index]
        layer_info = layers_info_json[index]
        build_imgs_attributes(layer_config, layer_info, dna_set, repetition_num)


def build_imgs_attributes(layer_config, layer_info, dna_set, repetition_num):
    attributes = {}
    totalNumber = layer_config["totalNumber"]
    token_ID = layer_config["startID"]
    counter = 0
    REPETITION_NUM_LIMIT = 20000
    layers = layer_config_item["layersOrder"]
    # 构建一个属性列表
    while counter < totalNumber and repetition_num < REPETITION_NUM_LIMIT:
        for layer in layers:
            if layer["isBeaconLayer"] == False:  # 不受任何约束的图层，完全随机
                beacon = None
                groupBy = None
                trait_type = layer["name"]
                index, value = choose_layer_from_layer_list(layer_info[name]["layer_list"])
                
    # 判断是否重复

    # 不重复的话更新数值

def build_metainfo_of_one_layer():
    pass

# 从图层列表选一个图层出来
def choose_layer_from_layer_list(layer_list):
    end = len(layer_list) - 1
    random_num = randint(0, end)
    return random_num, layer_list[random_num]

def update_layer_info():
    pass

# 创建源数据
def generate_metadata():
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
def blend(filepaths, output_filename=None):

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