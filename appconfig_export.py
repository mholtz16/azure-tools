import json
from azure.appconfiguration import AzureAppConfigurationClient
from azure.identity import DefaultAzureCredential

# One off script to export an app config.

# Azure App Configuration Endpoint (Replace with your endpoint)
APP_CONFIG_ENDPOINT = "https://tscpresent-dev.azconfig.io"

# Use Azure Identity (Managed Identity, Service Principal, etc.)
credential = DefaultAzureCredential()
client = AzureAppConfigurationClient(APP_CONFIG_ENDPOINT, credential)

def export_app_configuration():
    """Fetches all key-value pairs from Azure App Configuration and saves to a JSON file."""
    config_data = {}

    try:
        # Fetch all configuration values
        for config_setting in client.list_configuration_settings():
            config_data[config_setting.key] = config_setting.value

        # Save to JSON file
        with open("app_config_dev.json", "w", encoding="utf-8") as json_file:
            json.dump(config_data, json_file, indent=4)

        print("✅ Successfully exported App Configuration values to 'app_config_export.json'")
    except Exception as e:
        print(f"❌ Error fetching configuration: {str(e)}")

if __name__ == "__main__":
    export_app_configuration()