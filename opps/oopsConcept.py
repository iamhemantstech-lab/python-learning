class User:
    def __init__(self, name, city):
        self.userName = name
        self.city = city

    def introduce(self):
        return f"My name is {self.userName} and I am living in {self.city}"

# userObj = User("Hemant", "Surat")
# print(userObj.introduce())


class Animal(User):

    def eat(self):
        print("Animal is eating")


class Dog(Animal):

    def bark(self):
        print("Dog is barking")


dog = Dog("Hemant", "Surat")

# dog.eat()   # Inherited from Animal
# dog.bark()  # Defined in Dog
# res = dog.introduce()  
# print(res)
        

# class and constructor and static method

class Student:

    @staticmethod # this decorator where method doesn't accept self parameter
    def greet():
        print("Hello student")

    def __init__(self, name, marks):
        self.name = name
        self.marks = marks
        print("constructor called: ", name)

    def get_avg(self):
        sum = 0
        for mark in self.marks:
            sum += mark
        return sum/len(self.marks)

# student = Student("Kapor",[50,55,60])
# student.greet()
# avg=student.get_avg()
# print("avg", avg)

# Abstraction, Encapsulation, Inheritance, Polymorphisam ----- very important

# Abstraction

class Bike:

    def __init__(self):
        self.brk = False
        self.clutch = False
        self.gear = False

    def start(self):
        self.brk = True
        self.clutch = True
        self.gear = True
        print("bike start")

bike = Bike()
bike.start()