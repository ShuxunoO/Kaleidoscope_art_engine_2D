# # 被修饰的函数有多个参数，但没有返回值，修饰器函数也没有参数
# def w2(fun):
#     def wrapper(*args,**kwargs):
#         print("this is the wrapper head")
#         fun(*args,**kwargs)
#         print("this is the wrapper end")
#     return wrapper

# @w2
# def hello(name,name2):
#     print("hello "+name+name2)

# hello("world ","!!!")

# #输出:
# # this is the wrapper head
# # helloworld!!!
# # this is the wrapper end



# 被修饰的函数有返回值
def w3(fun):
    def wrapper():
        print("this is the wrapper head")
        temp=fun()
        print("this is the wrapper end")
        return temp   #要把值传回去呀！！
    return wrapper

@w3
def hello():
    print("hello")
    return "test"

result=hello()
print("After the wrapper,I accept %s" %result)

#输出:
#this is the wrapper head
#hello
#this is the wrapper end
#After the wrapper,I accept test




# 修饰器有参数
def func_args(pre='xiaoqiang'):
    def w_test_log(func):
        def inner():
            print('...记录日志...visitor is %s' % pre)
            func()

        return inner

    return w_test_log


# 带有参数的修饰器能够起到在运行时，有不同的功能

# 先执行func_args('wangcai')，返回w_test_log函数的引用
# @w_test_log
# 使用@w_test_log对test_log进行修饰
@func_args('wangcai')
def test_log():
    print('this is test log')

test_log()

#输出:
#...记录日志...visitor is wangcai
# this is test log




# def w_test(func):
#     def inner(*args, **kwargs):
#         ret = func(*args, **kwargs)
#         return ret

#     return inner


# @w_test
# def test():
#     print('test called')


# @w_test
# def test1():
#     print('test1 called')
#     return 'python'


# @w_test
# def test2(a):
#     print('test2 called and value is %d ' % a)


# test()
# test1()
# test2(9)

# # 输出:
# #test called
# #test1 called
# #test2 called and value is 9