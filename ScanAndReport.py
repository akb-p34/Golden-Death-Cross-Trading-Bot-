'''
author: akbar pathan
date: 1/12/2023
title: GDC strategy
'''

'''
What does it do:
- Downloads all ticker symbols for constituencies in the S&P 500, S&P 400, and the S&P 600.
- it calculates the 50 day and 200 day simple moving average for each constituency
- it calculates each time is the 50 day and 200 day simple moving average crosses each other in the past 30 days
- raw close price data of the current day and the day before will be used to calculate the average rate of change of the 50 day moving average and 200 day moving average and whichever slope is greater determines if it is a death cross or Golden Cross
- if a stock has a cross in the past 30 days then it will be recorded into a buy list or sell list depending if it's a golden or death cross
'''

# pandas is used to get the data of the ticker names for all three indexes
import pandas as pd

# datetime is used to get the current day and the date 30 days ago
from datetime import date, timedelta, datetime

# pandas_ta is used for the 50 day and 200 day simple moving average
import pandas_ta as ta

# yfinance is used to retrieve the adjusted close price, the name of the company, and the index the company is in
import yfinance as yf

# numpy is used to calculate the intersections of the 50 day and 200 day simple moving average
import numpy as np

# matplotlib is used to check data accuracy
import matplotlib.pyplot as plt


# get the ticker symbols of the stocks in the S&P 500
df500 = pd.read_csv('sp-500-index-01-12-2023.csv')["Symbol"]

# get the ticker symbols of the stocks in the S&P 400
df400 = pd.read_csv('sp-400-index-01-12-2023.csv')["Symbol"]

# get the ticker symbols of the stocks in the S&P 600
df600 = pd.read_csv('sp-600-index-01-12-2023.csv')["Symbol"]

# combine all three data frames together
df1500 = pd.concat([df500, df400, df600], ignore_index = True)


# get the current date
today = date.today().isoformat()

# get the date tomorrow
tmrw = (date.today()+timedelta(days=1)).isoformat()

# get the date 30 days ago
lastMo = (date.today()-timedelta(days=30)).isoformat()

# get the date one year ago
lastYr = (date.today()-timedelta(days=365)).isoformat()

# data collected after filtering for crosses under 31 days old to be converted to a csv file
finalData = {"Ticker":[], "Date":[], "Signal":[]}


# calculate crosses in the past 30 days
def crosses(ticker):
    # grabs close price data of the stock for 1 year
    rawClose = yf.download(ticker, start=lastYr, end=tmrw)["Close"]
    # calculates the simple moving 50 day average on the raw close price
    sma50 = rawClose.rolling(window=50).mean()
    # calculates the simple moving 200 day average on the raw close price
    sma200 = rawClose.rolling(window=200).mean()
    # finds any crosses on the 1 year graph after 200 days into that 1 year have passed
    intersections = np.argwhere(np.diff(np.sign(sma50 - sma200))).flatten()
    newIntersections = intersections[199:]
    # used to retrieve indexes of golden or death crosses
    buySignalIndex = []
    sellSignalIndex = []
    
    # categorizes each cross into a golden or death cross by comparing the slopes of the SMAs 
    for i in newIntersections:
        sma50Slope = (sma50[i+1] - sma50[i-1])/2
        sma200Slope = (sma200[i+1] - sma200[i-1])/2
        if (sma50Slope > sma200Slope):
            # Golden Cross
            buySignalIndex.append(i)
        else:
            # Death Cross
            sellSignalIndex.append(i)
    
    # adjusts the buySignalIndex to the day after to get the correct date on when to buy the stock at open
    for i in range(len(buySignalIndex)):
        buySignalIndex[i] = buySignalIndex[i] + 1
    
    # adjusts the sellSignalIndex to the day after to get the correct date on when to sell the stock at open
    for i in range(len(sellSignalIndex)):
        sellSignalIndex[i] = sellSignalIndex[i] + 1
    
    # filters and removes any buy signals that are older than 30 days, otherwise it appends data to finalData
    for i in buySignalIndex:
        # gets each part of the date into a list; splits up the YR, DAY, MO into different elements in a list
        crossDate = str(rawClose.index[i].date()).split("-")
        lastMoDate = lastMo.split("-")
        # converts all three entries in both lists to ints
        for j in range(len(crossDate)):
            crossDate[j] = int(crossDate[j])
        for j in range(len(lastMoDate)):
            lastMoDate[j] = int(lastMoDate[j])
        # variables used to compare dates
        d1 = datetime(crossDate[0], crossDate[1], crossDate[2])
        d2 = datetime(lastMoDate[0], lastMoDate[1], lastMoDate[2])
        # compares dates and removes if the Golden Cross is older than 1mo
        if(d1<d2):
            buySignalIndex.remove(i)
        else:
            finalData["Ticker"].append(ticker)
            finalData["Date"].append(str(rawClose.index[i].date()))
            finalData["Signal"].append("BUY")
    
    # filters and removes any sell signals that are older than 30 days, otherwise it appends data to finalData
    for i in sellSignalIndex:
        # gets each part of the date into a list; splits up the YR, DAY, MO into different elements in a list
        crossDate = str(rawClose.index[i].date()).split("-")
        lastMoDate = lastMo.split("-")
        # converts all three entries in both lists to ints
        for j in range(len(crossDate)):
            crossDate[j] = int(crossDate[j])
        for j in range(len(lastMoDate)):
            lastMoDate[j] = int(lastMoDate[j])
        # variables used to compare dates
        d1 = datetime(crossDate[0], crossDate[1], crossDate[2])
        d2 = datetime(lastMoDate[0], lastMoDate[1], lastMoDate[2])
        # compares dates and removes if the Golden Cross is older than 1mo
        if(d1<d2):
            sellSignalIndex.remove(i)
        else:
            finalData["Ticker"].append(ticker)
            finalData["Date"].append(str(rawClose.index[i].date()))
            finalData["Signal"].append("SELL")

# 'main' function
for i in range(len(df1500)):
    # gets the tickers of all 1505 stocks
    crosses(df1500[i])

df = pd.DataFrame(finalData)
df.to_csv("GoldenAndDeathCrosses.csv", index=False)