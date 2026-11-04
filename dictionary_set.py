# Note: Dictionary and set is important data structure

# Dictionary: It is used to store data values in key-value pairs
# It is unordered, mutable and don't allow duplicate keys

dict = {
    "name":"Jack",
    "country":"India",
    "mobile_no":9632587410,
    "subject_list": ["py","js","java"],
    "marks_tuple": (60,30,50),
    "sub_dict": {
        "gender":"male",
        "occupation":"scientist"
    }
}
dict["name"] = "Joel"
dict["email"] = "temp@mail.com"
# print(dict.items())
# print(dict["sub_dict"])
# print(dict["sub_dict"]["gender"])
# print(dict)


# Set: Set is the collection of unordered items.
# removed duplicates items mustbe unique
# each element in the set is a immutable - we can not change the value of element in set
# set is mutable - we can add, remove element in set

collection = {3,4,8,1,3,2,8}
empty_set = set() # create a empty set
collection.add(10)
collection.add((11,13))
collection.remove(8) # remove specific element
collection.pop() # remove random value
# print(collection)


# task
# store following word meanings in python dictonary
# table: "a piece of furniture","list of  facts"
# cat: "a small animal"



