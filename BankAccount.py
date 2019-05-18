# Sara Gong
# ITP 115, Parke, Spring 2018
# Final Project - Stock Market Game
# 01 May 2018

# File 2: Define the BankAccount class

# Attributes: owner, amount
# Methods: constructor, getOwner, getAmount, spend, earn, isEmpty, str
class BankAccount(object):
    # define attributes for the class
    def __init__(self, owner):
        self.__owner = owner.title()
        self.__amount = 1000.00

    # return owner
    # input: none
    # output: none
    def getOwner(self):
        return self.__owner

    # return amount
    # input: none
    # output: none
    def getAmount(self):
        return round(self.__amount, 2)

    # increase amount
    # input: amount to decrease by
    # output: none
    def spend(self, amount):
        self.__amount = self.__amount - float(amount)

    # decrease amount
    # input: amount to increase by
    # output: none
    def earn(self, amount):
        self.__amount = self.__amount + float(amount)

    # checks if account is empty
    # input: none
    # output: boolean
    def isEmpty(self):
        if self.getAmount() > 0:
            return False
        else:
            return True

    # return a summary of the bank account
    # input: none
    # output: message with owner's name and the amount in the bank account
    def __str__(self):
        msg = "\033[4mBank Account: $" + str(self.getAmount()) + "\033[0m"
        return msg