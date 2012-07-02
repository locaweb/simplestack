# Copyright 2012 Locaweb.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# @author: Francisco Freire, Locaweb.
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.

from simplestack.hypervisors.base import SimpleStack

import libvirt


class Stack(SimpleStack):

    state_translation = {
        libvirt.VIR_DOMAIN_RUNNING: "STARTED",
        libvirt.VIR_DOMAIN_SHUTOFF: "STOPPED",
        libvirt.VIR_DOMAIN_PAUSED: "PAUSED"
    }

    def __init__(self, poolinfo):
        self.connection = False
        self.poolinfo = poolinfo
        self.connect()

    def connect(self):
        self.connection = libvirt.open("qemu+tls://%s@%s/system?no_verify=1" % (
            self.poolinfo.get("username"),
            self.poolinfo.get("api_server")
        ))

    def guest_list(self):
        return [
            self._vm_info(self.connection.lookupByID(vm_id))
            for vm_id in self.connection.listDomainsID()
        ]

    def guest_info(self, guest_id):
        dom = self.connection.lookupByUUIDString(guest_id)
        return self._vm_info(dom)

    def guest_shutdown(self, guest_id, force=False):
        dom = self.connection.lookupByUUIDString(guest_id)
        if force:
            return dom.destroy()
        else:
            return dom.shutdown()

    # def guest_start(self, guest_id):
    #     dom = self.connection.lookupByUUIDString(guest_id)

    def guest_reboot(self, guest_id, force=False):
        dom = self.connection.lookupByUUIDString(guest_id)
        if force:
            return vm.reset(0)
        else:
            return vm.reboot(0)

    def guest_suspend(self, guest_id):
        dom = self.connection.lookupByUUIDString(guest_id)
        return dom.suspend()

    def guest_resume(self, guest_id):
        dom = self.connection.lookupByUUIDString(guest_id)
        return dom.resume()

    # def guest_update(self, guest_id, guestdata):
    #     dom = self.connection.lookupByUUIDString(guest_id)
    #
    # def guest_delete(self, guest_id):
    #     dom = self.connection.lookupByUUIDString(guest_id)

    def snapshot_list(self, guest_id):
        dom = self.connection.lookupByID(guest_id)
        snaps = [self._snapshot_info(s) for s in dom.snapshotListNames()]
        return snaps


    # http://libvirt.org/guide/html/
    # virDomainCreate # connection.create("<domain type='kvm'><name>test</name><memory unit='KiB'>524288</memory><os><type arch='x86_64'>hvm</type></os></domain>", 0)
    # virDomainDestroy # force => true
    # virDomainShutdown # force => false
    # virDomainSuspend || virDomainSave
    # virDomainResume || virDomainRestore
    # virDomainReboot # force => false
    # virDomainReset # force => true
    # virDomainSetVcpus & virDomainSetMemory
    # dom.RevertToSnapshot(snapshot, 0)
    # snapshot.delete(0)
    # dom.createXML("<domainsnapshot><description>name</description></domainsnapshot>", 0)
    # snapshot.getXMLDesc

    def _vm_info(dom):
        infos = dom.info()
        return {
            'id': dom.UUIDString(),
            'name': dom.name(),
            'cpus': infos[3],
            'memory': infos[1] / 1024,
            'hdd': None,
            'tools_up_to_date': None,
            'state': self.state_translation[infos[0]],
        }

    def _snapshot_info(self, snapshot):
        return {
            'id': snapshot.get_description(),
            'name': snapshot.name(),
            'state': snapshot.get_state(),
            'path': snapshot.get_path(),
            'created': snapshot.get_create_time()
        }
