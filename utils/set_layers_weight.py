import traceback
import logging
import sys
import exceptions
sys.path.append("..")
from CONST_ENV import ENV_PATH as PATH


logging.basicConfig(filename= "../../src/balance_weights.log")

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
        if layer_info["existSubdir"] == False:  # 表明该图层没有所属的信标图层
            balance_weight_in_dir(NFT_totalNumber, layer_info)
        else:
            balance_layerweight_in_subdirs(layerinfo_json, NFT_totalNumber, layer_name)


def balance_weight_in_dir(_SUM, layer_info):
    layer_list = layer_info["layer_list"]
    layers_num = layer_info["layers_number"]
    print(layer_list)
    _sum, counter = count_weights_in_layer_list(_SUM, layer_info)
    print("Sum of weights: ", _sum)
    print("Number of weighted layers: ", counter)
    if _sum == _SUM and counter == len(layer_list):  # The sum of the weights is equal to the total number of NFTs
        print(str(layer_info["name"]) + " layer: Sum of weights match, Pass")
        print("_" * 100 + "\n\n")
    else:
        print(str(layer_info["name"]) + " layer: Sum of weights does not match, reallocating……")
        print("_" * 100 + "\n\n")
        remaining_sum = _SUM - _sum
        remaining_counter = len(layer_list) - counter

        try:
            if _sum != _SUM and counter < len(layer_list):
                raise exceptions.Exit_Some_Layers_Without_Weights_ERROR(layer_info["name"], remaining_sum)
        except  exceptions.Exit_Some_Layers_Without_Weights_ERROR as _ERROR4:
            logging.error(traceback.format_exc())
            print(_ERROR4)
            redistribute_weights_for_noweight_layers(remaining_sum, remaining_counter, layer_info)

        try:
            if remaining_sum < remaining_counter:
                raise exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR(remaining_sum, layer_info["name"], remaining_counter)
        except exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR as _ERROR1:
            logging.error(traceback.format_exc())
            print(_ERROR1)
            sys.exit(0)

        try:
            if counter == len(layer_list):
                raise exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR(layer_info["name"], _sum, _SUM)
        except exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR as _ERROR2:
            logging.error(traceback.format_exc())
            print(_ERROR2)
            redistribute_weights_for_all_layers(_SUM, _sum, layer_info)

        try:
            if counter == 0:
                raise exceptions.All_Layers_Are_Not_Weighted_ERROR(layer_info["name"])
        except exceptions.All_Layers_Are_Not_Weighted_ERROR as _ERROR3:
            logging.error(traceback.format_exc())
            print(_ERROR3)
            redistribute_weights_for_all_noweight_layers(_SUM, layer_info)

    _sum, counter = count_weights_in_layer_list(_SUM, layer_info)
    layer_info["sum_of_weights"] = _sum
    return layer_info


def count_weights_in_dir(_SUM, layer_info):
    dir_list = layer_info["dir_list"]
    _sum = 0
    counter = 0
    for dir_item in dir_list:
        temp_sum, temp_counter = count_weights_in_layer_list(_SUM, layer_info[dir_item])
        _sum += temp_sum
        counter += temp_counter
        print(layer_info["name"], _sum, counter)
    return _sum, counter


def count_weights_in_layer_list(_SUM, layer_info):
    layer_list = layer_info["layer_list"]
    counter = 0  # Accumulate the number of layers that have been assigned weights
    _sum = 0  # the sum of layers' weights that have been assigned weights
    if len(layer_list) > 0:
        for layer in layer_list:  # iterate over the layer_list
            weight = layer_info[layer]["weight"]
            if weight != -1:
                try:
                    if weight >= _SUM:
                        raise exceptions.Current_Layer_Weight_Greater_Than_Given_Weight_ERROR(layer_info["name"], layer, weight, _SUM)
                    _sum += weight
                    counter += 1
                except exceptions.Current_Layer_Weight_Greater_Than_Given_Weight_ERROR as _ERROR:
                    layer_info[layer]["weight"] = -1
                    logging.error(traceback.format_exc())
                    print(_ERROR)
    return _sum, counter

def redistribute_weights_for_all_layers(remaining_sum, _sum, layer_info):
    layer_list = layer_info["layer_list"]
    remaining_counter = len(layer_list)
    for layer in layer_list:
        if remaining_counter > 1:
            new_weight = int(remaining_sum * layer_info[layer]["weight"] / _sum)
            layer_info[layer]["weight"] = new_weight
            remaining_sum -= new_weight
            remaining_counter -= 1
        else:
            layer_info[layer]["weight"] = remaining_sum
    print(layer_info)


def redistribute_weights_for_all_noweight_layers(_SUM, layer_info):
    layer_list = layer_info["layer_list"]
    remaining_counter = len(layer_list)
    average_value = remaining_sum // remaining_counter
    for layer in layer_list:
        if remaining_counter > 1:
            layer_info[layer]["weight"] = average_value
            remaining_sum -= average_value
            remaining_counter -= 1
        else:
            layer_info[layer]["weight"] = remaining_sum
    print(layer_info)


def redistribute_weights_for_noweight_layers(remaining_sum, remaining_counter, layer_info):
    layer_list = layer_info["layer_list"]
    average_value = remaining_sum // remaining_counter
    for layer in layer_list:
        if layer_info[layer]["weight"] == -1:
            if remaining_counter > 1:
                layer_info[layer]["weight"] = average_value
                remaining_sum -= average_value
                remaining_counter -= 1
            else:
                layer_info[layer]["weight"] = remaining_sum
    print(layer_info)

def balance_layerweight_in_subdirs(layerinfo_json, _SUM, layer_name):
    current_layer_info = layerinfo_json[layer_name]
    _sum, counter = count_weights_in_dir(_SUM, current_layer_info)
    remaining_sum = _SUM - _sum
    remaining_counter = len(layer_list) - counter
    print(_sum, counter)
    # 先判断图层类型
    if current_layer_info["isGroupSet"] == True and "groupBy" not in current_layer_info:
        # 再判断是不是满足规则
        if _sum == _SUM and counter == len(layer_list):  # The sum of the weights is equal to the total number of NFTs
            print(str(layer_info["name"]) + " layer: Sum of weights match, Pass")
            print("_" * 100 + "\n\n")

    # 如果自身作为信标图层，则按照 balance_weight_in_dir（）的方式进行均衡

    # 如果有所属的信标图层，则先读取到信标图层对应文件夹的权重之和，然后根据这个权重进行重新分配

    # 如果如果有所属的信标图层，但同时自己又含有一些信标图层不含有的分类，则按照常规方法进行均衡

    # 均衡之后要把新的权重之和放在本图层的json信息中


def redistribute_beacon_layer():
    print()

def redistribute_grouped_sublayers():
    print()

def redistribute_beacon_grouped_sublayers():
    print()