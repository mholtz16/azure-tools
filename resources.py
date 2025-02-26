# this is the beginnings of a set of resource classes
# There isn't much here.


from resourcegroup import ResourceGroup

class Resource:
    id=None
    name=None
    resource_group = None
    __resource__ = None
    type = None
    iteratormax = 256

    def __init__(self,resource_group: ResourceGroup,resource):
        self.__resource__ = resource
        self.resource_group = resource_group
        self.id = resource.id
        self.name = resource.name
        self.type = resource.type

class ComputeResource(Resource):
    location = None
    zone = None

    def __init__(self, resource_group,resource):
        super().__init__(self,resource_group,resource)
        self.location=resource.location
        self.zone=resource.zone



class NetworkResource(Resource):
    location = None
    zone = None

    def __init__(self, resource_group,resource):
        super().__init__(self,resource_group,resource)
        self.location=resource.location
        self.zone=resource.zone



