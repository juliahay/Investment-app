#! /usr/bin/python3

from massive import RESTClient
import pandas as pd
from pandas import json_normalize 
import requests
import json
import time

API_KEY = 'bsmdfKwVkC45Nke9ayRlSq7bpdRR95yJ'
client = RESTClient(api_key=API_KEY)
#stocks_client = polygon.StocksClient(API_KEY)

ticker = 'TQQQ'
#base_url = 'https://api.polygon.io/v2/'
#url = ''
#data_type = ''

date = '2025-11-10'

""" 
df = pd.DataFrame(client.list_options_contracts(
	underlying_ticker=ticker,
    contract_type="call",
	expired="false",
	order="asc",
	limit=100,
	))

print(df)
"""
contract_type = 'call'
expired = 'false'
order = 'asc'
limit = 1000
sort_type = 'strike_price'

final_df = pd.DataFrame()
url = "https://api.massive.com/v3/reference/options/contracts?underlying_ticker=" + ticker + "&contract_type=call&expired=false&order=asc&limit=1000&sort=ticker&apiKey=" + API_KEY

counter = 0

while url is not None and counter < 5:
    print(counter)
    r = requests.get(url)
    data = r.json()
    if 'next_url' in data:
        url = data['next_url'] + f'&apiKey={API_KEY}'
        time.sleep(20)
    else:
        url = None
    if 'results' not in data:
        print("No results found.")
        break
    df = pd.DataFrame(data["results"])
    #print(df)
    
    final_df = pd.concat([final_df, df], ignore_index=True)
    #print(final_df)
    counter += 1

final_df.index += 1
print(final_df)
"""
r = requests.get(f"https://api.massive.com/v3/reference/options/contracts?expired=false&order=asc&limit=1000&sort=ticker&apiKey=RkwOb2o8WMk16Vq_7_66LjDAcX_mXlgL")
data = r.json()
df = pd.DataFrame(data["results"])
df.index += 1
print(df)
"""
