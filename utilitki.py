"""
Plik zawiera gotowy zestaw funkcji, najczęściej dekoratorów, przydatnych w codziennej pracy.
"""

# importuję potrzebne biblioteki
from functools import wraps
import time 
import functools





#from functools import wraps
#import time 

def timefn(fn):
    """Mierzy czas trwania funkcji. Można przerobić """
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print ("@timefn: " + fn.__name__ + " took " + str(t2 - t1) + " seconds")
        return result
    return measure_time


#przykład
if __name__ == "__main__":
    import random
    @timefn
    def losowa(x):
        for _ in range(x):
            a = random.random()
        return 

    losowa(10000000)


# cash dla wywołanej funkcji, stosować jeżeli wiemy że wywołania dla danego zbioru 
# argunentów będą się powtarzać 

#import functools
def memoize(func):
    """
    Cache the results of the function so it doesn't need to be called
    again, if the same arguments are provided a second time.
    """
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        # This line is for demonstration only.
        # Remove it before using it for real.
        print('Calling %s()' % func.__name__)
        result = func(*args)
        cache[args] = result
        return result
    return wrapper