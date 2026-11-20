import requests

url =  "https://www.elprisetjustnu.se/api/v1/prices/2026/11-19_SE3.json"
response = requests.get(url)
data = response.json()
print(data[0])



