
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.recoveryservices import RecoveryServicesClient
from azure.mgmt.sql import SqlManagementClient

# This is the real work horse of the classes for iterating over azure.  The account class just has a list of these.
# The resource groups just use the subscription clients and data for most things.


from resourcegroup import ResourceGroup

class Subscription:
    id=None
    name=None
    resource_client = None
    compute_client = None
    network_client = None
    recoveryservice_client = None
    sql_mgmt_client = None
    __sub__ = None
    credentials = None
    iteratormax = 256
    resource_groups = []


    def __init__(self,credentials,subscription_id,sub_object):

        self.resource_client = ResourceManagementClient( credential=credentials,subscription_id = subscription_id)
        self.network_client = NetworkManagementClient(credential=credentials,subscription_id=subscription_id)
        self.compute_client = ComputeManagementClient(credential=credentials, subscription_id=subscription_id)
        self.recoverservices_client = RecoveryServicesClient(credential=credentials,subscription_id=subscription_id)
        self.sql_mgmt_client = SqlManagementClient(credential=credentials,subscription_id=subscription_id)
        __sub__ = sub_object
        self.id=sub_object.id
        self.subid = sub_object.id.split('/')[2]
        self.credentials = credentials
        self.name=sub_object.display_name
    
    def get_resource_groups(self):
        i=0

        self.resource_groups=[]
        for rg in self.resource_client.resource_groups.list():
            i+=1
            if i > self.iteratormax:
                break

            try:
                self.resource_groups.append(ResourceGroup(self,rg))
            except Exception as e:
                print("resource group append exception", e)
        return(self.resource_groups)
    
if __name__ == "__main__":
    print("This is a library. Do not execute")
    exit()
