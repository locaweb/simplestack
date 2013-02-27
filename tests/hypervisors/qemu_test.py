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

from nose.exc import SkipTest

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
            'memory': 524288,
            'image': '/mnt/storage/images/simplestack_test_image.img',
            'network_name': 'default',
        })
        clazz.stack.guest_start(clazz.vm.UUIDString())

    @classmethod
    def tearDownClass(clazz):
        clazz.stack.guest_delete(clazz.vm.UUIDString())

    def setUp(self):
        self.stack = self.__class__.stack
        self.vm = self.__class__.vm

        # Trying to assure the running state of the vm
        if self.stack.guest_info(self._get_vm_id())["state"] == "STOPPED":
            self.stack.guest_start(self._get_vm_id())

    def _stop_vm(self):
        if self.vm.ID() < 0:
            self.stack.guest_shutdown(self._get_vm_id(), force=True)
        else:
            self.stack.guest_shutdown(self._get_vm_id() )

    def _get_vm_id(self):
        return self.vm.UUIDString()

    def _network_name(self):
        return "default"

    def _media_name(self):
        return "[] /vmimages/tools-isoimages/windows.iso"

    def test_guest_update(self):
        raise SkipTest

    def test_guest_force_reboot(self):
        raise SkipTest

    def test_guest_update(self):
        raise SkipTest

    # Implemented by base hypervisor tests
    # def test_guest_shutdown(self):
    # def test_guest_list(self):
    # def test_guest_info(self):
    # def test_guest_start(self):
    # def test_guest_resume(self):
    # def test_guest_reboot(self):
    # def test_network_interface_info(self):
    # def test_network_interface_list(self):
    # def test_pool_info(self):

    def test_disk_create(self):
        raise SkipTest

    def test_disk_info(self):
        raise SkipTest

    def test_disk_list(self):
        raise SkipTest

    def test_disk_update(self):
        raise SkipTest

    def test_tag_list(self):
        raise SkipTest

    def test_tag_delete(self):
        raise SkipTest

    def test_tag_create(self):
        raise SkipTest

    def test_storage_list(self):
        raise SkipTest

    def test_storage_info(self):
        raise SkipTest

    def test_snapshot_info(self):
        """ available on base hypervisor """
        raise SkipTest

    def test_snapshot_list(self):
        """ available on base hypervisor """
        raise SkipTest

    def test_snapshot_revert(self):
        """ available on base hypervisor """
        raise SkipTest

    def test_snapshot_delete(self):
        """ available on base hypervisor """
        raise SkipTest

    def test_snapshot_create(self):
        raise SkipTest

    def test_network_interface_update(self):
        raise SkipTest

    def test_network_interface_delete(self):
        raise SkipTest

    def test_network_interface_create(self):
        raise SkipTest

    def test_media_mount(self):
        raise SkipTest

    def test_media_unmount(self):
        raise SkipTest

    def test_host_list(self):
        raise SkipTest

    def test_host_info(self):
        raise SkipTest
