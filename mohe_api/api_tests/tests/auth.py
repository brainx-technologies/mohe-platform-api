from django.test import Client

from mohe_api.api_tests.tests.base import AuthenticatedApiTestCase


class AuthTestCase(AuthenticatedApiTestCase):

    def test_noauth(self):
        c = Client()
        response = c.get('/accounts/user/')
        self.assertEqual(401, response.status_code)

    def test_basic_auth(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.get('/accounts/user/')
        self.assertEqual(200, response.status_code)

    def test_token_auth(self):
        c = Client(**self.get_token_auth_headers())
        response = c.get('/accounts/user/')
        self.assertEqual(200, response.status_code)

        data = response.json()
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['email'], self.email)
