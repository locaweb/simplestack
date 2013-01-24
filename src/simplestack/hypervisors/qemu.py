# Copyright 2013 Locaweb.
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
        self.libvirt_connection = False
        self.poolinfo = poolinfo
        self.connect()

    def libvirt_connect(self):
        return (
            libvirt.open("qemu+tls://%s@%s/system?no_verify=1" % (
                self.poolinfo.get("username"),
                self.poolinfo.get("api_server")
            ))
        )

    def connect(self):
        self.libvirt_connection = self.libvirt_connect()
        self.connection = self.libvirt_connection

    # def guest_update(self, guest_id, guestdata):
    #     dom = self.connection.lookupByUUIDString(guest_id)
    #
    # def guest_delete(self, guest_id):
    #     dom = self.connection.lookupByUUIDString(guest_id)
    #
    # def media_mount(self, guest_id, media_data):
    #     dom = self.connection.lookupByUUIDString(guest_id)
    #
    # def media_info(self, guest_id):
    #     dom = self.connection.lookupByUUIDString(guest_id)
    #
    # def snapshot_create(self, guest_id, snapshot_name=None):
    #     dom = self.connection.lookupByID(guest_id)

    # http://libvirt.org/guide/html/
    # <domain type='kvm'>
    #     <name>test</name>
    #     <memory unit='KiB'>524288</memory>
    #     <os>
    #         <type arch='x86_64'>hvm</type>
    #     </os>
    # </domain>
    # virDomainSuspend || virDomainSave
    # virDomainResume || virDomainRestore
    # virDomainSetVcpus & virDomainSetMemory
    # <domainsnapshot><description>name</description></domainsnapshot>
    # snapshot.getXMLDesc
