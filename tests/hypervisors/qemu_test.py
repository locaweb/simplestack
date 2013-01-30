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
        conf = ConfigParser.ConfigParser()
        conf.read("etc/test.cfg")
        clazz.stack = qemu.Stack({
            "api_server": conf.get("qemu", "api_server"),
            "username": conf.get("qemu", "username")
        })

        clazz.vm = clazz.stack.guest_create({
            'name':  'SimplestackTestVM:%f' % random.random(),
            'memory': 524288
        })

    @classmethod
    def tearDownClass(clazz):
        clazz.vm.shutdown()
        clazz.vm.destroy()

    def setUp(self):
        self.stack = self.__class__.stack
        self.vm = self.__class__.vm

    def _stop_vm(self):
        if self.vm.ID() < 0:
            self.vm.destroy()
        else:
            self.vm.shutdown()

    def _get_vm_id(self):
        return self.vm.UUID()

    def _network_name(self):
        return "default"

    def _media_name(self):
        return "[] /vmimages/tools-isoimages/windows.iso"

    def test_guest_update(self):
        pass

    def test_guest_suspend(self):
        pass

    def test_guest_start(self):
        pass

    def test_guest_resume(self):
        pass

    def test_guest_info(self):
        pass

    def test_guest_force_reboot(self):
        pass

    def test_guest_update(self):
        pass

    def test_guest_shutdown(self):
        pass

    def test_disk_create(self):
        pass

    def test_disk_info(self):
        pass

    def test_disk_list(self):
        pass

    def test_disk_update(self):
        pass

    def test_tag_list(self):
        pass

    def test_tag_delete(self):
        pass

    def test_tag_create(self):
        pass

    def test_storage_list(self):
        pass

    def test_storage_info(self):
        pass

    def test_snapshot_info(self):
        pass

    def test_snapshot_list(self):
        pass

    def test_snapshot_revert(self):
        pass

    def test_snapshot_delete(self):
        pass

    def test_snapshot_create(self):
        pass

    def test_pool_info(self):
        pass

    def test_network_interface_update(self):
        pass

    def test_network_interface_info(self):
        pass

    def test_network_interface_delete(self):
        pass

    def test_network_interface_create(self):
        pass

    def test_network_interface_list(self):
        pass

    def test_network_interface_create(self):
        pass

    def test_media_mount(self):
        pass

    def test_media_unmount(self):
        pass

    def test_host_list(self):
        pass

    def test_host_info(self):
        pass
