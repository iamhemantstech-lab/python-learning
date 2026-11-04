# Polymorphism: Polymorphism is OOP concept allows the same methods or operation to behave differently depending object.
# In simple words: Same method name, but different behaviour.

# with heritance
class Animal:
    def sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def sound(self):
        print("Dog barks")

class Cat(Animal):
    def sound(self):
        print("Cat meows")

dog = Dog()
cat = Cat()
dog.sound()
cat.sound()



# without inheritance
# class Dog:
#     def sound(self):
#         print("Dog barks")

# class Cat:
#     def sound(self):
#         print("Cat meows")

# def make_sounds(animal):
#     animal.sound()

# dog = Dog()
# cat = Cat()
# make_sounds(dog)
# make_sounds(cat)