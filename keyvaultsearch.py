from azure.identity import DefaultAzureCredential  # Provides authentication using managed identity or other credentials
from account import Account  # Custom class to manage Azure account and subscriptions
from azure.mgmt.keyvault import KeyVaultManagementClient  # SDK for managing Key Vault resources
from azure.keyvault.secrets import SecretClient  # SDK for interacting with secrets stored in Key Vault

def check_sub(sub):
    """
    Filters out unwanted subscriptions based on a predefined exclusion list.
    :param sub: Subscription name as a string.
    :return: True if the subscription should be included, False otherwise.
    """
    exclude = ['Vadim', 'MSDN', 'Visual Studio', 'Dev', 'Ripley', 'MCPP', 'brevick', 'Pay-As-You-Go']
    for e in exclude:
        if e in sub:
            return False  # Exclude any subscription that matches an entry in the list
    return True  # Allow all other subscriptions

# Authenticate using Azure Default Credentials (supports managed identity, environment variables, etc.)
credential = DefaultAzureCredential()

# Create an account object that retrieves available subscriptions
ac = Account(credential)

i = 0  # Counter to track processed subscriptions
l = len(ac.subscriptions)  # Get total number of subscriptions

# Iterate through all subscriptions linked to the account
for sub in ac.subscriptions:
    i += 1  # Increment counter
    print(sub.name, i, "of", l)  # Print subscription name and progress

    # Check if the subscription should be processed
    if check_sub(sub.name):
        try:
            # Iterate through all resource groups in the subscription
            for rg in sub.get_resource_groups():
                SUBSCRIPTION_ID = sub.subid  # Subscription ID
                RESOURCE_GROUP_NAME = rg.name  # Resource group name

                # Create a Key Vault management client to interact with Key Vault resources
                kv_mgmt_client = KeyVaultManagementClient(credential, SUBSCRIPTION_ID)

                # List all Key Vaults in the given resource group
                key_vaults = kv_mgmt_client.vaults.list_by_resource_group(RESOURCE_GROUP_NAME)

                for vault in key_vaults:
                    # Access the secrets stored in the Key Vault
                    secret_client = SecretClient(vault_url=vault.properties.vault_uri, credential=credential)

                    # Retrieve metadata about secrets (but not their values yet)
                    secrets = secret_client.list_properties_of_secrets()

                    # Define a list of search strings to look for in secret values
                    searchstrings = ['tsc-assets-mgmt-stage-ai']

                    try:
                        # Iterate through the secrets found in the Key Vault
                        for secret in secrets:
                            # Retrieve the actual secret value
                            value = secret_client.get_secret(secret.name).value

                            # Check if any of the search strings appear in the secret value
                            for v in searchstrings:
                                if v in value:
                                    print("HERE *********************************************************", vault.name, secret, value)

                    except Exception as e:
                        # Ignore errors that may occur while retrieving secrets
                        pass  

        except Exception as e:
            # Print any exceptions encountered while processing the subscription
            print(e)