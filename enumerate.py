# Enumerate: It is a built in function that allows us to loop through an iterable (such as a list, tuple or string) and get both index, value at the same time.
# Note: Start enumerate from a specific number
# By default, indexing starts from 0
# But we can change it using start

users = ["John", "Karan", "Paul"]

for index, user in enumerate(users):
    print("user", user)
    print("index", index)