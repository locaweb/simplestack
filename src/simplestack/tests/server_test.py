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

from webtest import TestApp
from simplestack import server

import unittest


class ServerTest(unittest.TestCase):

    def headers(self):
        return {"x-simplestack-hypervisor-token": "YWRtaW46c2VjcmV0"}

    def test_having_any_port_configured(self):
        self.assertTrue(int(server.get_config("port")))

    def test_hypervisor_token(self):
        token = "YWRtaW46c2VjcmV0"
        username, password = server.parse_token(token)
        self.assertEqual(username, "admin")
        self.assertEqual(password, "secret")

    def test_guest_list(self):
        app = TestApp(server.app)
        response = app.get("/mock/test/guests", headers=self.headers())
        self.assertEqual(response.json, [])
