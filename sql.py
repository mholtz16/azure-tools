import os
import pyodbc, struct
from azure import identity

# this just executes a query and prints out the results.

tscid = input("Enter TSC ID: ")

connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]



def get_conn():
    credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn

conn = get_conn()
cursor = conn.cursor()
cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    print(row)

