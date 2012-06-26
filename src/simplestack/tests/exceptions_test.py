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

from simplestack.exceptions import *

import json
import unittest


class FeatureNotAvailableTest(unittest.TestCase):

    def test_instance(self):
        exception = FeatureNotAvailable()
        output = json.loads(exception.output)
        self.assertEqual(exception.status, 501)
        self.assertEqual(output['message'], "The selected hypervisor doesn't implement this feature")
        self.assertEqual(exception.headers.get('Content-Type'), "application/json")
