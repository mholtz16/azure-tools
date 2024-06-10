from azure.identity import DefaultAzureCredential
from account import Account
from azure.mgmt.sql import SqlManagementClient
import sys
import re
from datetime import datetime, timedelta,date

default_answer = False
if '-n' in sys.argv:
    default_answer='n'
elif '-y' in sys.argv:
    default_answer='y'

print("default: ",default_answer or "prompt")

allow = ['AllowAllWindowsAzureIps']
delete_search = ['tonyr','AndyR','mjadmin','mholtz','Allow_DC3_VPN_Endpoint','AllowTechSmithExternal_38','AllowTechSmithExternal_69','AllowTechSmithExternal_64','BrandonBatesRemote','Brandon_remote','Allow_Andrij_Remote','AllowTonyRemote','AllowSNagamangalaRemote','Alex_Home','AllowJamesFogarty_remote','AllowJPetersonRemote','AllowBrandonAdmin','AllowBrandonRemote','AllowBBatesRemote','AllowTechSmithExternal_199.254.220.0','AllowTechSmithExternal_69.167.129.0','LiquidWeb','Allow TechSmith Extlernal','ALLOWLW3VPN','query-editor-']
with open ("deny.txt",'r') as d_list:
    delete_add = d_list.readlines()

for a in delete_add:
    delete_search.append(a.rstrip())


prompt_search = ['ClientIPAddress']
delete_ips = ['199.254.220.4','69.167.144.1','64.186.48.115','199.254.220.1','38.131.224.249','64.186.48.113','216.157.192.241','69.167.128.221','69.167.128.241','209.59.157.193','69.167.129.65','69.167.144.1','67.225.254.193']
allow_ips = ['0.0.0.0','64.85.153.32','64.85.153.34','64.85.153.33','152.117.118.104','152.117.118.110','152.117.118.109','152.117.118.108','152.117.118.107','152.117.118.106','152.117.118.105']
skipped=0
age_max = 90

def delete_rule(rg,server,rule):
    print(f"deleting {sub.name} {rg.name} {server.name} {rule.name}")
    if rule.start_ip_address not in delete_ips:
        delete_ips.append(rule.start_ip_address)
    with open('fw_rule_log','a') as log:
        sql_management_client.firewall_rules.delete(rg.name,server.name,rule.name)
        log.write(f"deleting {sub.name},{rg.name},{server.name},{rule.name}\n")
        print(f"deleted {rule.name}")



def match_date(rg,server,rule):
    name= rule.name
    r = re.match('.*(([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})).*',name)
    if r:
        date = r.group(1)
        ninty = datetime.now() - timedelta(days=age_max)
        year = int(r.group(2))
        month = int(r.group(3))
        day = int(r.group(4))
        d = datetime(year,month,day)
        if ninty > d:
            print(f'more than {d} days old   ************************',name)
            delete_rule(rg,server,rule)
        else:
            print(f'skipping rule {rg.name} {server.name} {rule.name} ({rule.start_ip_address} - {rule.end_ip_address})')
        return True
    return False

def list_match(name,name_search):
    for n in name_search:
        if n in name:
            return True
        
    return False

def allow_list(name):
    for n in allow:
        if n in name:
            print(f'allow {name}')
            return True
    return False


def rename_rule(rg,server,rule):
    today = date.today()
    new_name = f'{rule.name}-{today}-renamed'
    params = {
        'name': new_name,
        'start_ip_address': rule.start_ip_address,
        'end_ip_address': rule.end_ip_address
    }
    print(params)
    sql_management_client.firewall_rules.create_or_update(rg.name,server.name,rule.name,params)




credentials = DefaultAzureCredential()
ac = Account(credentials)

sub_count = len(ac.subscriptions)
i=0
for sub in ac.subscriptions:
    i+=1
    if 'ELEKS' not in sub.name:
        print(f'{sub.name} {i} of {sub_count}')
        for rg in sub.get_resource_groups():
            sql_management_client = rg.sql_mgmt_client

            servers = sql_management_client.servers.list_by_resource_group(rg.name)
            for server in servers:
                print(server.name)
                rules =sql_management_client.firewall_rules.list_by_server(rg.name, server.name)
                try:
                    for rule in rules:
                        if allow_list(rule.name) or rule.start_ip_address in allow_ips:
                            print(f'skipping rule {rg.name} {server.name} {rule.name} ({rule.start_ip_address} - {rule.end_ip_address})')
                            continue

                        elif list_match(rule.name,delete_search):
                            print(f'matched {rule.name}')
                            delete_rule(rg,server,rule)
                        elif rule.start_ip_address in delete_ips:
                            delete_rule(rg,server,rule)

                        elif match_date(rg,server,rule):
                            print("date_found")

                        elif list_match(rule.name,prompt_search):
                            x = (default_answer or input(f'{rg.name},{server.name},{rule.name},{rule.start_ip_address} delete or rename rule? r/y/N '))
                            if x == 'y':
                                delete_rule(rg,server,rule)
                            elif x == 'r':
                                rename_rule(rg,server,rule)
                            else:
                                print(f'skipping rule {rg.name} {server.name} {rule.name} ({rule.start_ip_address} - {rule.end_ip_address})')
                                allow_ips.append(rule.start_ip_address)
                                skipped += 1

                        else:  
                            
                            x = (default_answer or input(f'{rg.name},{server.name},{rule.name},{rule.start_ip_address} delete or rename rule? r/y/N '))
                            if x == 'y':
                                delete_rule(rg,server,rule)
                            elif x == 'r':
                                rename_rule(rg,server,rule)

                            else:
                                print(f'skipping rule {rg.name} {server.name} {rule.name} ({rule.start_ip_address} - {rule.end_ip_address})')
                                allow_ips.append(rule.start_ip_address)

                                skipped += 1
                except Exception as e:
                    print("error: ",rg.name,server.name,e)


