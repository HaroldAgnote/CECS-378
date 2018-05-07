import requests

url = "https://jaydensdisciples.me"

get_keys = "/keys"

request = url + get_keys
print("Sending request: " + str(request))
response = requests.get(url + get_keys)
print(response.text)