import requests

token='API-KEY'
url = "https://login.techsmith.com/api/v2/users"
payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': f'Bearer {token}'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)