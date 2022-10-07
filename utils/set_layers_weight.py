
def balance_layerweight(layerconfig_json, layerinfo_json):

    """
    Under normal circumstances,
    the sum of the weights of the layers in a layer folder should be equal to the total number of NFTs we set,
    but when the total number is more than or less than the total number of NFTs,
    we need to redistribute the weights according to the proportion of the layers.
    Of course, this The function is up to the user to decide whether to use it or not.

    The policy for adjusting the weights is quite sample: 
    When the sum of the weights is more or less than the total number of NFTs, 
    each layer's weight will be adjust to (total number * (weight / sum of the weights)).
    When we do not specify weights for some layers, 
    the weights of these layers will be divided equally from the total number of NFTs minus the assigned weights

    详细规则：
    1. 作为Group信标图层的权重要等于以他为信标的图层们的权重之和
    2. 自由图层们的权重之和要相等（所谓自由图层是指 没有混合限制，完全随机的图层

    图层均衡完成之后将会被遗弃放在一个list里面，函数返回权衡后的图层列表

    """

    NFT_totalNumber = layerconfig_json["totalNumber"]
    layers = layerconfig_json["layersOrder"]

    for layer in layers:
        layer_name = layer["name"]
        print(layer_name)
        dir_list = layerinfo_json[layer_name]["dir_list"]
        print(dir_list)
        layer_list = layerinfo_json[layer_name]["layer_list"]
        print(layer_list)
        _sum, counter = count_all_weights(layerinfo_json[layer_name])
        print(_sum, counter)
        print( "_______________________________________________________\n\n")

    # layer_configs = load_lsyers_config(layer_config_path)
    # for config_item in layer_configs:
    #     print(type(config_item).__name__ == "dict")
    #     for key, value in config_item.items():
    #         print("key: ", key)
    #         print("value: ", value)


"""

    Introduction:The operation of getting the total number of weights may seem strange (or even verbose)
    but please refer to a sample layer information to understand

            "Layer1": {
            "existSubdir": true,
            "layer_list": [
                "layer_name1"
            ],
            "dir_list": [
                "subdir1",
                "subdir2",
                "subdir3",
                "subdir4",
                "subdir5"
            ],
            "layer_total_number": xxx,
            "layer_name1": {
                "path": "xxx",
                "weight": -1
            },
            "Blue": [
                {
                    "sublayer_name1": {
                        "path": "xxx",
                        "weight": 100
                    }
                },
                {
                    "sublayer_name2": {
                        "path": "xxx",
                        "weight": -1
                    }
                }
                .
                .
                .
                .
                .
                .
                    ]

    """

def count_layer_list_weights(layer_info):
    """
    It iterates over the layer_list and accumulates the sum of the weights of the layers that have been
    assigned weights
    
    :param layer_info: a dictionary that contains the information of all layers in the model
    :return: The sum and the number of layers of the weights of the layers that have been assigned weights 
    """
    layer_list = layer_info["layer_list"]
    counter = 0  # Accumulate the number of layers that have been assigned weights
    _sum = 0  # the sum of layers' weights that have been assigned weights
    if len(layer_list) > 0:
        for layer in layer_list:  # iterate over the layer_list
            if layer_info[layer]["weight"] != -1:
                _sum = _sum + layer_info[layer]["weight"]
                counter = counter + 1
    return _sum, counter


def count_dir_list_weights(layer_info):
    """
    The function iterates over the subdirectories of the layer_info dictionary, and accumulates the
    weights of the layers that have been assigned weights.
    
    :param layer_info: a dictionary that contains the information of all layers in the model
    :return: The sum of the weights of the layers in the subdirectories that have been assigned weights,
    and the number of layers in the subdirectories that have been assigned weights.
    """
    dir_list = layer_info["dir_list"]
    counter = 0  # Accumulate the number of layers in subdirctors that have been assigned weights
    _sum = 0  # the sum of layers' weights in subdirctors that have been assigned weights
    if len(layer_info["dir_list"]) > 0:
        for dir_item in  dir_list:  # iterate over the layer_list
            sublayer_list = layer_info[dir_item]
            for layer_item in sublayer_list:
                layer_info_temp = list(layer_item.values())
                weight = layer_info_temp[0]["weight"]
                if weight != -1:
                    _sum = _sum + weight
                    counter = counter + 1
    return _sum, counter


def count_all_weights(layer_info):
    """
    It takes a list of layer names and returns the number of weights in each layer and the total number
    of weights in the model.
    
    :param layer_info: a list of dictionaries, each dictionary contains the information of a layer
    :return: The counter of weights and the sum of the weights.
    """

    layer_counter, layer_sum = count_layer_list_weights(layer_info)
    dir_counter, dir_sum = count_dir_list_weights(layer_info)
    return layer_counter + dir_counter, layer_sum + dir_sum
