# Sara Gong
# ITP 115, Parke, Spring 2018
# Final Project - Stock Market Game
# 01 May 2018

# File 3: Main file
# Functions: scrapeData, saveData, openData, getStartYear, getPrice, printAssets, getNetWorth, delta, printMarket,
# selectStock, chooseQuantity, trade, graph, main

from stock import *
from bank_account import *
import matplotlib.pyplot as plt
import csv
import os.path

# scrape price data the first time the user runs the program - this takes a while
# input: list of stocks
# output: list of lists with stock names and prices
def scrapeData(stockList):
    data = []
    for stock in stockList:
        list = []
        ticker = stock.getTicker()
        list.append(ticker)
        print("Please wait. Now downloading data for:", stock.getCompany())
        priceList = stock.getPriceList()
        for price in priceList:
            list.append(price)
        data.append(list)

    return data

# save scraped price data to a file
# input: list of lists with data
# output: none
def saveData(data):
    fileOut = open("YahooFinanceData.csv", "w", newline="")
    writer = csv.writer(fileOut, delimiter=",")
    for stock in data:
        writer.writerow(stock)
    fileOut.close()

# get price data from a csv file
# input: none
# output: list of lists with data
def openData():
    data = []
    fileIn = open("YahooFinanceData.csv", "r")
    reader = csv.reader(fileIn, delimiter=",")
    for row in reader:
        data.append(row)

    return data

# get start year from user
# input: none
# output: year
def getStartYear():
    while True:
        try:
            year = int(input("Start Year (between 1990 and 2008): ").strip())
            while year not in range(1990,2009):
                print("Try again.")
                year = int(input("Start Year (between 1990 and 2008): ").strip())
            break
        except ValueError:
            print("Try again.")

    return year

# Get a stock's price for the year
# Input: dictionary of stocks/prices, stock, year
# Output: price
def getPrice(dataDict, stock, year):
    i = year - 1990
    price = dataDict[stock][i]
    price = float(price)

    return price

# Print yearly accounts
# Input: bank account, list of stocks, year
# Output: none
def printAssets(Account, stockList, year):
    print("\033[4m" + "\033[1m" + "\n" + Account.getOwner() + "'s Assets on January 1st, " + str(year) + ":\033[0m")
    print(Account)
    print("\033[4mStocks:\033[0m")
    for stock in stockList:
        print(stock)

# calculate net worth of bank account and stocks owned
# input: bank account, list of stocks, dictionary of stocks/prices, year
# output: net worth (float)
def getNetWorth(Account, stockList, dataDict, year):
    worth = Account.getAmount()
    for stock in stockList:
        price = getPrice(dataDict, stock.getTicker(), year)
        quantity = stock.getQuantity()
        worth = worth + (price*quantity)
        worth = round(worth, 2)

    return worth

# arrow symbol showing change from previous year
# input: stock, dictionary with data, year
# output: symbol and color code
def delta(dataDict, stock, year):
    if year == 1990:
        return "―"
    else:
        if getPrice(dataDict,stock.getTicker(), year) > getPrice(dataDict, stock.getTicker(), year-1):
            return "\033[92m▲"
        else:
            return "\033[91m▼"

# Print market prices for the year
# Input: list of stocks, dictionary of stocks/prices, year
# Output: none
def printMarket(stockList, dataDict, year):
    print("\n\033[4m" + "\033[1m" + "Stock Market on January 1st, " + str(year) + ":\033[0m")
    for stock in stockList:
        print(str(delta(dataDict, stock, year)), stock.getCompany() + ": $" + str(getPrice(dataDict, stock.getTicker(), year)) + " per share\033[0m")

# allow user to select stock to trade
# input: list of stocks
# output: stock choice
def selectStock(stockList):
    tickers = []
    for stock in stockList:
        tickers.append(stock.getTicker())

    ticker = input("Select a stock: ").upper().strip()
    while ticker not in tickers:
        ticker = input("Enter a valid ticker: ").upper().strip()

    for stock in stockList:
        if ticker == stock.getTicker():
            choice = stock

    return choice

# allow user to choose quantity of stock to trade
# input: none
# output: quantity of stock to trade
def chooseQuantity():
    while True:
        try:
            quantity = float(input("Enter number of shares: ").strip())
            while quantity < 0:
                print("Enter a positive number.")
                quantity = float(input("Enter number of shares: ").strip())
            break
        except ValueError:
            print("Try again.")

    return quantity


# allow user to conduct trade
# inputs: bank account, stock list, dictionary of stocks/prices, year
# output: none
def trade(Account, stockList, dataDict, year):
    shouldTrade = "y"
    while shouldTrade.lower() == "y":

        buyorsell = input("\nBuy, sell, or pass to the next year? ").strip()
        while buyorsell.lower() not in ["buy", "sell", "pass"]:
            buyorsell = input("Try again: ").strip()

        if buyorsell.lower() in ["buy", "sell"]:

            if Account.isEmpty() == True and buyorsell == "buy":
                print("Sorry, you're broke! :O")

            else:
                stockChoice = selectStock(stockList)
                price = getPrice(dataDict, stockChoice.getTicker(), year)
                quantity = chooseQuantity()

                # buy
                if buyorsell.lower() == "buy":
                    while Account.getAmount() < price*quantity:
                        print("Sorry, you don't have enough money! Try again.")
                        quantity = chooseQuantity()

                    Account.spend(price*quantity)
                    stockChoice.buy(quantity)
                    print("You bought", str(quantity), "shares for $" + str(round(price*quantity, 2)),"and you have", str(stockChoice.getQuantity()),
                          "shares of", stockChoice.getCompany() + ".")
                    print("You now have $" + str(Account.getAmount()) +" in the bank.")

                # sell
                if buyorsell.lower() == "sell":
                    if stockChoice.getQuantity() == 0:
                        print("Sorry, you don't own any of that stock!")
                    else:
                        while stockChoice.getQuantity() < quantity:
                            print("Sorry, you don't own that many shares! Try again.")
                            quantity = chooseQuantity()
                        Account.earn(price*quantity)
                        stockChoice.sell(quantity)
                        print("You sold", str(quantity), "shares for $" + str(round(price*quantity, 2)), "and you have", str(stockChoice.getQuantity()),
                              "shares of", stockChoice.getCompany() + ".")
                        print("You now have $" + str(Account.getAmount()) + " in the bank.")

                shouldTrade = input("Continue trading? (y/n) ").strip()
                while shouldTrade.lower() not in ["y", "n"]:
                    shouldTrade = input("Try again: ").strip()

        else:
            shouldTrade = "n"

# graph yearly net worth
# Inputs: list of years, list of yearly net worth, investor's name
# Output: none
def graph(yearList, worthList, name):
    plt.plot(yearList,worthList, marker='o')
    plt.axis([yearList[0] - 1, yearList[0] + 12, 0, max(worthList) + 500])
    plt.gca().ticklabel_format(style="plain")
    plt.xlabel("Time (years)")
    plt.ylabel("Net Worth ($)")
    plt.title(name + "'s Net Worth")
    plt.show()

# Main
# Input: none
# Output: none
def main():
    # welcome
    print("\033[1mWelcome to Wall Street.\033[0m")
    print("You'll start out with $1000 in the bank, and you have 10 years to make it rain. Good luck!")

    # Hard code the stocks on the market
    AAPL = Stock("AAPL")
    BP = Stock("BP")
    CVX = Stock("CVX")
    FOX = Stock("FOX")
    KO = Stock("KO")
    MCD = Stock("MCD")
    PG = Stock("PG")
    TGT = Stock("TGT")
    WMT = Stock("WMT")
    XOM = Stock("XOM")
    stockList = [AAPL, BP, CVX, FOX, KO, MCD, PG, TGT, WMT, XOM]

    # if price data does not exist in a file
    if os.path.exists("YahooFinanceData.csv") == False:
        print("\nDownloading data from Yahoo Finance... This should take 5-10 minutes.")
        dataList = scrapeData(stockList)
        saveData(dataList)
        print("Data saved to YahooFinanceData.csv")
    # if price data exists in a file
    else:
        dataList = openData()

    # convert list of lists to dictionary
    dataDict = {}
    for list in dataList:
        dataDict[list[0]] = []
        for item in list[1:]:
            dataDict[list[0]].append(item)

    # game loop
    play = "y"
    while play.lower() == "y":
        name = input("\nName: ").strip().title()
        year = getStartYear()
        myBankAccount = BankAccount(name)
        yearList = []
        worthList = []

        gameRound = 1
        # loop for each year
        while gameRound <= 10:
            printMarket(stockList, dataDict, year)
            printAssets(myBankAccount, stockList, year)
            worth = getNetWorth(myBankAccount, stockList, dataDict, year)
            print("\033[4mNet Worth: $" + str(worth) + "\033[0m")

            # graph
            yearList.append(year)
            worthList.append(worth)
            if gameRound > 1:
                print("\nExit graph window to begin trading.")
                graph(yearList, worthList, name)

            trade(myBankAccount, stockList, dataDict, year)

            print("\n.....A year goes by.....")
            gameRound += 1
            year += 1

        # return final results
        worthFinal = getNetWorth(myBankAccount, stockList, dataDict, year)
        print("\nIt's January 1st,", str(year) + ", game over!")
        if worthFinal == 1000.0:
            print("\033[1mYour net worth is now $1000.00, no change. -_-\033[0m")
        elif worthFinal > 1000.0:
            print("\033[1mYour net worth is now $" + str(worthFinal), "and has increased by $" + str(round(worthFinal-1000.0,2)) +". Congratulations!!! :D\033[0m")
        else:
            print("\033[1mYour net worth is now $" + str(worthFinal), "and has decreased by $" + str(round(1000.0-worthFinal,2)) +". Better luck next time. :(\033[0m")
        worthList.append(worthFinal)
        yearList.append(year)
        print("\nExit graph window to continue.")
        graph(yearList, worthList, name)

        # play again?
        play = input("Play again? (y/n) ").strip()
        while play.lower() not in ["y", "n"]:
            play = input("Try again: ").strip()
        if play.lower() == "y":
            for stock in stockList:
                stock.resetQuantity()

    print("\n\033[1mThanks for playing!\033[0m")

main()