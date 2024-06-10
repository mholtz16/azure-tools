from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient
from azure.data.tables import TableClient

credential = DefaultAzureCredential()
service = TableServiceClient(endpoint="https://tscscreencastdev.table.core.windows.net/", credential=credential)
for table in service.list_tables():
    print(table.name)
    table = TableClient(endpoint="https://tscscreencastdev.table.core.windows.net/", credential=credential,table_name=table.name)
    for ent in table.list_entities():
        print(dir(ent))
        exit()



exit()
