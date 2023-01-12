'''
author: akbar pathan
date: 1/12/2023
title: GDC strategy
'''

'''
What does it do:
- Downloads all ticker symbols for constituencies in the S&P 500, S&P 400, and the SNP 600.
- it calculates the 50 day and 200 day simple moving average for each constituency
- it calculates each time is the 50 day and 200 day simple moving average crosses each other in the past 30 days
- raw close price data of the current day and the day before will be used to calculate the average rate of change of the 50 day moving average and 200 day moving average and whichever slope is greater determines if it is a death cross or Golden Cross
- if a stock has a cross in the past 30 days then it will be recorded into a buy list or sell list depending if it's a golden or death cross
'''

