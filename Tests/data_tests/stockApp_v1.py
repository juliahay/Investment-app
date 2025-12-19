from massive import RESTClient
import pandas as pd
from pandas import json_normalize 
import requests
import json
import webbrowser
import datetime
from dateutil.relativedelta import relativedelta

API_KEY = 'UBHvDYupWopjarOGExaqioHxZ0eq1h1V'
client = RESTClient(api_key=API_KEY)

date = datetime.date.today().isoformat()
date_3mo_ago = (datetime.date.today() - relativedelta(months=3)).isoformat()
date_5day = (datetime.date.today() - datetime.timedelta(days=5)).isoformat()

print("Grabbing full ticker snapshot...")

final_df = pd.DataFrame()
full_snapshot = f"https://api.massive.com/v2/snapshot/locale/us/markets/stocks/tickers?apiKey={API_KEY}"
r = requests.get(full_snapshot)
data = r.json()
full_df = pd.DataFrame(data["tickers"])

print("Getting stocks that meet market cap, 3 month, and 5 day criteria...")
count = 0
for row in full_df.itertuples():
    ticker = row.ticker
    url_ticker = f'https://api.massive.com/v3/reference/tickers/{ticker}?apiKey={API_KEY}'
    url_3mo = f"https://api.massive.com/v1/open-close/{ticker}/{date_3mo_ago}?adjusted=true&apiKey={API_KEY}"
    url_5day = f"https://api.massive.com/v2/aggs/ticker/{ticker}/range/1/day/{date_5day}/{date}?adjusted=true&sort=asc&limit=120&apiKey=UBHvDYupWopjarOGExaqioHxZ0eq1h1V" #this may not be one call!
    r_ticker = requests.get(url_ticker)
    data_ticker = r_ticker.json()
    r_3mo = requests.get(url_3mo)
    data_3mo = r_3mo.json()
    r_5day = requests.get(url_5day)
    data_5day = r_5day.json()
    

    passed_mc = False
    passed_3mo = False
    passed_5day = True #NOT PUT IN YET
    if 'results' in data_ticker and data_3mo['status'] == 'OK' and 'results' in data_5day:
        df_ticker = pd.DataFrame([data_ticker["results"]])
        df_3mo = pd.DataFrame([data_3mo])
        df_5day = pd.DataFrame([data_5day["results"]])
        if 'market_cap' in df_ticker.columns and df_ticker["market_cap"][0] >= 1e11:
            passed_mc = True
        
        #NOT WORKING YET
        print(full_df.loc[[row.Index]]['day'][0]['c'])
        print(df_3mo["close"][0])
        if full_df.loc[[row.Index]]['day'][0]['c'] > df_3mo["close"][0]:
            passed_3mo = True
        

    if passed_mc and passed_3mo and passed_5day:
        print(count)
        final_df = pd.concat([final_df, full_df.loc[[row.Index]]], ignore_index=True)
    count += 1
    
"""
print("Processing nested columns...")

for col in final_df.select_dtypes(include=['object']).columns:
    if not isinstance(final_df[col][0], str):
        for key, value in final_df[col][0].items():
            title = col + '_' + key
            final_df[title] = final_df[col].apply(lambda x: x[key])
        final_df = final_df.drop(columns=[col])
"""



final_df.index += 1
print(final_df)