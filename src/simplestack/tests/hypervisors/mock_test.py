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

from simplestack.exceptions import FeatureNotImplemented
from simplestack.hypervisors import mock
from simplestack.tests.hypervisors.base_test_case import HypervisorBaseTest

import random
import unittest


class MockTest(unittest.TestCase, HypervisorBaseTest):

    @classmethod
    def setUpClass(clazz):
        clazz.stack = mock.Stack(None)
        clazz.vm_name = "TestVM:%f" % random.random()
        clazz.vm = clazz.stack.guest_create({"name": clazz.vm_name})

    @classmethod
    def tearDownClass(clazz):
        clazz.stack.__class__.guests = {}

    @classmethod
    def _stopVmClass(clazz):
        pass

    def setUp(self):
        self.stack = self.__class__.stack
        self.vm = self.__class__.vm

    def _get_vm_id(self):
        return self.vm["id"]

    def _stop_vm(self):
        self.__class__._stopVmClass()

    def _media_name(self):
        return "cd"
