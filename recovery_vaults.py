from azure.identity import DefaultAzureCredential
import json
from account import Account
from azure.mgmt.recoveryservices import RecoveryServicesClient
credentials = DefaultAzureCredential()
ac = Account(credentials)

def include_sub(name):
    ignore_list = ['dev','stage','test','eleks']
    for ignore in ignore_list:
        if ignore in name.lower():
            return(False)
    return(True)


for sub in ac.subscriptions:
    if include_sub(sub.name):

        for rg in sub.get_resource_groups():
            print (rg.name)
            rsvs = rg.get_recoveryservices_vaults()
            for rsv in rsvs:
                vault = rg.recoverservices_client.vaults.get(rg.name,rsv.name)
                print(dir(vault))
                # backup_items = backup_client.backup_protected_items.list(resource_group_name='rg_xxx', vault_name=var_vault)
                exit()



