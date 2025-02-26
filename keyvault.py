from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_secret(name,keyVaultName) -> str:
    KVUri = f"https://{keyVaultName}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    return(client.get_secret(name).value)


if __name__ == '__main__':
    print("this is a library. Please don't execute it directly")
    exit()
