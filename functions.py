# lambda function

# ========================================== without lambda
def cube (num):
    return num ** 3
# print(cube(3))

# ======================================== with lambda
# note: first x is parameter
lambda_cube = lambda x: x ** 3
# print(lambda_cube(3))


# ================================== function with *args ==========================
def sum_all(*args):
    print("args: ", args)
    print("*args: ", *args)
    return sum(args)

# print(sum_all(1,2,3))
# print(sum_all(1,2,3,4,5))


# ================================== function with **kw   args ==========================
def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_kwargs(name="shaktiman", power="laser")
print_kwargs(name="shaktiman")
print_kwargs(name="shaktiman", power="laser", enemy="Dr. Jackaal")


# ================================ yield =================================================
# yield is a keyword used inside a function to turn it into a generator, allowing it to produce a sequence of values one at a time instead of all at once.
# yield stores the function's state (its local variables and the exact line where it paused) in heap memory and yield immediately pauses (freezes) the function right then and there, hands you that single number, and waits!

# without yield
def given_number():
    numbers=[]
    for i in range(1,6):
        numbers.append(i)
    return numbers

# print(given_number()) # this print list

# this print number in new line
# for num in given_number():
#     print(num)

# ========================================== with yield ========================================
# In a simple way, yield hands over a single result in every iteration, clears that result from memory, and reuses the exact same memory space for the next iteration. Is this correct?
# Imagine a restaurant with only 1 table (or a fixed number of tables), and 50 people waiting outside in a line for lunch.
# Instead of buying 50 new tables to seat everyone at the same time (which is what return with a list does), the restaurant manager acts like yield: he calls one person at a time to the table. Once that person finishes eating and leaves, the manager clears the table and seats the next person in line at that exact same table.
# He never needs to arrange any extra tables, no matter if 50 people or 5,000 people are waiting outside.

def given_numbers():
    for i in range(1, 6):
        yield i # Hands you one number at a time

for num in given_numbers():
    print(num)

