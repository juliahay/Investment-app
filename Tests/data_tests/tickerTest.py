#! /usr/bin/python3

from polygon import RESTClient
import pandas as pd
from pandas import json_normalize 
import requests
import json

API_KEY = 'bsmdfKwVkC45Nke9ayRlSq7bpdRR95yJ'
client = RESTClient(api_key=API_KEY)
client = RESTClient(api_key=API_KEY, trace=True, verbose=True)
#stocks_client = polygon.StocksClient(API_KEY)

#ticker = 'AAPL'
#base_url = 'https://api.polygon.io/v2/'
#url = ''
#data_type = ''

date = '2025-10-28'

#echo curl l -X GET "https://api.massive.com/v3/reference/tickers?market=stocks&active=true&order=asc&limit=100&sort=ticker&apiKey=API_KEY"
tickers = []
for t in client.list_tickers(market="crypto", date=date, limit=1000):
    print (t)
    tickers.append(t)
print(tickers)


