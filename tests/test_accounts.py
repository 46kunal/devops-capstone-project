"""Account API tests compatible with nosetests and pytest."""

import os
import tempfile
import unittest

from service.app import create_app


class AccountTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=os.getcwd())
        app = create_app({"TESTING": True, "DATABASE": os.path.join(self.directory.name, "test.db"),
                          "API_TOKEN": "test-token"})
        self.client = app.test_client()
        self.headers = {"Authorization": "Bearer test-token"}

    def tearDown(self):
        self.directory.cleanup()

    def test_health_and_auth(self):
        self.assertEqual(self.client.get("/health").json, {"status": "ok"})
        self.assertEqual(self.client.get("/").json["service"], "Customer Accounts")
        self.assertEqual(self.client.get("/accounts").status_code, 401)

    def test_security_headers_and_cors(self):
        response = self.client.get("/accounts", headers={**self.headers, "Origin": "http://localhost:3000"})
        self.assertEqual(response.headers["Access-Control-Allow-Origin"], "http://localhost:3000")
        self.assertIn("Content-Security-Policy", response.headers)
        denied = self.client.get("/accounts", headers={**self.headers, "Origin": "https://untrusted.example"})
        self.assertNotIn("Access-Control-Allow-Origin", denied.headers)

    def test_account_lifecycle(self):
        response = self.client.post("/accounts", json={"name": "Ada", "email": "Ada@Example.com"}, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        account_id = response.json["id"]
        self.assertEqual(response.json["email"], "ada@example.com")
        self.assertEqual(len(self.client.get("/accounts", headers=self.headers).json), 1)
        self.assertEqual(self.client.get(f"/accounts/{account_id}", headers=self.headers).json["name"], "Ada")
        response = self.client.put(f"/accounts/{account_id}", json={"balance": 10.5, "active": False},
                                   headers=self.headers)
        self.assertEqual(response.json["balance"], 10.5)
        self.assertFalse(response.json["active"])
        self.assertEqual(self.client.delete(f"/accounts/{account_id}", headers=self.headers).status_code, 204)
        self.assertEqual(self.client.get(f"/accounts/{account_id}", headers=self.headers).status_code, 404)

    def test_validation_and_duplicate(self):
        self.assertEqual(self.client.post("/accounts", json={}, headers=self.headers).status_code, 400)
        payload = {"name": "Ada", "email": "ada@example.com"}
        self.assertEqual(self.client.post("/accounts", json=payload, headers=self.headers).status_code, 201)
        self.assertEqual(self.client.post("/accounts", json=payload, headers=self.headers).status_code, 409)
        self.assertEqual(self.client.put("/accounts/1", json={"balance": -1},
                                         headers=self.headers).status_code, 400)
