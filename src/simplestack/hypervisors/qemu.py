from simplestack.hypervisors.base import SimpleStack
import libvirt


class Stack(SimpleStack):

    def __init__(self, db):
        self.connection = False
        self.database = db
