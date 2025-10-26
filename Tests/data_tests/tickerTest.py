#! /usr/bin/python3

from polygon import RESTClient
import pandas as pd
from pandas import json_normalize 
import requests
import json

API_KEY = 'bsmdfKwVkC45Nke9ayRlSq7bpdRR95yJ'
client = RESTClient(api_key=API_KEY)
#stocks_client = polygon.StocksClient(API_KEY)

#ticker = 'AAPL'
#base_url = 'https://api.polygon.io/v2/'
#url = ''
#data_type = ''

date = '2025-10-24'

tickers = []
for t in client.list_tickers(market="stocks", active=True, limit=1000):
    tickers.append(t)
print(tickers)


