from massive import RESTClient
import pandas as pd
from pandas import json_normalize 
import requests
import json
import webbrowser

API_KEY = 'UBHvDYupWopjarOGExaqioHxZ0eq1h1V'
client = RESTClient(api_key=API_KEY)
#stocks_client = polygon.StocksClient(API_KEY)

ticker = 'AAPL'
#base_url = 'https://api.polygon.io/v2/'
#url = ''
#data_type = ''

date = '2025-11-18'

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

final_df = pd.DataFrame()
url = "https://api.massive.com/v2/snapshot/locale/us/markets/stocks/tickers?apiKey=UBHvDYupWopjarOGExaqioHxZ0eq1h1V"
r = requests.get(url)
data = r.json()
full_df = pd.DataFrame(data["tickers"])

"""
counter = 0
while url is not None:
    print(counter)
    r = requests.get(url)
    data = r.json()
    if 'next_url' in data:
        url = data['next_url'] + f'&apiKey={API_KEY}'
        #print("next_url:", url)
    else:
        url = None
    if 'results' not in data:
        #print("No results found.")
        break
    df = pd.DataFrame(data["results"])
    #print(df)
    
    final_df = pd.concat([final_df, df], ignore_index=True)
    #print(final_df)
    counter += 1
"""
print("Grabbing ticker data...")

for row in full_df.itertuples():
    ticker = row.ticker
    url = f'https://api.massive.com/v3/reference/tickers/{ticker}?apiKey={API_KEY}'
    r = requests.get(url)
    data = r.json()
    if 'results' in data:
        ticker_df = pd.DataFrame([data["results"]])
        if 'market_cap' in ticker_df.columns and ticker_df["market_cap"][0] >= 1e11:
            final_df = pd.concat([final_df, full_df.loc[[row.Index]]], ignore_index=True)
    

print("Processing nested columns...")

for col in final_df.select_dtypes(include=['object']).columns:
    if not isinstance(final_df[col][0], str):
        for key, value in final_df[col][0].items():
            title = col + '_' + key
            final_df[title] = final_df[col].apply(lambda x: x[key])
        final_df = final_df.drop(columns=[col])
        
#final_df = final_df[final_df['marketCap'] >= 1e11]
final_df.index += 1
print(final_df)

html_full = final_df.to_html()
text_file = open("data.html", "w")
text_file.write(html_full)
text_file.close()

webbrowser.open("file:///Users/jhay/Desktop/CompSci/Stock App/Tests/data_tests/data.html")
