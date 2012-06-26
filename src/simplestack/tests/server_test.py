import unittest
from webtest import TestApp
from simplestack import server


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
