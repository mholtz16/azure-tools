from azure.identity import DefaultAzureCredential
from account import Account
from azure.mgmt.monitor import MonitorManagementClient
from pymongo import MongoClient
from urllib.parse import quote_plus

# This script retrieves all Azure Monitor action groups, metric alerts, 
# and scheduled query alerts from multiple subscriptions and stores them in MongoDB.

# MongoDB Connection Setup #

# Raw credentials for MongoDB (Replace with actual credentials)
username = "<youusername>"
password = "<password>"  # Special characters need encoding

# Encode username and password to ensure safe transmission in the connection string
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Construct the MongoDB connection URI
connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@mholtz-test.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"

print(connection_string)  # Print the connection string for debugging (avoid in production)

# Establish connection to MongoDB
client = MongoClient(connection_string)

# Select the database and collections
db = client["azure_alerts"]
ag = db['ActionGroups']  # Collection for Action Groups
ma = db['MetricAlerts']  # Collection for Metric Alerts
sqa = db['ScheduledQueryAlerts']  # Collection for Scheduled Query Alerts

# Helper Function #

def check_sub(sub):
    """
    Filters out unwanted subscriptions based on predefined exclusion list.
    :param sub: Subscription name as a string.
    :return: True if the subscription should be included, False otherwise.
    """
    exclude = ['Vadim', 'MSDN', 'Visual Studio', 'Dev', 'Ripley', 'MCPP', 'brevick', 'Pay-As-You-Go']
    for e in exclude:
        if e in sub:
            return False  # Exclude subscriptions that match the list
    return True  # Include all other subscriptions

# Azure Authentication #

# Authenticate using DefaultAzureCredential, which will attempt various authentication methods
credential = DefaultAzureCredential()

# Initialize the Account object to retrieve Azure subscriptions
ac = Account(credential)

# Get the total number of subscriptions
l = len(ac.subscriptions)

# Subscription Processing #

i = 0  # Counter for progress tracking
for sub in ac.subscriptions:
    i += 1
    print(sub.name, i, "of", l)  # Log current subscription being processed

    if check_sub(sub.name):  # Only process subscriptions that pass the filter
        for rg in sub.get_resource_groups():  # Iterate over resource groups in the subscription
            SUBSCRIPTION_ID = sub.subid
            RESOURCE_GROUP_NAME = rg.name

            # Initialize Azure Monitor client for the current subscription
            monitor_client = MonitorManagementClient(credential, SUBSCRIPTION_ID)

            # Fetch and Store Action Groups #
            action_groups = monitor_client.action_groups.list_by_resource_group(RESOURCE_GROUP_NAME)
            for action_group in action_groups:
                result = ag.insert_one(action_group.serialize())  # Insert into MongoDB
                print(f"Inserted Action Group ID: {result.inserted_id}")  # Log inserted document ID

            # Fetch and Store Metric Alerts #
            metric_alerts = monitor_client.metric_alerts.list_by_resource_group(RESOURCE_GROUP_NAME)
            for metric_alert in metric_alerts:
                result = ma.insert_one(metric_alert.serialize())  # Insert into MongoDB
                print(f"Inserted Metric Alert ID: {result.inserted_id}")  # Log inserted document ID

            # Fetch and Store Scheduled Query Alerts #
            scheduled_queries = monitor_client.scheduled_query_rules.list_by_resource_group(RESOURCE_GROUP_NAME)
            for scheduled_query in scheduled_queries:
                result = sqa.insert_one(scheduled_query.serialize())  # Insert into MongoDB
                print(f"Inserted Scheduled Query ID: {result.inserted_id}")  # Log inserted document ID