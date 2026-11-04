# Abstraction: Abstraction is an OOP conecpt that hides the implementation details and expose only essential functionality to user.

# example with class object
class ATM:
    def __init__(self):
        self.atmHaveMoney = False
        self.insertCard = False
        self.enterPin = False
        self.pinVerified = False
        self.balance = False

    def withdraw(self):
        self.atmHaveMoney = True
        self.insertCard = True
        self.enterPin = True
        self.pinVerified = True
        self.balance = True
        print("User withdraw money successfully!!")

# atm = ATM()
# atm.withdraw()

# example with abc module
from abc import ABC, abstractmethod

class Bike(ABC): #abtract class
    @abstractmethod #Makes a method abstract
    def start(self):
        pass #means no implementation is provided here

class Honda(Bike):
    def start(self):
        print("bike start")

obj = Honda()
obj.start()

# Note: if we want to call abstract method then you have to use super keyword with method to call it in child class
# ex: super().start()