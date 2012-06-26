import unittest
import random
import ConfigParser
from simplestack.hypervisors import vmware
from simplestack.utils import vmware as vmware_utils
from simplestack.tests.hypervisors.base_test_case import HypervisorBaseTest


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
