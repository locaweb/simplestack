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
# @author: Thiago Morello (morellon), Locaweb.
# @author: Willian Molinari (PotHix), Locaweb.

from simplestack.hypervisors import vmware
from simplestack.utils import vmware as vmware_utils
from simplestack.tests.hypervisors.base_test_case import HypervisorBaseTest

import random
import unittest
import ConfigParser


class VMwareTest(unittest.TestCase, HypervisorBaseTest):

    @classmethod
    def setUpClass(clazz):
        conf = ConfigParser.ConfigParser()
        conf.read("test.cfg")
        clazz.stack = vmware.Stack({"api_server": conf.get("vmware", "api_server"), "username": conf.get("vmware", "username"), "password": conf.get("vmware", "password")})
        clazz.vm = clazz.stack.connection.get_vm_by_name("clone").clone("TestVM:%f" % random.random())

    @classmethod
    def tearDownClass(clazz):
        clazz._stopVmClass()
        clazz.stack.guest_delete(clazz.vm.properties.config.uuid)

    @classmethod
    def _stopVmClass(clazz):
        try:
            clazz.vm.power_on()
        except:
            pass
        try:
            clazz.vm.power_off()
        except:
            pass

    def setUp(self):
        self.stack = self.__class__.stack
        self.vm = self.__class__.vm
        try:
            self.vm.power_on()
        except:
            pass

    def _get_vm_id(self):
        return self.vm.properties.config.uuid

    def _stop_vm(self):
        self.__class__._stopVmClass()

    def _media_name(self):
        return "[] /vmimages/tools-isoimages/windows.iso"
