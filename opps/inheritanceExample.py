# Inheritance: Inheritance is an OOP concept when one class derives the properties and methods from another class
# child class inherite the properties and methods from parent class
# Types: Single inheritance, Multilevel inheritance, Multiple inheritance

# Single inheritance
# class Vehicle:
#     def start(self):
#         print("vehicle start")

#     def stop(self):
#         print("vehicle stop")
    

# class Bike(Vehicle):
#     def __init__(self, name):
#         self.name = name

# bikeObj = Bike("Honda bike")
# print(bikeObj.name)
# bikeObj.start()
# bikeObj.stop()

# Multilevel inheritance
# class Vehicle:
#     def start(self):
#         print("vehicle start")

#     def stop(self):
#         print("vehicle stop")
    

# class Bike(Vehicle):
#     def __init__(self, name):
#         self.name = name

# class Model(Bike):
#     def showModel(self):
#         print("Bike name: ", self.name)

# modelObj = Model("Honda")
# modelObj.showModel()
# modelObj.start()
# modelObj.stop()

# Multiple inheritance
class P1:
    a = "variable of class p1"

class P2:
    b = "variable of class p2"

class P3(P1,P2):
    c = "variable of class p3"

obj = P3()
print(obj.c)
print(obj.b)
print(obj.a)
