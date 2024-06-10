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





for sub in ac.subscriptions:
    for rg in sub.get_resource_groups():
        print (rg.name)
        vnets = rg.network_client.virtual_networks.list(rg.name)
        i=1
        print(f'\t{rg.name}')
        for vn in vnets:
            j=1
            if i>256:
                break
            if vn.dhcp_options:
                if j>256:
                    break
                print(f'\t\t{sub.name} {rg.name} {vn.name}\n')
                for server in vn.dhcp_options.dns_servers:
                    print("\t\t\t",server)

