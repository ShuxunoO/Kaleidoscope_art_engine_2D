import traceback
import logging
import sys
sys.path.append("..")
from CONST_ENV import ENV_PATH as PATH

logging.basicConfig(filename= PATH.LAYER_PATH)

class Current_Weight_Greater_Than_Given_Weight(Exception):
    def __init__(self, dir_name, layer_name, current_weight, given_weight):
        self.dir_name = dir_name
        self.layer_name = layer_name
        self.current_weight = current_weight
        self.given_weight = given_weight

    def __str__(self):
        ERROR_INFO = "The weight of " + self.layer_name + " layer in the " + self.dir_name + " is "\
        + str(self.current_weight) + " , which is greater than the given weight of " + str(self.given_weight)
