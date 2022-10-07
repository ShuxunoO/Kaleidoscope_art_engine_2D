
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

    # print(layerconfig_json ,"\n\n")
    # print(layerinfo_json , "\n\n")
    sum = layerconfig_json["totalNumber"]
    layers = layerconfig_json["layersOrder"]

    for layer in layers:
        layer_name = layer["name"]
        print(layer_name)
        dir_list = layerinfo_json[layer_name]["dir_list"]
        print(dir_list)
        layer_list = layerinfo_json[layer_name]["layer_list"]
        print(layer_list)
        counter = 0  # Sum of cumulative weights
        num_of_noweight_layers = 0  # Record the number of layers with no assigned weights


    # layer_configs = load_lsyers_config(layer_config_path)
    # for config_item in layer_configs:
    #     print(type(config_item).__name__ == "dict")
    #     for key, value in config_item.items():
    #         print("key: ", key)
    #         print("value: ", value)
