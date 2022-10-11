from 

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

    图层均衡完成之后将会被一起放在一个list里面，函数返回权衡后的图层列表

"""
def balance_layerweight(layerconfig_json, layerinfo_json):

    NFT_totalNumber = layerconfig_json["totalNumber"]
    layers = layerconfig_json["layersOrder"]
    for layer in layers:
        layer_name = layer["name"]
        layer_info = layerinfo_json[layer_name]
        print(layer_name)
        if layer_info["existSubdir"] == False:  # 表明该图层不受任何限制
            balance_layerweight_in_dir(NFT_totalNumber, layer_info)
        else:
            balance_layerweight_in_subdirs(layerinfo_json, layer_info)
            #TODO：1.根据 dir_list 去限制他图层那里去拿总权重
            # 2. 统计一下 sum  和 counter的数值是不是正好，如果不是就用总权重去给当前子文件夹做均衡
            print()
        # 每一层图层所有layer_list的权重之和必须相等


def balance_layerweight_in_dir(_SUM, layer_info):
    layer_list = layer_info["layer_list"]
    print(layer_list)
    _sum, counter = count_weights_in_layer_list(layer_info)
    print("Sum of weights: ", _sum)
    print("Number of weighted layers: ", counter)
    if _sum == _SUM and counter == len(layer_list):  # 所有权重都已经设计好了
        print(str(layer_info["name"]) + " layer: Sum of weights match, Pass")
        print("_" * 30 + "\n\n")
    else:
        print(str(layer_info["name"]) + " layer: Sum of weights does not match, reallocating……")
        print("_" * 30 + "\n\n")
        remaining_sum = _SUM - _sum
        remaining_counter = layer_info["layer_total_number"] - counter
        average_value = remaining_sum // remaining_counter
        for layer in layer_list:
            if layer_info[layer]["weight"] == -1:
                if remaining_counter > 1:
                    layer_info[layer]["weight"] = average_value
                    remaining_sum -= average_value
                    remaining_counter -= 1
                else:
                    layer_info[layer]["weight"] = remaining_sum
    # print(layer_info)
    return layer_info


def count_weights_in_layer_list(layer_info):
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
                _sum += layer_info[layer]["weight"]
                counter += 1
    return _sum, counter


def balance_layerweight_in_subdirs(layerinfo_json, layer_info):
    dir_list = layer_info["dir_list"]
    for dir_item in dir_list:
        # 拿到分组层的名字
        layer_beacon = layer_info["groupBy"]
        # 拿到拿到分组层的名字权重
        _SUM = layerinfo_json[layer_beacon][dir_item]["weight"]
        print("layer_beacon weight: ", layer_beacon, dir_item, _SUM)
        balance_layerweight_in_subdir(_SUM, layer_info[dir_item])


def balance_layerweight_in_subdir(_SUM, subdir_info):
    # 计算当前子文件夹中图层的权重之和以及赋权图层的数量
    _sum, counter = count_weights_in_subdir(subdir_info)
    print(_sum, counter)
    if _sum == _SUM and counter == len(layer_info[dir_item]):
        print(str(dir_item) + " layer: Sum of weights match, Pass")
        print("_" * 30 + "\n\n")
    else:
        print("subdir" + " Sum of weights does not match, reallocating……")
        print("_" * 30 + "\n\n")
        remaining_sum = _SUM - _sum
        remaining_counter = len(subdir_info["layer_list"]) - counter
        average_value = remaining_sum // remaining_counter
        layer_list = subdir_info["layer_list"]
        for layer in layer_list:
            if subdir_info[layer]["weight"] == -1:
                if remaining_counter > 1:
                    subdir_info[layer]["weight"] = average_value
                    remaining_sum -= average_value
                    remaining_counter -= 1
                else:
                    subdir_info[layer]["weight"] = remaining_sum


def count_weights_in_subdir(subdir_info):
    layer_list = subdir_info["layer_list"]
    counter = 0  # Accumulate the number of layers in subdirctors that have been assigned weights
    _sum = 0  # the sum of layers' weights in subdirctors that have been assigned weights
    for layer in layer_list:
        weight = subdir_info[layer]["weight"]
        if weight != -1:
            _sum += weight
            counter += 1
    return _sum, counter

