from azure.identity import DefaultAzureCredential
from account import Account
from azure.mgmt.sql import SqlManagementClient
import sys
import re
from datetime import datetime, timedelta, date

# Set default answer based on command-line arguments
# '-n' sets default to 'no', '-y' sets default to 'yes'
default_answer = False
if '-n' in sys.argv:
    default_answer = 'n'
elif '-y' in sys.argv:
    default_answer = 'y'

print("default: ", default_answer or "prompt")

# Lists of firewall rules to allow, delete, or prompt for action
allow = ['AllowAllWindowsAzureIps']
delete_search = [
    'tonyr', 'AndyR', 'mjadmin', 'mholtz', 'Allow_DC3_VPN_Endpoint',
    'AllowTechSmithExternal_38', 'AllowTechSmithExternal_69', 'AllowTechSmithExternal_64',
    'BrandonBatesRemote', 'Brandon_remote', 'Allow_Andrij_Remote',
    'AllowTonyRemote', 'AllowSNagamangalaRemote', 'Alex_Home',
    'AllowJamesFogarty_remote', 'AllowJPetersonRemote', 'AllowBrandonAdmin',
    'AllowBrandonRemote', 'AllowBBatesRemote', 'AllowTechSmithExternal_199.254.220.0',
    'AllowTechSmithExternal_69.167.129.0', 'LiquidWeb', 'Allow TechSmith Extlernal',
    'ALLOWLW3VPN', 'query-editor-'
]

# Load additional deny rules from file
deny_file = "deny.txt"
with open(deny_file, 'r') as d_list:
    delete_add = d_list.readlines()
for a in delete_add:
    delete_search.append(a.rstrip())

prompt_search = ['ClientIPAddress']
delete_ips = ['199.254.220.4', '69.167.144.1', '64.186.48.115', '199.254.220.1']  # IPs to delete
allow_ips = ['0.0.0.0', '64.85.153.32', '64.85.153.34']  # IPs to allow
skipped = 0
age_max = 90  # Max rule age in days

def delete_rule(rg, server, rule):
    """
    Deletes a firewall rule from a given server.
    Logs the deletion to a file.
    """
    print(f"deleting {sub.name} {rg.name} {server.name} {rule.name}")
    if rule.start_ip_address not in delete_ips:
        delete_ips.append(rule.start_ip_address)
    with open('fw_rule_log', 'a') as log:
        sql_management_client.firewall_rules.delete(rg.name, server.name, rule.name)
        log.write(f"deleting {sub.name},{rg.name},{server.name},{rule.name}\n")
        print(f"deleted {rule.name}")

def match_date(rg, server, rule):
    """
    Checks if a firewall rule is older than the max allowed age.
    Deletes the rule if it's older.
    """
    name = rule.name
    r = re.match(r'.*(([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})).*', name)
    if r:
        rule_date = datetime(int(r.group(2)), int(r.group(3)), int(r.group(4)))
        if datetime.now() - timedelta(days=age_max) > rule_date:
            print(f'more than {age_max} days old, deleting:', name)
            delete_rule(rg, server, rule)
        else:
            print(f'skipping rule {rg.name} {server.name} {rule.name}')
        return True
    return False

def list_match(name, name_search):
    """Checks if a given name matches any item in a search list."""
    return any(n in name for n in name_search)

def allow_list(name):
    """Checks if a rule name is in the allowed list."""
    if any(n in name for n in allow):
        print(f'allow {name}')
        return True
    return False

def rename_rule(rg, server, rule):
    """Renames a firewall rule by appending today's date."""
    today = date.today()
    new_name = f'{rule.name}-{today}-renamed'
    params = {
        'name': new_name,
        'start_ip_address': rule.start_ip_address,
        'end_ip_address': rule.end_ip_address
    }
    print(params)
    sql_management_client.firewall_rules.create_or_update(rg.name, server.name, rule.name, params)

# Authenticate with Azure
credentials = DefaultAzureCredential()
ac = Account(credentials)
sub_count = len(ac.subscriptions)

i = 0
for sub in ac.subscriptions:
    i += 1
    if 'ELEKS' not in sub.name:  # Skip certain subscriptions
        print(f'{sub.name} {i} of {sub_count}')
        for rg in sub.get_resource_groups():
            sql_management_client = rg.sql_mgmt_client
            servers = sql_management_client.servers.list_by_resource_group(rg.name)
            for server in servers:
                print(server.name)
                rules = sql_management_client.firewall_rules.list_by_server(rg.name, server.name)
                try:
                    for rule in rules:
                        if allow_list(rule.name) or rule.start_ip_address in allow_ips:
                            print(f'skipping rule {rg.name} {server.name} {rule.name}')
                            continue
                        elif list_match(rule.name, delete_search) or rule.start_ip_address in delete_ips:
                            delete_rule(rg, server, rule)
                        elif match_date(rg, server, rule):
                            print("date_found")
                        elif list_match(rule.name, prompt_search):
                            x = default_answer or input(f'{rg.name},{server.name},{rule.name} delete or rename? r/y/N ')
                            if x == 'y':
                                delete_rule(rg, server, rule)
                            elif x == 'r':
                                rename_rule(rg, server, rule)
                            else:
                                print(f'skipping rule {rg.name} {server.name} {rule.name}')
                                allow_ips.append(rule.start_ip_address)
                                skipped += 1
                        else:
                            x = default_answer or input(f'{rg.name},{server.name},{rule.name} delete or rename? r/y/N ')
                            if x == 'y':
                                delete_rule(rg, server, rule)
                            elif x == 'r':
                                rename_rule(rg, server, rule)
                            else:
                                print(f'skipping rule {rg.name} {server.name} {rule.name}')
                                allow_ips.append(rule.start_ip_address)
                                skipped += 1
                except Exception as e:
                    print("error: ", rg.name, server.name, e)
