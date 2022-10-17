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

def say(_error, name):
    @raise_ERROR_1(_error)
    def say_someting(name):
        print("hello", name)
        return "hello " + name
    return say_someting(name)

print(say("_error1", "shuxun"))