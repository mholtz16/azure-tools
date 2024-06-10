import json
import requests
from keyvault import get_secret

url = "https://login.techsmith.com/oauth/token"

print("Retrieving id and secrets from keyvault...")

client_id = get_secret('VideoReviewAuth0ClientID')
secret = get_secret('VideoReviewAuth0Secret')
audience = "https://apis.techsmith.com"

payload = {
    "client_id": client_id,
    "client_secret": secret,
    "audience": audience,
    "grant_type": "client_credentials",
    }

headers = { 'content-type': "application/json" }
print("Retrieving access token from Auth0...")
output = requests.post(url, json = payload, headers = headers).json()

print(output)
#exit()
token = output['access_token']


#tscid = input("Email tscid of customer: ")
headers = {
    'content-type': "application/json",
    'Authorization': f'Bearer {token}',
    'On-Behalf-Of': "e3225a29-cf3a-4aed-827a-fe1c1d5ec7fa",
}

uri= 'https://videoreview.techsmith.com/api/v1/reviews'

print (headers)
output = requests.get(uri, headers=headers)
print(output.reason)





