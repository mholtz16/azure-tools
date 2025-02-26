from azure.identity import DefaultAzureCredential
import json
from account import Account
from ipaddress import ip_network,ip_address
import csv


# takes and export of ips frim ipam and searchs for network iterfaces in azure. 
# it then checks if that IP is in azure and reports if it is not.


ips=[]
with open ('ipam.csv','r') as csvfile:
    r = csv.reader(csvfile,delimiter=',')
    for row in r:
        ips.append(row[0].split('/',1)[0])

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
        vnets = rg.network_client.virtual_networks.list(rg.name)
        for nic in sub.network_client.network_interfaces.list(rg.name):
            for ipc in nic.ip_configurations:
                if ipc.private_ip_address in ips:
                    print(f'found {nic.name} {ipc.private_ip_address} in ipam')
                else:
                    print(f'need to add {nic.name} {ipc.private_ip_address} to ipam')

#        for vn in vnets:
#            exit()
#            for sn in vn.subnets:
#                if sn.ip_configurations:
#                    for ipc in sn.ip_configurations:
#                        print(ipc.name,ipc.private_ip_address)
            # if it's not peered it doesn't really matter
            #if len(vn.virtual_network_peerings) > 0:  
            #    print(f'{rg.name} {vn.name} {vn.address_space.address_prefixes}')
            #network_interface_ip_configurations.list(rgname,nicname)

