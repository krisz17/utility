"""
Plik zawiera gotowy zestaw funkcji, najczęściej dekoratorów, przydatnych w codziennej pracy.
"""

# importuję potrzebne biblioteki
from functools import wraps
import time 
import functools
import inspect
from itertools import chain




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

# przykładowe wywołanie
if __name__ == "__main__":
    @memoize
    def silnia(n):
        if n==1:
            return 1
        return n*silnia(n-1)
    
    print(silnia(5))
    print("a za drugim razem mamy już tylko:")
    print(silnia(6))


# Sprawdzanie poprawności typów argumentów funkcji 
#import inspect
#import functools
#from itertools import chain

def typesafe(func):
    """
    Verify that the function is called with the right argument types and
    that it returns a value of the right type, according to its annotations
    """
    spec = inspect.getfullargspec(func)
    annotations = spec.annotations
    for name, annotation in annotations.items():
        if not isinstance(annotation, type):
            raise TypeError("The annotation for '%s' is not a type." % name)
        error = "Wrong type for %s: expected %s, got %s."
        defaults = spec.defaults or ()
        defaults_zip = zip(spec.args[-len(defaults):], defaults)
        kwonlydefaults = spec.kwonlydefaults or {}
        for name, value in chain(defaults_zip, kwonlydefaults.items()):
            if name in annotations and not isinstance(value, annotations[name]):
                raise TypeError(error % ('default value of %s' % name,
                                        annotations[name].__name__,
                                        type(value).__name__))
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Populate a dictionary of explicit arguments passed positionally
        explicit_args = dict(zip(spec.args, args))
        keyword_args = kwargs.copy()
        # Add all explicit arguments passed by keyword
        for name in chain(spec.args, spec.kwonlyargs):
            if name in kwargs:
                explicit_args[name] = keyword_args.pop(name)
        # Deal with explicit arguments
        for name, arg in explicit_args.items():
            if name in annotations and not isinstance(arg, annotations[name]):
                raise TypeError(error % (name,
                                        annotations[name].__name__,
                                        type(arg).__name__))
        # Deal with variable positional arguments
        if spec.varargs and spec.varargs in annotations:
            annotation = annotations[spec.varargs]
            for i, arg in enumerate(args[len(spec.args):]):
                if not isinstance(arg, annotation):
                    raise TypeError(error % ('variable argument %s' % (i + 1),
                                            annotation.__name__,
                                            type(arg).__name__))
        # Deal with variable keyword arguments
        if spec.varkw and spec.varkw in annotations:
            annotation = annotations[spec.varkw]
            for name, arg in keyword_args.items():
                if not isinstance(arg, annotation):
                    raise TypeError(error % (name,
                                            annotation.__name__,
                                            type(arg).__name__))
        r = func(*args, **kwargs)
        if 'return' in annotations and not isinstance(r, annotations['return']):
            raise TypeError(error % ('the return value',
                                    annotations['return'].__name__,
                                    type(r).__name__))
        return r
    return wrapper

# przykładowe wywołanie które pownny wskazać błędy w wywołaniu obu funkcji
if __name__ == "__main__"
    @typesafe
    def prepend_rows(rows:list, prefix:str) -> list:
        return [prefix + row for row in rows]

    aa = prepend_rows(rows=['112', 'tre'], prefix = 123) 


