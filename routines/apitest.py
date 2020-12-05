import yfinance as yf
import pandas as pd
import json
import uuid

from dbconnector import get_DBConnection

msft = yf.Ticker("MSFT")

# get stock info
#print(msft.info)
#dictator = msft.info

# get historical market data
dictator = msft.history(period="max")

print(dictator.info)


#df = pd.DataFrame(msft.history(period="max"))

#print(df.describe)

#print(msft.history(period="max"))

#print(msft.actions)

#data = yf.download("SPY AAPL", start="1900-01-01", end="2017-04-30")

#print(data.describe)