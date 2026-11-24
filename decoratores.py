import time

def cache(func):
    cached_values = {}
    def wrapper(*args):
        if args in cached_values:
            return cached_values[args]
        result = func(*args)
        cached_values[args] = result

        return result 
    return wrapper

@cache
def calculate_sum(a,b):
    time.sleep(2)
    return a + b

# here cache is our custom decorator cache will execute before the calculate_sum execution

print("sum of 5 and 15:*** Original ", calculate_sum(55,15))
print("sum of 5 and 15: ", calculate_sum(5,15))
print("sum of 10 and 15: Original ", calculate_sum(10,15))
print("sum of 5 and 15: ", calculate_sum(5,15))
print("sum of 20 and 15: Original ", calculate_sum(20,15))
print("sum of 5 and 15: ", calculate_sum(5,15))
print("sum of 10 and 15: ", calculate_sum(10,15))
print("sum of 20 and 15: ", calculate_sum(20,15))




