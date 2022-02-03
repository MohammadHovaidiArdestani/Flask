import requests
resp = requests.get('https://api.themotivate365.com/stoic-quote')
if resp.status_code == 200:
    data = resp.json()
    author = data['data']['author']
    quote = data['data']['quote']
    print(f'author of the quote: {author}')
    print(f'quote: {quote}')
else:
    print(f'ops... something bad happened. status code: {resp.status_code}')