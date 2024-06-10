from azure.identity import DefaultAzureCredential
import json
from account import Account
from getpass import getpass
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

skip_subs = ['TSC-Captioning-Dev01','TSC-WebWWW-Dev01','TSC-Internal-Dev','TSC-CorpCloud-Dev01','TSC-WebServices-Dev']


for sub in ac.subscriptions:
    if sub.name not in skip_subs:
#        print (sub.name)
        for rg in sub.get_resource_groups():
            vms  = rg.get_vms()
            i=1
            for vm in vms:
                try:
                    if not vm.os_profile.windows_configuration:
                        print(vm.name)
                except:
                    None
