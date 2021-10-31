import requests
url = 'https://en.wikipedia.org/wiki/Data_science'

text = requests.get(url).content.decode('utf-8')

