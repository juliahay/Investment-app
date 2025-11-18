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
contract_type = 'call'
expired = 'false'
order = 'asc'
limit = 1000
sort_type = 'strike_price'

final_df = pd.DataFrame()
url = "https://api.massive.com/v3/reference/options/contracts?contract_type=call&expired=false&order=asc&limit=1000&sort=ticker&apiKey=RkwOb2o8WMk16Vq_7_66LjDAcX_mXlgL"

#https://api.massive.com/v3/reference/options/contracts?cursor=YXA9JTdCJTIySUQlMjIlM0ElMjI5OTI3NTQyNDk2MTg1NzI4OTYlMjIlMkMlMjJTdGFydERhdGVVdGMlMjIlM0ElN0IlMjJUaW1lJTIyJTNBJTIyMjAyNS0wNy0xNFQwMCUzQTAwJTNBMDBaJTIyJTJDJTIyVmFsaWQlMjIlM0F0cnVlJTdEJTJDJTIyRW5kRGF0ZVV0YyUyMiUzQSU3QiUyMlRpbWUlMjIlM0ElMjIwMDAxLTAxLTAxVDAwJTNBMDAlM0EwMFolMjIlMkMlMjJWYWxpZCUyMiUzQWZhbHNlJTdEJTJDJTIydW5kZXJseWluZ190aWNrZXIlMjIlM0ElMjJBQUwlMjIlMkMlMjJ0aWNrZXIlMjIlM0ElMjJPJTNBQUFMMjYwMzIwQzAwMDIzMDAwJTIyJTJDJTIyZXhwaXJhdGlvbl9kYXRlJTIyJTNBJTIyMjAyNi0wMy0yMFQwMCUzQTAwJTNBMDBaJTIyJTJDJTIyc3RyaWtlX3ByaWNlJTIyJTNBMjMlMkMlMjJjZmklMjIlM0ElMjJPQ0FTUFMlMjIlMkMlMjJjb250cmFjdF90eXBlJTIyJTNBJTIyY2FsbCUyMiUyQyUyMmV4ZXJjaXNlX3N0eWxlJTIyJTNBJTIyYW1lcmljYW4lMjIlMkMlMjJwcmltYXJ5X2V4Y2hhbmdlJTIyJTNBJTdCJTIyU3RyaW5nJTIyJTNBJTIyQkFUTyUyMiUyQyUyMlZhbGlkJTIyJTNBdHJ1ZSU3RCUyQyUyMnNoYXJlc19wZXJfY29udHJhY3QlMjIlM0ExMDAlMkMlMjJhZGRpdGlvbmFsX3VuZGVybHlpbmdzJTIyJTNBJTIyJTVCJTVEJTIyJTdEJmFzPSZjb250cmFjdF90eXBlPWNhbGwmZXhwaXJlZD1mYWxzZSZsaW1pdD0xMDAwJm9yZGVyPWFzYyZzb3J0PXRpY2tlcg&apiKey=RkwOb2o8WMk16Vq_7_66LjDAcX_mXlgL
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

final_df.index += 1
print(final_df)

html_full = final_df.to_html()
text_file = open("data.html", "w")
text_file.write(html_full)
text_file.close()

webbrowser.open("file:///Users/jhay/Desktop/CompSci/Stock App/Tests/data_tests/data.html")
"""
r = requests.get(f"https://api.massive.com/v3/reference/options/contracts?expired=false&order=asc&limit=1000&sort=ticker&apiKey=RkwOb2o8WMk16Vq_7_66LjDAcX_mXlgL")
data = r.json()
df = pd.DataFrame(data["results"])
df.index += 1
print(df)
"""