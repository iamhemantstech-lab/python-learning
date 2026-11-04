# Encapsulation: Encapsulation is an OOP conecpt that combines varibales and methods into the single unit (class) and restrict direct access to some data.

class BankAccount:
    # Note: 
    # no underscore means it is a public varibale -  access anywhere
    # single underscore means it is a protected varibale - 
    # double underscores means it is a private varibale
    # def __init__(self, balance):
    #     self.name = "Rahul"          # Public
    #     self._age = 22               # Protected
    #     self.__salary = 30000        # Private


    def __init__(self, balance):
        self.__balance = balance

    def deposite(self, amount):
        self.__balance += amount

    def getBalance(self):
        return self.__balance

bankAcc = BankAccount(10000)
bankAcc.deposite(8000)
result = bankAcc.getBalance()
# print(result)
# print("access", bankAcc._BankAccount__balance) # private varibale internally become "_BankAccount__balance" using mangled name