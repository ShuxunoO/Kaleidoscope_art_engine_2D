def fun1(a, b, c, d):
    print(a)
    print(b)
    print(c)
    print(d)

def fun2():
    a = 1
    b = 2
    c = 3
    d = 4
    args = (a, b, c, d)
    fun1(*args)

fun2()