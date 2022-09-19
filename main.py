# import os


# listDir=os.listdir(layerPath)#获取当前目录下的所有内容
# print(listDir)

import os#适应python
file_type = dict()  #创建一个空的字典，用来存储我们的结果
#os.chdir(r'F:\\python_code ')   #更改当前工作目录,其实不用更改，一直是这个路径
# current_work_dir = os.curdir： 指代当前目录，在windows系统下是'.'
path = os.getcwd()#获取当前路径
layerPath = os.path.join(path,"layers")
all_file = os.listdir(layerPath)  #用列表列举当前目录中的文件名
#print(all_file )
for each_file in all_file:   #依次提取这个列表中的每一个元素（路径）
    if os.path.isdir(each_file) == True:   #判断这个路径是否表示文件夹,如果这是文件夹，就==True,如果不是文件夹就跳到else
        file_type.setdefault('文件夹',0)  #返回字典中键对应的值，但如果键不存在于字典中，将会添加键并将值设为default
        file_type['文件夹'] += 1
    else:  # 如果不是文件夹，即是有后缀的那些文件
        ext = os.path.splitext(each_file)[1]   #分离文件名与扩展名，返回元组(f_name, f_extension)[1]这里的意思是元组中第二个名字即扩展名
        file_type.setdefault(ext, 0)   #将这个拓展名放置在字典中
        file_type[ext] +=1#如果没有这个扩展名就添加，如果有这个扩展名就+1

#下面我们来打印结果
for type_file in file_type:
    print('该文件夹下共有类型为【%s】的文件【%d】个'%(type_file,file_type[type_file]))


