import json
import os

# load json file


# write json file
def save_json(save_path,filename,data):
    print(save_path)
    file_path = os.path.join(save_path,filename + ".json")
    with open(file_path,'w') as file:
        json.dump(data, file, indent=4)
