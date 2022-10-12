import sys
sys.path.append("..")
from CONST_ENV import ENV_PATH as PATH


class Current_Layer_Weight_Greater_Than_Given_Weight_ERROR(Exception):
    def __init__(self, dir_name, layer_name, current_weight, given_weight):
        self.dir_name = dir_name
        self.layer_name = layer_name
        self.current_weight = current_weight
        self.given_weight = given_weight

    def __str__(self):
        ERROR_INFO = "The weight of " + self.layer_name + " layer in " + self.dir_name + " is "\
        + str(self.current_weight) + " , which is greater than the given weight of " + str(self.given_weight) + \
        ", going to set " + "weight" + " = -1"
        return ERROR_INFO


class Remaining_Sum_Less_Than_Remaining_Counter_ERROR(Exception):
    def __init__(self, remaining_sum, dir_name, remaining_counter):
        self.remaining_sum = remaining_sum
        self.remaining_counter = remaining_counter

    def __str__(self):
        ERROR_INFO = "The remaining sum in " + self.dir_name + " is "+ str(self.remaining_sum) + ", which is less than remaining counter " + self.remaining_counter + \
        ". I have no idea to redistribute weights for the layers. System exit."
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

class Exit_Layers_Without_Weights_ERROR(Exception):
    def __init__(self, dir_name, given_weight):
        self.dir_name = dir_name
        self.given_weight = given_weight

    def __str__(self):
        ERROR_INFO = "There are unweighted layers in folder " + self.dir_name + \
        " They will equally share the given weights of " +  str(self.given_weight)
        return ERROR_INFO

