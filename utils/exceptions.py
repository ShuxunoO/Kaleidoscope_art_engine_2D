import traceback
import logging
import sys
sys.path.append("..")
from CONST_ENV import ENV_PATH as PATH
logging.basicConfig(filename="../src/balance_weights.log")

class Current_Layer_Weight_Greater_Than_Given_Weight_ERROR(Exception):
    def __init__(self, dir_name, layer_name, current_weight, given_weight):
        self.dir_name = dir_name
        self.layer_name = layer_name
        self.current_weight = current_weight
        self.given_weight = given_weight

    def __str__(self):
        ERROR_INFO = "The weight of " + self.layer_name + " layer in " + self.dir_name + " is "\
        + str(self.current_weight) + " , which is not less than the given weight of " + str(self.given_weight) + \
        ", going to set " + "weight" + " = -1"
        return ERROR_INFO



class Remaining_Sum_Less_Than_Remaining_Counter_ERROR(Exception):
    def __init__(self, remaining_sum, dir_name, remaining_counter):
        self.remaining_sum = remaining_sum
        self.dir_name = dir_name
        self.remaining_counter = remaining_counter

    def __str__(self):
        ERROR_INFO = "The remaining weight in " + self.dir_name + " is "+ str(self.remaining_sum) + ", which is less than remaining counter " + str(self.remaining_counter) + \
        ". program has no idea to redistribute weights for the layers. Please allocate the weights of the layers reasonably!  System exit."
        return ERROR_INFO


class Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR(Exception):
    def __init__(self, dir_name, sum_weight, given_weight):
        self.dir_name = dir_name
        self.sum_weight = sum_weight
        self.given_weight = given_weight

    def __str__(self):
        ERROR_INFO = "The sum of  layers' weights in " + self.dir_name + " is " + str(self.sum_weight)\
        + " , which is not equal to the given weight of " + str(self.given_weight) + \
        ", going to redistribute weights for all layers"
        return ERROR_INFO

# def raise_Sum_Of_Weights_Is_Not_Equal_To_Given_Weight_ERROR(dir_name, sum_weight, given_weight):
#     def decorator(_fun):
#         def wrapper(*args, **kwargs):
#             try:
#                 raise Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR(
#                         dir_name, sum_weight, given_weight)
#             except Sum_Of_Layer_Weights_Is_Not_Equal_To_Given_Weight_ERROR as _ERROR:
#                 logging.error(traceback.format_exc())
#                 print(_ERROR)
#             return _fun(*args, **kwargs)
#         return wrapper
#     return decorator


class All_Layers_Are_Not_Weighted_ERROR(Exception):
    def __init__(self, dir_name):
        self.dir_name = dir_name

    def __str__(self):
        ERROR_INFO = "All the layers in " + self.dir_name + " are not weighted, "+\
            "so program is going to redistribute weights for all layers"
        return ERROR_INFO

class Exit_Some_Layers_Without_Weights_ERROR(Exception):
    def __init__(self, dir_name, given_weight):
        self.dir_name = dir_name
        self.given_weight = given_weight

    def __str__(self):
        ERROR_INFO = "There are unweighted layers in folder " + self.dir_name + \
        " They will equally share the given weights of " +  str(self.given_weight)
        return ERROR_INFO

