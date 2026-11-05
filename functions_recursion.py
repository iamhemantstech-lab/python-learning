def sum(a,b): # a,b are parameters
    return a + b

result = sum(2,3) # 2,3 are arguments
# print(result) 


name = ["Karan", "Rahul", "Amit", "Priya", "Neha"]

def display(list):
    for elm in list:
        print(elm, end=" ")
# display(name)
# print()


def factorial(n):
    fac =1
    for i in range(1,n+1):
        fac *= i
    return fac

# print(factorial(5))

# Recursion
# when function call itself repeatedly

def show(n):
    if(n == 0): # base case
        return
    print(n)
    show(n-1)

# show(5)

# foctoial using recursion
def fact (n):
    
    if (n == 0):
        return 1
    res  = n * fact(n-1)
    return res
    
    

# print(fact(5))

# calculate sum of first n number
# n_by_user = int(input("Enter number:"))

def sum(n):
    if(n==1 or n==0):
        return 1
    return sum(n-1) + n
# print(sum(5))


# print all elements in a list 
# hint: use list and index as paramater
myList = [2,3,1,5,4,6,7]

def showElement(list,index=0):
    if(index == len(list)):
        return
    print(list[index])
    showElement(list, index +1)

# showElement(myList)
