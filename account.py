
from azure.mgmt.resource import SubscriptionClient
from azure.identity import DefaultAzureCredential
from subscription import Subscription


class Account:
    credentials = None
    subscriptions = []
    sub_client = None
    iteratormax = 256
    def __init__(self,credentials):
        self.credentials = credentials
        self.sub_client = SubscriptionClient(credential=credentials)
        i=0
        for sub in self.sub_client.subscriptions.list():
            i+=1
            if i > self.iteratormax:
                break
            try:
                self.subscriptions.append(Subscription(self.credentials,sub.subscription_id,sub))
            except Exception as e:
                print("account exception",e)
    
    def get_sub_name(self,name):
        for sub in self.subscriptions:
            if sub.name == name:
                return sub
        return None
        
