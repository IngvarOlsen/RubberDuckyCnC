import requests

url = '207.127.88.215/update'
data = {'key': 'value'}
response = requests.post(url, json=data)