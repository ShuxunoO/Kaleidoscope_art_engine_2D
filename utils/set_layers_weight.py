import traceback
import logging
import sys
import exceptions
sys.path.append("..")
logging.basicConfig(filename="../../src/balance_weights.log")

"""
均衡模块

"""


def balance_layer_weight(layerconfig_json, layerinfo_json):
    print("\n\n"+"^^" * 50 + "\n\n")
    _SUM = layerconfig_json["totalNumber"]
    layers_order = layerconfig_json["layersOrder"]
    # 先优先均衡信标层的权重
    print("先优先均衡信标层的权重")
    for layer in layers_order:

        layer_name = layer["name"]
        layer_info = layerinfo_json[layer_name]
        if layer_info["isBeaconLayer"] == True:
            print(layer_name)
            balance_layer_weight_in_subdirs(
                layerinfo_json, _SUM, layer_name)
            print(layer_info)

    for layer in layers_order:
        layer_name = layer["name"]
        print(layer_name)
        layer_info = layerinfo_json[layer_name]
        if layer_info["existSubdir"] == False:  # 表明该图层没有所属的信标图层
            layer_list = layer_info["layer_list"]
            balance_layer_weight_in_layer_list(_SUM, layer_list, layer_info)
            print(layer_info)
        else:
            # 只处理没有处理过的图层
            if layer_info["is_balanced"] == False:
                balance_layer_weight_in_subdirs(
                    layerinfo_json, _SUM, layer_name)
                print(layer_info)
    return layerinfo_json

# 处理不受任何约束的图层


def balance_layer_weight_in_layer_list(_SUM, layer_list, layer_info):
    if layer_info["is_balanced"] == True:
        return
    layers_num = layer_info["layers_number"]
    _sum, counter = count_weights_in_layer_list(_SUM, layer_list, layer_info)
    print("Sum of weights: ", _sum)
    print("Number of weighted layers: ", counter)

    if _sum == _SUM and counter == layers_num:  # The sum of the weights is equal to the total number of NFTs
        print(str(layer_info["name"]) + " layer: Sum of weights match, Pass")
        print("_" * 100 + "\n\n")
        return
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

        elif counter == 0:  # 图层一个都没有被赋值
            try:
                raise exceptions.All_Layers_Are_Not_Weighted_ERROR(
                    layer_info["name"])
            except exceptions.All_Layers_Are_Not_Weighted_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
                redistribute_weights_for_all_noweight_layers(
                    _SUM, remaining_counter, layer_list, layer_info)

        elif counter == layers_num:  # 图层均被赋值，但权重之和不满足指定值
            try:
                raise exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR(
                    layer_info["name"], _sum, _SUM)
            except exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
            redistribute_weights_for_all_layers(
                _SUM, counter, _sum, layer_list, layer_info)

        else:  # 没有很好的解决办法，程序停止
            try:
                raise exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR(
                    remaining_sum, layer_info["name"], remaining_counter)
            except exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
                sys.exit(0)
    update_sum_of_weights(_SUM, layer_list, [], layer_info, 1)

# 均衡 含有子文件夹的图层


def balance_layer_weight_in_subdirs(layerinfo_json, _SUM, layer_name):
    layer_info = layerinfo_json[layer_name]
    if layer_info["is_balanced"] == True:
        return
    # 先判断图层类型
    if layer_info["isBeaconLayer"] == True and "groupBy" not in layer_info:  # 只是信标层
        dir_list = layer_info["dir_list"]
        redistribute_beacon_layer(_SUM, dir_list, layerinfo_json[layer_name])
    elif layer_info["isBeaconLayer"] == False and "groupBy" in layer_info:  # 只是从属层
        dir_list = layer_info["dir_list"]
        redistribute_subordinate_layer(layerinfo_json, dir_list, layer_name)
    else:
        redistribute_beacon_subordinate_layer(layerinfo_json, _SUM, layer_name)

# 记数文件夹列表中权重


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

# 记数图层列表中的权重


def count_weights_in_layer_list(_SUM, layer_list, layer_info):
    counter = 0  # Accumulate the number of layers that have been assigned weights
    _sum = 0  # the sum of layers' weights that have been assigned weights
    if len(layer_list) > 0:
        for layer in layer_list:  # iterate over the layer_list
            weight = layer_info[layer]["weight"]
            if weight != -1:
                try:
                    if weight >= _SUM and len(layer_list) > 1:
                        raise exceptions.Current_Layer_Weight_Greater_Than_Given_Weight_ERROR(
                            layer_info["name"], layer, weight, _SUM)
                    _sum += weight
                    counter += 1
                except exceptions.Current_Layer_Weight_Greater_Than_Given_Weight_ERROR as _ERROR:
                    layer_info[layer]["weight"] = -1
                    logging.error(traceback.format_exc())
                    print(_ERROR)
    return _sum, counter

# 更新图层的权重


def update_sum_of_weights(_SUM, layer_list, dir_list, layer_info, flag):
    if flag == 1:  # 没有子文件夹
        _sum, _ = count_weights_in_layer_list(_SUM, layer_list, layer_info)
        print("sum_of_weights after balance", _sum)
        layer_info["sum_of_weights"] = _sum
        layer_info["is_balanced"] = True
    if flag == 2:  # 更新含有子文件夹的父文件夹权重
        _sum, _ = count_weights_in_dir_list(_SUM, dir_list, layer_info)
        layer_info["sum_of_weights"] = _sum
        layer_info["is_balanced"] = True


# 全有赋值，但总和不对
def redistribute_weights_for_all_layers(_SUM, remaining_counter, _sum, layer_list, layer_info):
    remaining_sum = _SUM
    for layer in layer_list:
        if remaining_counter > 1:
            new_weight = round(_SUM * layer_info[layer]["weight"] / _sum)
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
            temp_checker = layer_info[layer]["weight"]
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
    return remaining_sum, remaining_counter


def redistribute_beacon_layer(_SUM, dir_list, layer_info):
    # 先计算出信标层的总个数
    layers_num = 0
    for dir_item in dir_list:
        layers_num += layer_info[dir_item]["layers_number"]
    _sum, counter = count_weights_in_dir_list(_SUM, dir_list, layer_info)
    remaining_sum = _SUM - _sum
    remaining_counter = layers_num - counter
    if _sum == _SUM and counter == layers_num:  # The sum of the weights is equal to the total number of NFTs
        print(str(layer_info["name"]) + " layer: Sum of weights match, Pass")
        print("_" * 100 + "\n\n")
        return
    else:
        print(str(layer_info["name"]) +
              " layer: Sum of weights does not match, reallocating……")
        print("_" * 100 + "\n\n")

        # 有些图层被赋值，有些图层未被赋值
        if _sum != _SUM and 0 < counter < layers_num:
            try:
                raise exceptions.Exit_Some_Layers_Without_Weights_ERROR(
                    layer_info["name"], remaining_sum)
            except exceptions.Exit_Some_Layers_Without_Weights_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
                for dir_item in dir_list:
                    sublayer_list = layer_info[dir_item]["layer_list"]
                    remaining_sum, remaining_counter = redistribute_weights_for_noweight_layers(
                        remaining_sum, remaining_counter, sublayer_list, layer_info[dir_item])
                    update_sum_of_weights(
                        _SUM, sublayer_list, [], layer_info[dir_item], 1)

        # 图层均被赋值，但权重之和不满足指定值
        elif counter == layers_num:
            try:
                raise exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR(
                    layer_info["name"], _sum, _SUM)
            except exceptions.Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
                for dir_item in dir_list:
                    sublayer_list = layer_info[dir_item]["layer_list"]
                    remaining_counter = redistribute_weights_for_all_layers(
                        remaining_sum, remaining_counter, _sum, layer_info[dir_item])
                    update_sum_of_weights(
                        _SUM, sublayer_list, [], layer_info[dir_item], 1)

        elif counter == 0:  # 图层一个都没有被赋值
            try:
                raise exceptions.All_Layers_Are_Not_Weighted_ERROR(
                    layer_info["name"])
            except exceptions.All_Layers_Are_Not_Weighted_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
                for dir_item in dir_list:
                    sublayer_list = layer_info[dir_item]["layer_list"]
                    remaining_sum, remaining_counter = redistribute_weights_for_all_noweight_layers(
                        remaining_sum, remaining_counter, layer_info[dir_item])
                    update_sum_of_weights(
                        _SUM, sublayer_list, [], layer_info[dir_item], 1)

        # 没有很好的解决办法，程序停止
        else:
            try:
                raise exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR(
                    remaining_sum, layer_info["name"], remaining_counter)
            except exceptions.Remaining_Sum_Less_Than_Remaining_Counter_ERROR as _ERROR:
                logging.error(traceback.format_exc())
                print(_ERROR)
                sys.exit(0)

    update_sum_of_weights(_SUM, [], dir_list, layer_info, 2)


# 分配从属层的权重
def redistribute_subordinate_layer(layerinfo_json, dir_list, layer_name):
    layer_info = layerinfo_json[layer_name]
    beacon = layer_info["groupBy"]
    beacon_layer = layerinfo_json[beacon]
    for dir_item in dir_list:
        beacon_sum = beacon_layer[dir_item]["sum_of_weights"]  # 拿到信标层的权重之和
        sublayer_list = layer_info[dir_item]["layer_list"]  # 拿到要均衡的子列表
        balance_layer_weight_in_layer_list(
            beacon_sum, sublayer_list, layer_info[dir_item])
        update_sum_of_weights(beacon_sum, sublayer_list,
                              [], layer_info[dir_item], 1)
    update_sum_of_weights(
        beacon_layer["sum_of_weights"], [], dir_list, layer_info, 2)


def redistribute_beacon_subordinate_layer(layerinfo_json, _SUM, layer_name):
    layer_info = layerinfo_json[layer_name]
    dir_list = layer_info["dir_list"]
    beacon = layer_info["groupBy"]
    beacon_layer = layerinfo_json[beacon]
    beacon_dir_list = beacon_layer["dir_list"]
    # 两个列表取交集得到交集附属子文件夹列表
    subordinate_dir_list = list(
        set(dir_list).intersection(set(beacon_dir_list)))
    print("subordinate_dir_list:", subordinate_dir_list)
    # 两个列表取差集得到新的信标文件夹列表
    new_beacon_dir_list = list(set(dir_list).difference(set(beacon_dir_list)))
    # 先分配附属子层的文件夹
    print("new_beacon_dir_list", new_beacon_dir_list)
    redistribute_subordinate_layer(
        layerinfo_json, subordinate_dir_list, layer_name)
    _sum, _ = count_weights_in_dir_list(_SUM, subordinate_dir_list, layer_info)
    remaining_sum = _SUM - _sum
    print("remaining_sum: ", remaining_sum)
    # 分配新的信标层权重
    redistribute_beacon_layer(remaining_sum, new_beacon_dir_list, layer_info)
    update_sum_of_weights(_SUM, [], dir_list, layer_info, 2)
