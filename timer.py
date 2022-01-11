import time

def timeit(func):
    def wrapper(*args,**kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - t0) * 1000
        name = func.__name__

        print(f"{name} with args: {args} and kwargs: {kwargs} returned value: {result} in: {duration} milliseconds")

        return(result)
    return wrapper

if __name__ == "__main__":
    @timeit
    def return_nums(a, b, c):
        j = 0
        for i in range(1000000):
            j += i

        return(a,b,c)



    print(return_nums(1,2,c=3))