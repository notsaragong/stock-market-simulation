# Sara Gong
# ITP 115, Parke, Spring 2018
# Final Project - Stock Market Game
# 01 May 2018

# File 1: Define the Stock class

from bs4 import BeautifulSoup
import urllib.request

# Attributes: ticker, quantity
# Methods: constructor, getTicker, getQuantity, resetQuantity, buy, sell, getCompany, getPriceList, str
class Stock(object):
    def __init__(self, ticker):
        self.__ticker = ticker.upper()
        self.__quantity = 0.0

    # return ticker
    # input: none
    # output: none
    def getTicker(self):
        return self.__ticker

    # return quantity
    # input: none
    # output: none
    def getQuantity(self):
        return self.__quantity

    # reset quantity
    # input: none
    # output: none
    def resetQuantity(self):
        self.__quantity = 0

    # increase quantity
    # input: quantity to increase by
    # output: none
    def buy(self, quantity):
        self.__quantity = self.__quantity + float(quantity)

    # decrease quantity
    # input: quantity to decrease by
    # output: none
    def sell(self, quantity):
        self.__quantity = self.__quantity - float(quantity)

    # return company name
    # input: none
    # output: company name
    def getCompany(self):
        try:
            url = "https://finance.yahoo.com/quote/" + self.__ticker + "/"
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page.read(), "html.parser")

            company = soup.select('h1')[0].text
            company = str(company)
            return company
        except:
            print("Yahoo Finance can't find that stock.")

    # This function returns a list of yearly prices of the stock, starting from the entered startYear
    # input: none
    # output: list of prices for the stock
    def getPriceList(self):
        priceList = []
        # Scrape prices between 1990 - present from Yahoo Finance
        year = 1990
        while year <= 2018:
            if year == 1990:
                period1 = "631180800"
                period2 = "631699200"
            elif year == 1991:
                period1 = "662716800"
                period2 = "663235200"
            elif year == 1992:
                period1 = "694252800"
                period2 = "694425600"
            elif year == 1993:
                period1 = "725875200"
                period2 = "726134400"
            elif year == 1994:
                period1 = "757411200"
                period2 = "757929600"
            elif year == 1995:
                period1 = "788947200"
                period2 = "789465600"
            elif year == 1996:
                period1 = "820483200"
                period2 = "821001600"
            elif year == 1997:
                period1 = "852105600"
                period2 = "852624000"
            elif year == 1998:
                period1 = "883641600"
                period2 = "884073600"
            elif year == 1999:
                period1 = "915177600"
                period2 = "915696000"
            elif year == 2000:
                period1 = "946713600"
                period2 = "947232000"
            elif year == 2001:
                period1 = "978336000"
                period2 = "978854400"
            elif year == 2002:
                period1 = "1009872000"
                period2 = "1010390400"
            elif year == 2003:
                period1 = "1041408000"
                period2 = "1041926400"
            elif year == 2004:
                period1 = "1072944000"
                period2 = "1073462400"
            elif year == 2005:
                period1 = "1104566400"
                period2 = "1105084800"
            elif year == 2006:
                period1 = "1136102400"
                period2 = "1136620800"
            elif year == 2007:
                period1 = "1167638400"
                period2 = "1168156800"
            elif year == 2008:
                period1 = "1199174400"
                period2 = "1199692800"
            elif year == 2009:
                period1 = "1230796800"
                period2 = "1231315200"
            elif year == 2010:
                period1 = "1262332800"
                period2 = "1262851200"
            elif year == 2011:
                period1 = "1293868800"
                period2 = "1294387200"
            elif year == 2012:
                period1 = "1325404800"
                period2 = "1325923200"
            elif year == 2013:
                period1 = "1357027200"
                period2 = "1357545600"
            elif year == 2014:
                period1 = "1388563200"
                period2 = "1389081600"
            elif year == 2015:
                period1 = "1420099200"
                period2 = "1420617600"
            elif year == 2016:
                period1 = "1451635200"
                period2 = "1452153600"
            else:
                period1 = "1483257600"
                period2 = "1483776000"

            url ="https://finance.yahoo.com/quote/"+self.__ticker+"/history?"+\
                 "period1="+period1+"&period2="+period2+"&interval=1wk&filter=history&frequency=1wk"
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page.read(), "html.parser")

            table = soup.find('table', class_="W(100%) M(0)")
            row = table.find_all('td')[1]
            price = row.span.string
            price = float(price)
            priceList.append(price)

            year += 1

        return priceList

    # input: none
    # output: "Company Name: Quantity of Stock"
    def __str__(self):
        msg = "\t" + str(self.getCompany()) + ": " + str(self.getQuantity()) + " share(s)"
        return msg
