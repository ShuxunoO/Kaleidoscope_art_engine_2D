import time

def time_recorder(_fun):
    def wrapper(*args):
        time1 = time.time()
        counter = _fun(*args)
        time2 = time.time()
        print("程序用时："+ str(time2 - time1))
        return counter
    return wrapper

def is_prime(num):
    if num < 2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2, num):
            if num % i == 0:
                return False
        return True

print(is_prime(6))

@time_recorder
def show_all_primes(num):
    counter = 0
    for i in range(2 , num):
        if  is_prime(i):
            print(i)
            counter += 1
    return counter

print(show_all_primes(10000))

