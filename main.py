import pandas as pd
import numpy as np
import xlsxwriter
import math
import requests

tickers = pd.read_csv("C://Users/paduz/PycharmProjects/algotrading_test/sp_500_stocks.csv")
portfolio = float(input("How big is your portfolio?"))

from secrets import IEX_CLOUD_API_TOKEN

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

groups =list(chunks(tickers["Ticker"],100))
strings = []

for i in range(0,len(groups)):
    strings.append(",".join(groups[i]))
df = pd.DataFrame(columns=["Symbol", "Price", "MCap", "Shares"])
for str in strings:
    batch_api = f"https://sandbox.iexapis.com/stable/stock/market/batch?symbols={str}&types=quote&token={IEX_CLOUD_API_TOKEN}"
    data = requests.get(batch_api).json()
    for symbol in str.split(","):
        df = df.append(pd.Series([symbol,data[symbol]["quote"]["latestPrice"],data[symbol]["quote"]["marketCap"],"N/A"],index=["Symbol", "Price", "MCap", "Shares"]),ignore_index=True)



size = portfolio/(len(df.index))
for i in range(0,len(df.index)):
    df.loc[i,"Shares"] = math.floor(size/df.loc[i,"Price"])


writer = pd.ExcelWriter('Sp500_Screener.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1',index=False)
writer.save()


















