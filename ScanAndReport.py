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
from datetime import date, timedelta

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


# calculate crosses in the past 30 days
def crosses(ticker):
    rawClose = yf.download(ticker, start=lastYr, end=today)["Close"]
    sma50 = rawClose.rolling(window=50).mean()
    sma200 = rawClose.rolling(window=200).mean()

    intersections = np.argwhere(np.diff(np.sign(sma50 - sma200))).flatten()
    newIntersections = intersections[199:]
    
    buySignalIndex = []
    sellSignalIndex = []

    for i in newIntersections:
        sma50Slope = (sma50[i+1] - sma50[i-1])/2
        sma200Slope = (sma200[i+1] - sma200[i-1])/2
        if (sma50Slope > sma200Slope):
            # Golden Cross
            buySignalIndex.append(i)
        else:
            # Death Cross
            sellSignalIndex.append(i)

    plt.plot(rawClose)
    plt.plot(sma200)
    plt.plot(sma50)
    plt.ylabel('Raw Close Price (in $)')
    plt.xlabel('Date')
    plt.xticks(rotation = 45)
    plt.title(ticker + " Raw Close, 50 day SMA, & 200 day SMA")
    plt.legend(["Adj Close", "200D MA", "50D MA"], loc="upper left")
    plt.show()


    

'''
# 'main' function
for i in range(len(df1500)):
    # gets the tickers of all 1505 stocks
    crosses(df1500[i])
'''

crosses("NKE")