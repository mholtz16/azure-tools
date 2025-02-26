from azure.identity import DefaultAzureCredential
import json
from account import Account
from getpass import getpass

# iterate over all the vms in the account and print out the version of windows on them.



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
                    if vm.os_profile.windows_configuration:
                        print(vm.os_profile.windows_configuration)
                except:
                    None
