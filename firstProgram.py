# print("Hello, Hemant")
# print("Hello Hemant.", "How are you?")


# variables 
name="Hemant"
number = 2 + 3j
age=10
temp=23.5
is_active=True
p=None

# print("Name is: ",name, "age is: ", age)
# print(number,temp)

# data type
# print(type(name))
# print(type(number))
# print(type(age))
# print(type(temp))
# print(type(is_active))
# print(type(p))


fruits = ["Apple", "Banana", "Mango"]
colors = ("Red", "Green", "Blue")

# print(type(fruits))


user = {
    "name": "Hemant",
    "age": 25,
    "city": "Ahmedabad"
}
# print(type(user))

num = {10,10,20,20,30,40,50}
# print(type(num))

# type conversion
# implicit - Python automatically converts one data type into another when required.
a = 10
b = 5.5
result = a + b
# print("implicit:", result)


# explicit
x = int("100")       # String to Integer
y = float("10.5")    # String to Float
z = str(100)         # Integer to String
s = list((1, 2, 3))  # Tuple to List
t = set([1, 2, 2])   # List to Set
# print(x)
# print(y)
# print(z)
# print(s)
# print(t)


# comments - for single line comment use #
'''
this is 
example of
multiline comment
'''


# input from user
# userInputValue = input("Enter your name: ")
# print("userInputValue: ", userInputValue)

# userInputCityCode = input("Enter your city code: ")
# print("userInputCityCode: ", userInputCityCode, "type: ", type(userInputCityCode))

def sum(a,b):
    return a + b

result = sum(5,7)
print(result) 