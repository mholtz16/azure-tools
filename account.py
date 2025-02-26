from azure.mgmt.resource import SubscriptionClient
from azure.identity import DefaultAzureCredential
from subscription import Subscription

# The Account class represents an Azure account, containing multiple subscriptions.
# It uses the provided credentials (typically DefaultAzureCredential) to authenticate.
# The class retrieves and stores up to 256 subscriptions by default.

class Account:
    credentials = None  # Stores authentication credentials
    subscriptions = []  # List to hold Subscription objects
    sub_client = None  # Client for interacting with Azure subscriptions
    iteratormax = 256  # Maximum number of subscriptions to process

    def __init__(self, credentials):
        """
        Initializes the Account object with the given credentials.
        Retrieves subscriptions and stores them in the subscriptions list.
        """
        self.credentials = credentials
        self.sub_client = SubscriptionClient(credential=credentials)

        i = 0  # Counter to track the number of subscriptions processed
        for sub in self.sub_client.subscriptions.list():
            i += 1
            if i > self.iteratormax:
                print(f"Reached iteratormax of {self.iteratormax}")
                break  # Stop processing if the maximum number of subscriptions is reached

            try:
                # Create a Subscription object and add it to the list
                self.subscriptions.append(Subscription(self.credentials, sub.subscription_id, sub))
            except Exception as e:
                # Catch and print any exceptions that occur while processing subscriptions
                print("Account exception:", e)

    def get_sub_name(self, name):
        """
        Searches for a subscription by name and returns it if found.
        :param name: The name of the subscription to search for.
        :return: Subscription object if found, otherwise None.
        """
        for sub in self.subscriptions:
            if sub.name == name:
                return sub  # Return the subscription if the name matches
        return None  # Return None if no match is found
    
if __name__ == "__main__":
    print("This python code is a library and is not meant to be directly executed")
    exit()