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

from jinja2 import Template, Environment, PackageLoader


class Stack(SimpleStack):
    """
    This module provides Qemu implementation through libvirt
    http://libvirt.org/guide/html-single/

    Most part of this module uses the libvirt code available through
    inheritance via SimpleStack class.
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
            env = Environment(loader=PackageLoader("simplestack", "."))
            template = env.get_template("templates/qemu_xml.tmpl")
            xml = template.render(guestdata)

            return self.libvirt_connection.defineXML(xml)
        except:
            raise InvalidArguments()
