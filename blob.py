from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

account_url = 'https://ACCOUNT.blob.core.windows.net'
default_credential = DefaultAzureCredential()


blob_service_client = BlobServiceClient(account_url, credential=default_credential)
container_client = blob_service_client.get_container_client("uploads")

for blob in container_client.list_blobs(name_starts_with = 'g01390040FNNh7cTvjejABoCPiAQp'):
    #print(dir(blob))
    print(blob.name)
    #exit()
#blob_list = blob_service_client.walk_blobs('/uploads/g01390040FNNh7cTvjejABoCPiAQp/')