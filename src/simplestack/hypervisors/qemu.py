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

import os
import libvirt

from simplestack.exceptions import InvalidArguments
from simplestack.hypervisors.base import SimpleStack
from simplestack.presenters.formatter import Formatter

from Cheetah.Template import Template

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
        self.template_path = os.path.join(os.path.dirname(__file__), '../templates/qemu_xml.tmpl')

    def libvirt_connect(self):
        return libvirt.open(self.libvirt_connection_path())

    def connect(self):
        self.libvirt_connection = self.libvirt_connect()
        self.connection = self.libvirt_connection

    def guest_create(self, guestdata):
        """
        This method creates a new guest

        guestdata should contain a dict with the following arguments:

        name, memory, image, network_name
        """

        try:
            xml = str(Template(file = self.template_path, searchList = [guestdata,]))
            return self.libvirt_connection.defineXML(xml)
        except:
            raise InvalidArguments()
