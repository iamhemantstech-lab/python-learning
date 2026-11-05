# basically 2 loops are in python
# 1 while
# 2 for

# while loop
# n = int(input("Enter number:"))
# i = 1
# while i<=10:
#     print(n, "*", i, "=", n*i)
#     i += 1


list = [1,2,3,5,7,54,234,11,5,8,9,3,1,3,6,8]
tuple = (11,22,33,55,77,5454,234234,1111,55,88,99,33,11,33,66,88)
x=55

# i=0
# while i<len(list):
#     if tuple[i] == x:
#         print(x, "is present at index: ", i)
#         break
#     else:
#         print("Not available")
#     i +=1

# while i < len(list):
#     if (tuple[i] == x):
#         i += 1
#         continue
#     print(tuple[i])
#     i += 1

# j=1
# while j <= 10:
#     if (j%2 != 0):
#         j += 1
#         continue
#     print(j)
#     j +=1


# for loop
# loops are used for sequential traversal. For traversing list, string, tuples, range.
str = "hellowelcomeintothepythonlearning"
# for c in str:
#     print(c)
# idx=0
# for i in tuple:
#     if(i == x):
#         print(x, "is present at index: ", idx)
#         break
#     idx += 1



# range()
# range function return a sequance of numbers, starting from 0 (by default) and increment by 1 (by default) and stop before a specified number.

# range(start?, stop, step?)
# start - initial val to start
# step - increament by value

# for n in range(5):
#     print(n)



# pass statement
# pass is null statement that does nothing. It is a placeholder for furtur code.
# for a in range(5):
#     pass
# print("loop is end using pass statement")


# practice

# wap to print sum of n number

# n = int(input("Enter a number:"))
i=1
sum = 0
mul = 1
# while i <= n:
#     sum += i
#     i += 1
# print("sum", sum)


# for el in range(1,n,1):
#     sum += el
# print("for sum", sum)

# wap to find the factorial of first n numbers
# factorial means for 5 : 1*2*3*4*5 = 120
ind = 0
# for el in range(1,6):
#     mul *= el
# print(mul)
