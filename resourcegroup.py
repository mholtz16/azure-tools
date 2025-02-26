
# This is a class representing a resource group in azure.
# most azure api clients are linked to the subscription so it 
# inherits those from the parent subscription


class ResourceGroup:
    id=None
    name=None
    subscription = None
    resource_client = None
    compute_client = None
    network_client = None
    sql_mgmt_client = None
    vms=[]
    rs_vaults = []
    resources = []
    __res_grp__ = None
    iteratormax = 256

    def __init__(self,subscription, resource_group):
        self.subscription = subscription
        self.resource_client = subscription.resource_client
        self.network_client = subscription.network_client
        self.compute_client = subscription.compute_client
        self.recoverservices_client = subscription.recoverservices_client
        self.sql_mgmt_client = subscription.sql_mgmt_client
        self._res_grp__ = resource_group
        self.resources = resource_group
        self.name = resource_group.name
        self.resources=[]

    def get_vms(self):
        self.vms = []
        for vm in self.compute_client.virtual_machines.list(self.name):
            try:
                self.vms.append(vm)
                self.resources.append(vm)
            except Exception as e:
                print("append vm error",e)
        return(self.vms)
    
    def get_recoveryservices_vaults(self):
        rsvs = self.recoverservices_client.vaults.list_by_resource_group(self.name)
        for rsv in rsvs:
            self.rs_vaults.append(rsv)
            self.resources.append(rsv)

        return(self.rs_vaults)

if __name__ == "__main__":
    print("This is a library. Do not execute")
    exit()