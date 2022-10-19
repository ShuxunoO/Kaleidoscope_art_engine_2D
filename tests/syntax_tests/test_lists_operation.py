# # 两个列表取交集
# list_1 = [1,2,3]
# list_2 = [2,3,4]
# print(list(set(list_1) & set(list_2)))
# print(list(set(list_1).intersection(set(list_2))))


# # 两个集合取并集
# list_1 = [1,2,3]
# list_2 = [2,3,4]
# print(list(set(list_1) | set(list_2)))
# print(list(set(list_1).union(set(list_2))))

# # 两个集合取差集
# list_1 = [1,2,3]
# list_2 = [2,3,4]
# print(list(set(list_1) ^ set(list_2))) #两个列表取差集
# print(list(set(list_1).difference(set(list_2)))) #list_1中有而list_2中没有的

list_1 = ["green", "blue", "orange", "black"]
list_2 = ["green", "blue","red","purple"]

print(list(set(list_2).difference(set(list_1))))
