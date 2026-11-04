# List = list is built in data type that store the values
# list is mutable means we can modify it
# list store the multiple type of element like str, int ex. myList=[10,2,"hello",5,"world", 9.8]

myList=[10,2,"hello",5,"world", 9.8]
myList[2] = "Hi"
myList.append("python") # add one element at the end
myList.insert(3, "user") # insert element at index
# print(myList)

# list=[4,6,21,3,5,7,4,3]
# print(list.sort())
# print(list.sort(reverse=True))

# list.remove(3) # MIMP - removes first occurrence of element

# list.pop() # MIMP -  removes last element at index if not pass any index

# list.clear() # -  removes all elements
# print(list)



# Tuple = tuple is built in data type to store values
# tuple is immutable means we can not change it
myTuple = (3,5,2,1,5,7,0)

# print(myTuple[1])
# print(myTuple.index(5))
# print(myTuple.count(5))

# Note= Always use "," while creating tuple with single element other wise python will consider it as a int
invalid_tuple = (1)
valid_tuple = (1,)
# print(type(invalid_tuple))
# print(type(valid_tuple))


# wap to ask the user to enter names of three fav movies and store them into list
moviesList = []
# m = input("Enter fav movies name 1:")
# moviesList.append(m)
# m = input("Enter fav movies name 2:")
# moviesList.append(m)
# m = input("Enter fav movies name 3:")
# moviesList.append(m)

# print('movielist: ', moviesList)





# wap to check if a list contains a palindrome of elements (hint: use copy() method)
palStr = ["m","a","m",]
shallow_copy = palStr.copy()  # copy create a shallow copy of list
shallow_copy.reverse()

print(palStr,  shallow_copy)

if(palStr == shallow_copy):
    print("palindrom")
else:
    print("not palindrom")

