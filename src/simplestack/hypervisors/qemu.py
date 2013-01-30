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

import libvirt

from simplestack.hypervisors.base import SimpleStack
from simplestack.presenters.formatter import Formatter


class Stack(SimpleStack):
    """
    This module provides Qemu implementation through libvirt
    http://libvirt.org/guide/html-single/
    """

    state_translation = {
        libvirt.VIR_DOMAIN_PAUSED:  "PAUSED",
        libvirt.VIR_DOMAIN_RUNNING: "STARTED",
        libvirt.VIR_DOMAIN_SHUTOFF: "STOPPED"
    }

    def __init__(self, poolinfo):
        self.connection = False
        self.libvirt_connection = False
        self.poolinfo = poolinfo
        self.format_for = Formatter()

        self.connect()

        self.guest_xml = """
            <domain type='kvm'>
                <name>%(name)s</name>
                <memory unit='KiB'>%(memory)s</memory>
                <os>
                    <type arch='x86_64'>hvm</type>
                </os>
            </domain>
        """

    def libvirt_connect(self):
        # FIXME: Use qemu+tls instead of tcp
        return (
            libvirt.open("qemu+tcp://%s@%s/system?no_verify=1" % (
                self.poolinfo.get("username"),
                self.poolinfo.get("api_server")
            ))
        )

    def connect(self):
        self.libvirt_connection = self.libvirt_connect()
        self.connection = self.libvirt_connection

    def guest_create(self, guestdata):
        """
        This method creates a new guest

        guestdata should contain the following arguments:
        {'name': 'vm name', 'memory': 524288}
        """

        return self.libvirt_connection.createXML(self.guest_xml % guestdata, 0)
