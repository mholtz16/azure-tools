from azure.identity import DefaultAzureCredential
from account import Account
from azure.mgmt.sql import SqlManagementClient
import pyodbc, struct
import requests
from azure.mgmt.sql.models import FirewallRule
from datetime import datetime

# This is a stab at the DB maintenance replacement. We went with a different solution that was probably simpler in the end.



my_ip = requests.get('http://mholtz.net/ip.php').text.rstrip()

credentials = DefaultAzureCredential()
ac = Account(credentials)

def get_conn(cs):
    credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    try:
        conn = pyodbc.connect(cs, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    except Exception as e:
        print(e)
        return(None)
    return conn


i=0
sub_count = len(ac.subscriptions)

sql_firewall_rule = FirewallRule(
    start_ip_address=my_ip,
    end_ip_address=my_ip
)
today = datetime.today().strftime('%Y-%m-%d')
fw_rule_name = f'mholtz_automation_{today}'


for sub in ac.subscriptions:
    i+=1
    if 'ELEKS' not in sub.name and 'dev' not in sub.name.lower():
        print(f'{sub.name} {i} of {sub_count}')
        for rg in sub.get_resource_groups():
            sql_management_client = rg.sql_mgmt_client

            servers = sql_management_client.servers.list_by_resource_group(rg.name)
            for server in servers:
                sql_management_client.firewall_rules.create_or_update(rg.name,server.name,fw_rule_name,sql_firewall_rule)
                databases = sql_management_client.databases.list_by_server(rg.name,server.name)
                for d in databases:
                    cs = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server.name}.database.windows.net,1433;Database={d.name};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
                    conn = get_conn(cs)
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute("""
                            SELECT S.name as 'Schema',
                            T.name as 'Table',
                            I.name as 'Index',
                            DDIPS.avg_fragmentation_in_percent,
                            DDIPS.page_count
                            FROM sys.dm_db_index_physical_stats (DB_ID(), NULL, NULL, NULL, NULL) AS DDIPS
                            INNER JOIN sys.tables T on T.object_id = DDIPS.object_id
                            INNER JOIN sys.schemas S on T.schema_id = S.schema_id
                            INNER JOIN sys.indexes I ON I.object_id = DDIPS.object_id
                            AND DDIPS.index_id = I.index_id
                            WHERE DDIPS.database_id = DB_ID()
                            and I.name is not null
                            AND DDIPS.avg_fragmentation_in_percent > 0
                            ORDER BY DDIPS.avg_fragmentation_in_percent desc
                                        """)
                        for row in cursor.fetchall():
                            if row[3] >= 50 and row[4]>10 and row[0]!= 'dbo':
                                print(rg.name,server.name,d.name,row)
                sql_management_client.firewall_rules.delete(rg.name,server.name,fw_rule_name)
