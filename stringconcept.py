# String: A string in Python is a sequence of characters enclosed in single, double, or triple quotes. It is used to store textual data. Strings are immutable, which means we cannot modify the original string after creating it.

str1 = "This is exmaple of string.\n Please read carefully"
# print(str1)


# concate string means add or join string
s1="Hello"
s2="world"
final_string= s1 + " " + s2
# print(final_string)
# print("length of string: ", len(s1))
# print("uppercase: ", s1.upper())
# print("lowercase: ", s1.lower())
# print("capitalize: ", s2.capitalize())
# print("title: ", final_string.title())
# print("casefold: ", "HELLO".casefold())

# Indexing
# print("we can access the char using index: ", final_string[6])

# Slicing
# syntax -  string[start:end]
# start: Index from where slicing begins (included)
# end: Index where slicing stops (excluded)
# step: How many positions to skip
print("slicing: ", s1[:0])

print("find function: ", final_string.find("l"))
