import os
base_path = os.getcwd()
layer_path = os.path.join(base_path, "layers")

a = []
for root, dirs, files in os.walk(layer_path):

    a.append({
        "root": root,
        "content":
        {
            "dirs": dirs,
            "files": files,
        }
    })



    # print('root:',root)
    # print('dirs:',dirs)
    # print('files:',files)
