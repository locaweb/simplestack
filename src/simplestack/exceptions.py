import json
from bottle import HTTPError, HTTPResponse


class SimpleStackError(HTTPError):
    def __init__(self, code, message):
        super(SimpleStackError, self).__init__(code, None, None, None, {"Content-Type": "application/json"})
        self.output = json.dumps({"error": self.__class__.__name__, "message": message})


class FeatureNotAvailable(SimpleStackError):
    def __init__(self):
        super(FeatureNotAvailable, self).__init__(501, "The selected hypervisor doesn't implement this feature")


class FeatureNotImplemented(SimpleStackError):
    def __init__(self):
        super(FeatureNotImplemented, self).__init__(501, "SimpleStack doesn't implement this feature for the selected hypervisor yet")


class EntityNotFound(SimpleStackError):
    def __init__(self, entity_type, entity_id):
        super(EntityNotFound, self).__init__(404, "%s:%s not found" % (entity_type, entity_id))


class HypervisorError(SimpleStackError):
    def __init__(self, hypervisor_error):
        super(HypervisorError, self).__init__(500, "Hypervisor Error: %s" % hypervisor_error)
