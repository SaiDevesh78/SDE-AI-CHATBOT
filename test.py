
import requests

response = requests.get("https://emailvalidation.abstractapi.com/v1/?api_key=d67756b2438440449ef53733fe9fea9f&email=saidevesh2009@gmail.com")
print(response.status_code)
print(response.content)