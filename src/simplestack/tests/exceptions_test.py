import json
import unittest
from simplestack.exceptions import *


class FeatureNotAvailableTest(unittest.TestCase):

    def test_instance(self):
        exception = FeatureNotAvailable()
        output = json.loads(exception.output)
        self.assertEqual(exception.status, 501)
        self.assertEqual(output['message'], "The selected hypervisor doesn't implement this feature")
        self.assertEqual(exception.headers.get('Content-Type'), "application/json")
