from azure.identity import DefaultAzureCredential
import json
from account import Account
from getpass import getpass

credentials = DefaultAzureCredential()
ac = Account(credentials)


# Iterate over all the attached disks in an account and output a csv
# subscription,resource_group, diskname, diskstate
#skip_subs = ['TSC-Captioning-Dev01','TSC-WebWWW-Dev01','TSC-Internal-Dev','TSC-CorpCloud-Dev01','TSC-WebServices-Dev']
skip_subs = []
print('subscription,resource group,disk,status')
for sub in ac.subscriptions:
    if sub.name not in skip_subs:
#        print (sub.name)
        for rg in sub.get_resource_groups():
            disks   = rg.compute_client.disks.list_by_resource_group(rg.name)
            i=1
            for disk in disks:
                if disk.disk_state != 'Attached':
                    print(f'{sub.name},{rg.name},{disk.name},{disk.disk_state}')