from polygon import RESTClient
import pandas as pd
from pandas import json_normalize 
import requests
import json

API_KEY = 'RkwOb2o8WMk16Vq_7_66LjDAcX_mXlgL'
client = RESTClient(api_key=API_KEY)
#stocks_client = polygon.StocksClient(API_KEY)

ticker = 'AAPL'
#base_url = 'https://api.polygon.io/v2/'
#url = ''
#data_type = ''

date = '2025-10-23'

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
limit = 100
sort_type = 'strike_price'

r = requests.get(f"https://api.polygon.io/v3/reference/options/contracts?underlying_ticker={ticker}&contract_type={contract_type}&expired={expired}&order={order}&limit={limit}&sort={sort_type}&apiKey={API_KEY}")
data = r.json()
df = pd.DataFrame(data["results"])
df.index += 1
print(df)