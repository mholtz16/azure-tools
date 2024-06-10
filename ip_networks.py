from azure.identity import DefaultAzureCredential
import json
from account import Account
'''

with open('creds.json','r') as c:
    creds=json.loads(c.read())


azure_creds=creds['azure']
client = azure_creds['client']
tenant = azure_creds['tenant']
secret=azure_creds['secret']['value']
'''
credentials = DefaultAzureCredential()
ac = Account(credentials)

location = input("location (eastus, eastus2, northcentralus, westus...): ")
environment = input("Environment (Dev, Stage, Live): ")



for sub in ac.subscriptions:
    for rg in sub.get_resource_groups():
        vnets = rg.network_client.virtual_networks.list(rg.name)
        for vn in vnets:
            if vn.location == location and vn.tags['Environment']==environment:
                if vn.dhcp_options:
                    print(f'{sub.name} {rg.name} {vn.name} {vn.location} {vn.dhcp_options}')
                else:
                    print(f'{sub.name} {rg.name} {vn.name} {vn.location} None')
                    None

