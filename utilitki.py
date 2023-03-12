"""
Plik zawiera gotowy zestaw funkcji, najczęściej dekoratorów, przydatnych w codziennej pracy.
Przed każdym dekoratorem w komentarzu podane są wymagane biblioteki do zaimportowania przed uruchomieniem kodu
"""

# importuję potrzebne biblioteki
from functools import wraps
import time 
import functools
import inspect
from itertools import chain
import random
# pip install ratelimit
from ratelimit import limits
import requests


#from functools import wraps
#import time 
def timefn(fn):
    """Pomiar czasu wywołania funkcji do momentu zwrócenia przez nią wartości albo błędu"""
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
    Zapamiętuję wynik funkcji przez co nie musi byc ponownie 
    przeliczana, te same argumenty dadzą ten sam wynik.
    """
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        # Kolejne 2 linie kodu są jedynie do celów prezentacyjnych, do wykasowania w d.
        if __name__ == "__main__":
            print('Wywołanie %s()' % func.__name__)
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
    print("A za drugim razem mamy już tylko:")
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




# Dekorator ponownie wywołuje funkcję jeżeli poprzednie wywołanie zwróciło wyjątek

#import random
#import time
#from functools import wraps

def retry(num_retries, exception_to_check, sleep_time=0):
    """
    Dekorator ponownie wywołuje funkcję jeżeli poprzednie wywołanie zwróciło wyjątek.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, num_retries+1):
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    print(f"{func.__name__} raised {e.__class__.__name__}. Retrying...")
                    if i < num_retries:
                        time.sleep(sleep_time)
            # Raise the exception if the function was not successful after the specified number of retries
            raise e
        return wrapper
    return decorate

if __name__ == "__main__":
    @retry(num_retries=3, exception_to_check=TypeError, sleep_time=1)
    def random_value(a):
        value = random.randint(a)
        return value
    
    random_value()




# dodawanie jednostki do wyniku np, PLN, zł, km/h

def use_unit(unit):
    """Funkcja zwraca wartość o zadanej jednostce"""
    use_unit.ureg = pint.UnitRegistry()
    def decorator_use_unit(func):
        @functools.wraps(func)
        def wrapper_use_unit(*args, **kwargs):
            value = func(*args, **kwargs)
            return value * use_unit.ureg(unit)
        return wrapper_use_unit
    return decorator_use_unit

if __name__ == "__main__":
    @use_unit(" km/s")
    def average_speed(distance, duration):
        return distance / duration
    

# dekorator zabezpieczający przed zbyt częstum wykonaniem funkcji 
#import time
#from functools import wraps
def rate_limited(max_per_second):
    """Dekorator pauzujący zbyt częste wywołanie funkcji"""
    min_interval = 1.0 / float(max_per_second)
    def decorate(func):
        last_time_called = [0.0]
        @wraps(func)
        def rate_limited_function(*args, **kargs):
            elapsed = time.perf_counter() - last_time_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kargs)
            last_time_called[0] = time.perf_counter()
            return ret
        return rate_limited_function
    return decorate


# pip install ratelimit
#from ratelimit import limits
#import requests

if __name__ = "__main__":
    FIFTEEN_MINUTES = 900
    @limits(calls=15, period=FIFTEEN_MINUTES)
    def call_api(url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('API response: {}'.format(response.status_code))
        return response