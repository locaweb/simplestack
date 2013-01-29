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
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.

from simplestack.hypervisors import qemu
from tests.hypervisors.base_test_case import HypervisorBaseTest

import random
import unittest
import ConfigParser


class QemuTest(unittest.TestCase, HypervisorBaseTest):

    @classmethod
    def setUpClass(clazz):
        vm_info = """
            <domain type='kvm'>
                <name>TestVM:%f</name>
                <memory unit='KiB'>524288</memory>
                <os>
                    <type arch='x86_64'>hvm</type>
                </os>
            </domain>
        """
        conf = ConfigParser.ConfigParser()
        conf.read("etc/test.cfg")
        clazz.stack = qemu.Stack({
            "api_server": conf.get("qemu", "api_server"),
            "username": conf.get("qemu", "username")
        })

        clazz.vm = clazz.stack.connection.createXML(vm_info % random.random(), 1)

    @classmethod
    def tearDownClass(clazz):
        clazz.vm.shutdown()
        clazz.vm.destroy()

    def setUp(self):
        self.stack = self.__class__.stack
        self.vm = self.__class__.vm

    def _stop_vm(self):
        self.vm.shutdown()

    def _get_vm_id(self):
        return self.vm.ID()

    def _network_name(self):
        return "default"

    def _media_name(self):
        return "[] /vmimages/tools-isoimages/windows.iso"
