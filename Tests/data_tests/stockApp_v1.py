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

# FIND WAY TO HAVE DATE SET TO LAST WEEKDAY IF RUN ON WEEKEND
today = datetime.date.today()
if today.strftime('%A') == 'Saturday':
    today = today - datetime.timedelta(days=1)
elif today.strftime('%A') == 'Sunday':
    today = today - datetime.timedelta(days=2)
date = today.isoformat()

months_ago = today - relativedelta(months=3)
if months_ago.strftime('%A') == 'Saturday':
    months_ago = months_ago - datetime.timedelta(days=1)
elif months_ago.strftime('%A') == 'Sunday':
    months_ago = months_ago - datetime.timedelta(days=2)
date_3mo_ago = months_ago.isoformat()


print("Grabbing full ticker snapshot...")

final_df = pd.DataFrame()
full_snapshot = f"https://api.massive.com/v2/snapshot/locale/us/markets/stocks/tickers?apiKey={API_KEY}"
r = requests.get(full_snapshot)
data = r.json()
full_df = pd.DataFrame(data["tickers"])

print("Getting stocks that meet market cap, 3 month, and 5 day criteria...")
count = 0
for row in full_df.itertuples():
    count += 1
    ticker = row.ticker
    url_ticker = f'https://api.massive.com/v3/reference/tickers/{ticker}?apiKey={API_KEY}'
    url_3mo = f"https://api.massive.com/v1/open-close/{ticker}/{date_3mo_ago}?adjusted=true&apiKey={API_KEY}"
    r_ticker = requests.get(url_ticker)
    data_ticker = r_ticker.json()
    r_3mo = requests.get(url_3mo)
    data_3mo = r_3mo.json()
    
    if 'results' in data_ticker and data_3mo['status'] == 'OK':
        df_ticker = pd.DataFrame([data_ticker["results"]])
        df_3mo = pd.DataFrame([data_3mo])
        if 'market_cap' not in df_ticker.columns or df_ticker["market_cap"][0] < 1e11:
            continue
        
        if row.day['c'] <= df_3mo["close"][0]:
            continue
    else:
        continue
    
    df_5day = pd.DataFrame()
    i = 1
    while df_5day.shape[0] < 5:
        date_5day = datetime.date.today() - datetime.timedelta(days=i)
        if date_5day.strftime('%A') in ['Saturday', 'Sunday']:
            i += 1
            continue
        url_5day = f"https://api.massive.com/v1/open-close/{ticker}/{date_5day.isoformat()}?adjusted=true&apiKey={API_KEY}"
        r_5day = requests.get(url_5day)
        data_5day = r_5day.json()
        df_5day = pd.concat([df_5day, pd.DataFrame([data_5day])], ignore_index=True)
        i += 1
    
    if df_5day['close'].max() > row.day['c']:
        continue
   
    final_df = pd.concat([final_df, full_df.loc[[row.Index]]], ignore_index=True)
    
        
    
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