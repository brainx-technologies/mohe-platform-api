import base64

from django.test import TestCase
from rest_framework.authtoken.models import Token

from mohe.patient.models import Patient


class AuthenticatedApiTestCase(TestCase):

    def setUp(self):
        self.email = 'test@mondialab.org'
        self.password = 'test password'

        patient, created = Patient.objects.get_or_create(id=1, defaults=dict(
            email=self.email, is_active=True
        ))
        if created:
            patient.set_password(self.password)
            patient.save()

        self.token, _ = Token.objects.get_or_create(user=patient)
        self.token.save()

    def get_token_auth_headers(self):
        return {
            'HTTP_AUTHORIZATION': 'Token {0}'.format(self.token.key),
        }

    def get_basic_auth_headers(self):
        return {
            'HTTP_AUTHORIZATION': 'Basic {0}'.format(
                base64.b64encode(f'{self.email}:{self.password}'.encode()).decode())
        }
