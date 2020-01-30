import requests
import random

url = 'http://127.0.0.1:8080/task'

for num in range(1000000):
    data = {'somekey': random.randint(-10000, 100000)}
    res = requests.get(url, data = data)
    print (res.text)