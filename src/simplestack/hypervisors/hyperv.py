from simplestack.hypervisors.base import SimpleStack
import libvirt


class Stack(SimpleStack):

    def __init__(self, hostinfo):
        self.connection = False
        self.hostinfo = hostinfo
        self.connect()

    def connect(self):
        ''' Connection to hypervisor '''
        open_flags = 0
        valid_auth_options = [libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_NOECHOPROMPT]
        authcb = None
        authcb_data = None

        uri = "hyperv://%s@%s/?transport=http" % (self.hostinfo.get("username"), self.hostinfo.get("api_server"))
        self.connection = libvirt.openAuth(uri, [valid_auth_options, authcb, authcb_data], open_flags)
        return

    def host_info(self):
        ''' Return information of hostname as a Dict '''
        return self.connection.getInfo()

    def guest_list(self):
        ''' Return guests running on hostname '''
        return [self.connection.lookupByID(id).name() for id in self.connection.listDomainsID()]

    def guest_info(self, guestname):
        ''' Return information of guestname as a Dict '''
        vm = self.connection.lookupByName(guestname)
        info = {
            'name': vm.name(),
            'info': vm.info(),
            'state': vm.state(0),
        }
        return info
