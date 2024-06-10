from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_secret(name) -> str:
    keyVaultName = 'tscitmanagement-live'
    KVUri = f"https://{keyVaultName}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    return(client.get_secret(name).value)
