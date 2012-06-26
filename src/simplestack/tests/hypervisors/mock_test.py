import unittest
import random
from simplestack.exceptions import FeatureNotImplemented
from simplestack.hypervisors import mock
from simplestack.tests.hypervisors.base_test_case import HypervisorBaseTest


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

    def _get_nw_interface_id(self):
        return "0"

    def _stop_vm(self):
        self.__class__._stopVmClass()

    def _media_name(self):
        return "cd"
