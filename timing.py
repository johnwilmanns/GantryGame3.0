import time

def timeit(func):
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        func(*args, **kwargs)
        td = time.perf_counter()-t0
        print(f"{func.__name__} took {td} seconds to run")

    return wrapper