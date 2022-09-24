import json
import os

# load json file


# write json file
def save_json(save_path, filename, data):
    print(save_path)
    file_path = os.path.join(save_path,filename + ".json")
    with open(file_path,'w') as file:
        json.dump(data, file, indent=4)


# get_layersinfos
def get_layersinfos(base_path, file_name):
    current_path = os.path.join(base_path, file_name)
    layer_list = os.listdir(current_path)
    # print(layer_list)
    layer_dict = {}
    for item in layer_list:
        sub_path = os.path.join(current_path, item)
        if os.path.isdir(sub_path):
            print("Dir")
            sublayer_list = os.listdir(sub_path)
            sublayer_dict = {}
            sublayer_dict[item] = [{tempt_sublayer:{
                "path" : os.path.join(sub_path, tempt_sublayer),
                "weight": 10,
                "counter" : 2,
                "conflictElements": "xxx"
            }} for tempt_sublayer in sublayer_list]
            layer_dict[file_name] = sublayer_dict
            return layer_dict
        else:
            print("File")
            layer_dict[file_name] = [{layer:{
                "path" : os.path.join(current_path, layer),
                "weight": 10,
                "counter" : 2,
                "conflictElements": "xxx"
            }} for layer in layer_list]
            return layer_dict


