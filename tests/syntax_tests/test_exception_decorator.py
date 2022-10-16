class My_ERROR1(Exception):
    def __init__(self, name):
        self.name  = name
    def __str__(self):
        ERROR_INFO = self.name + "is raised"
        return ERROR_INFO


def raise_ERROR_1(error_name):
    def inner(_fun):
        def wrapper(*args,**kwargs):
            try:
                raise My_ERROR1(error_name)
            except My_ERROR1 as Error:
                print (Error)
            return _fun(*args,**kwargs)
        return wrapper
    return inner

@raise_ERROR_1("错误1")
def say_someting(name):
    print("hello", name)
    return "hello " + name

result = say_someting("shuxun")

print(result)