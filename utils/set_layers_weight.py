from CONST_ENV import ENV_PATH as PATH
import traceback
import logging
import sys
import exceptions
sys.path.append("..")
logging.basicConfig(filename="../../src/balance_weights.log")

"""
"""

def balance_layerweight(layerconfig_json, layerinfo_json):
    _SUM = layerconfig_json["totalNumber"]
    layers_order = layerconfig_json["layersOrder"]
    for layer in layers_order:
        layer_name = layer["name"]
        layer_info = layerinfo_json[layer_name]
        print(layer_name)
        if layer_info["existSubdir"] == False:  # 表明该图层没有所属的信标图层
            layer_list = layer_info["layer_list"]
            balance_layer_weight_in_layerlist(_SUM, layer_list, layer_info)
        else:
            print("existSubdir")
            balance_layer_weight_in_subdirs(
                layerinfo_json, _SUM, layer_name)

def balance_layer_weight_in_layerlist(_SUM, layer_list, layer_info):
    layers_num = layer_info["layers_number"]
    print(layer_list)
    _sum, counter = count_weights_in_layer_list(_SUM, layer_list, layer_info)
    print("Sum of weights: ", _sum)
    print("Number of weighted layers: ", counter)

    if _sum == _SUM and counter == layers_num:  # The sum of the weights is equal to the total number of NFTs
        print(str(layer_info["name"]) + " layer: Sum of weights match, Pass")
        print("_" * 100 + "\n\n")
    else:
        print(str(layer_info["name"]) +
              " layer: Sum of weights does not match, reallocating……")
        print("_" * 100 + "\n\n")
        remaining_sum = _SUM - _sum
        remaining_counter = layers_num - counter

        if _sum != _SUM and 0 < counter < layers_num:  # 有些图层被赋值，有些图层未被赋值
            try:
                raise exceptions.Exit_Some_Layers_Without_Weights_ERROR(
                    layer_info["name"], remaining_sum)
            except exceptions.Exit_Some_Layers_Without_Weights_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
                redistribute_weights_for_noweight_layers(
                    remaining_sum, remaining_counter, layer_list, layer_info)

        if counter == 0:  # 图层一个都没有被赋值
            try:
                raise exceptions.All_Layers_Are_Not_Weighted_ERROR(
                    layer_info["name"])
            except exceptions.All_Layers_Are_Not_Weighted_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
                redistribute_weights_for_all_noweight_layers(
                    _SUM, remaining_counter, layer_list, layer_info)

        if counter == layers_num:  # 图层均被赋值，但权重之和不满足指定值
            try:
                raise exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR(
                    layer_info["name"], _sum, _SUM)
            except exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
            redistribute_weights_for_all_layers(
                _SUM, counter, _sum, layer_list, layer_info)

        if remaining_sum < remaining_counter:  # 没有很好的解决办法，程序停止
            try:
                raise exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR(
                    remaining_sum, layer_info["name"], remaining_counter)
            except exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
                sys.exit(0)
    update_sum_of_weights(_SUM, layer_list, [], layer_info, _type = "root_dir")
    layer_info["is_balanced"] = True


def balance_layer_weight_in_subdirs(layerinfo_json, _SUM, layer_name):
    layer_info = layerinfo_json[layer_name]
    # 先判断图层类型
    if layer_info["isBeaconLayer"] == True and "groupBy" not in layer_info:  # 只是信标层
        dir_list = layer_info["dir_list"]
        redistribute_beacon_layer(_SUM, dir_list, layerinfo_json[layer_name])
    elif layer_info["isBeaconLayer"] == False and "groupBy" in layer_info:  # 只是从属层
        # 信标层必须要在子层之前均衡
        dir_list = layer_info["dir_list"]
        redistribute_subordinate_layer(layerinfo_json, dir_list, layer_name)


    # 如果有所属的信标图层，则先读取到信标图层对应文件夹的权重之和，然后根据这个权重进行重新分配

    # 如果如果有所属的信标图层，但同时自己又含有一些信标图层不含有的分类，则按照常规方法进行均衡


def count_weights_in_dir_list(_SUM, dir_list, layer_info):
    _sum = 0
    counter = 0
    for dir_item in dir_list:
        layer_list = layer_info[dir_item]["layer_list"]
        temp_sum, temp_counter = count_weights_in_layer_list(
            _SUM, layer_list, layer_info[dir_item])
        _sum += temp_sum
        counter += temp_counter
        print(layer_info["name"], _sum, counter)
    return _sum, counter

def count_weights_in_layer_list(_SUM, layer_list, layer_info):
    counter = 0  # Accumulate the number of layers that have been assigned weights
    _sum = 0  # the sum of layers' weights that have been assigned weights
    if len(layer_list) > 0:
        for layer in layer_list:  # iterate over the layer_list
            weight = layer_info[layer]["weight"]
            if weight != -1:
                try:
                    if weight >= _SUM:
                        raise exceptions.Current_Layer_Weight_Greater_Than_Given_Weight_ERROR(
                            layer_info["name"], layer, weight, _SUM)
                    _sum += weight
                    counter += 1
                except exceptions.Current_Layer_Weight_Greater_Than_Given_Weight_ERROR as _ERROR:
                    layer_info[layer]["weight"] = -1
                    logging.error(traceback.format_exc())
                    print(_ERROR)
    return _sum, counter


def update_sum_of_weights(_SUM, layer_list, dir_list, layer_info, _type):
    if _type == "root_dir":
        _sum, _ = count_weights_in_layer_list(_SUM, layer_list, layer_info)
        print("sum_of_weights after balance", _sum)
        layer_info["sum_of_weights"] = _sum
    else:  # 更新含有子文件夹的父文件夹权重
        _sum, _ = count_weights_in_dir_list(_SUM, dir_list, layer_info)
        layer_info["sum_of_weights"] = _sum


# 全有赋值，但总和不对
def redistribute_weights_for_all_layers(_SUM, remaining_counter, _sum, layer_list, layer_info):
    remaining_sum = _SUM
    for layer in layer_list:
        print(layer)
        if remaining_counter > 1:
            new_weight = round(_SUM * layer_info[layer]["weight"] / _sum)
            print(new_weight)
            layer_info[layer]["weight"] = new_weight
            remaining_sum -= new_weight
            remaining_counter -= 1
        else:
            layer_info[layer]["weight"] = remaining_sum
    return remaining_counter

# 一个赋值都没有
def redistribute_weights_for_all_noweight_layers(remaining_sum, remaining_counter, layer_list, layer_info):
    average_value = remaining_sum // remaining_counter
    for layer in layer_list:
        if remaining_counter > 1:
            layer_info[layer]["weight"] = average_value
            remaining_sum -= average_value
            remaining_counter -= 1
        else:
            layer_info[layer]["weight"] = remaining_sum
    # print(layer_info)
    return remaining_sum, remaining_counter

# 个别没有赋值的情况
def redistribute_weights_for_noweight_layers(remaining_sum, remaining_counter, layer_list, layer_info):
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
    return remaining_sum, remaining_counter


def redistribute_beacon_layer( _SUM, dir_list, layer_info):
    print(dir_list)
    layers_num = layer_info["layers_number"]
    _sum, counter = count_weights_in_dir_list(_SUM, dir_list, layer_info)
    remaining_sum = _SUM - _sum
    remaining_counter = layers_num - counter
    print(_sum, counter)
    if _sum == _SUM and counter == layers_num:  # The sum of the weights is equal to the total number of NFTs
        print(str(layer_info["name"]) + " layer: Sum of weights match, Pass")
        print("_" * 100 + "\n\n")
    else:
        print(str(layer_info["name"]) +
              " layer: Sum of weights does not match, reallocating……")
        print("_" * 100 + "\n\n")

        try:
            if remaining_sum < remaining_counter:  # 没有很好的解决办法，程序停止
                raise exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR(
                    remaining_sum, layer_info["name"], remaining_counter)
        except exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR as _ERROR:
            logging.error(traceback.format_exc())
            print(_ERROR)
            sys.exit(0)

        try:
            if _sum != _SUM and 0 < counter < layers_num:  # 有些图层被赋值，有些图层未被赋值
                raise exceptions.Exit_Some_Layers_Without_Weights_ERROR(
                    layer_info["name"], remaining_sum)
        except exceptions.Exit_Some_Layers_Without_Weights_ERROR as _ERROR:
            logging.error(traceback.format_exc())
            print(_ERROR)
            for dir_item in dir_list:
                sublayer_list = layer_info[dir_item]["layer_list"]
                remaining_sum, remaining_counter = redistribute_weights_for_noweight_layers(
                    remaining_sum, remaining_counter, sublayer_list, layer_info[dir_item])
                update_sum_of_weights(_SUM, sublayer_list,[], layer_info[dir_item], _type = "sub_dir")


        try:
            if counter == layers_num:  # 图层均被赋值，但权重之和不满足指定值
                raise exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR(
                    layer_info["name"], _sum, _SUM)
        except exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR as _ERROR:
            logging.error(traceback.format_exc())
            print(_ERROR)
            for dir_item in dir_list:
                sublayer_list = layer_info[dir_item]["layer_list"]
                remaining_counter = redistribute_weights_for_all_layers(
                    remaining_sum, remaining_counter, _sum, layer_info[dir_item])
                update_sum_of_weights(_SUM, sublayer_list, [], layer_info[dir_item], _type = "sub_dir")

        try:
            if counter == 0:  # 图层一个都没有被赋值
                raise exceptions.All_Layers_Are_Not_Weighted_ERROR(
                    layer_info["name"])
        except exceptions.All_Layers_Are_Not_Weighted_ERROR as _ERROR:
            logging.error(traceback.format_exc())
            print(_ERROR)
            for dir_item in dir_list:
                sublayer_list = layer_info[dir_item]["layer_list"]
                remaining_sum, remaining_counter = redistribute_weights_for_all_noweight_layers(
                    remaining_sum, remaining_counter, layer_info[dir_item])
                update_sum_of_weights(_SUM, sublayer_list, [], layer_info[dir_item], _type = "sub_dir")
    update_sum_of_weights(_SUM, [], dir_list, layer_info, _type = "root_dir")
    layer_info["is_balanced"] = True


def redistribute_subordinate_layer(layerinfo_json, dir_list, layer_name):
    layer_info = layerinfo_json[layer_name]
    beacon = layer_info["groupBy"]
    beacon_layer = layerinfo_json[beacon]
    for dir_item in dir_list:
        _SUM = beacon_layer[dir_item]["sum_of_weights"]  # 拿到信标层的权重之和
        layer_list = layer_info[dir_item]["layer_list"]  # 拿到要均衡的子列表
        balance_layer_weight_in_layerlist(_SUM, layer_list, layer_info[dir_item])
    layer_info["is_balanced"] = True

def redistribute_beacon_subordinate_layer():
    print()
