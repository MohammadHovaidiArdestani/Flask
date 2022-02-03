import requests
resp = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
data = resp.json()
currency = "GBP"
current_price = data["bpi"][currency]["rate_float"]
amount = 1
total = current_price*amount
print(f"{amount} BTC will cost {total} {currency}")