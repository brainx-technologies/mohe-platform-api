from django.test import Client
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK, HTTP_401_UNAUTHORIZED

from mohe.hardware.models import Model, Device
from mohe_api.api_tests.tests.base import AuthenticatedApiTestCase


class ModelTestCase(AuthenticatedApiTestCase):
    def setUp(self):
        super(ModelTestCase, self).setUp()
        # hardware
        model = Model.objects.create(id=1, name='MOHE 1', key='M1')
        self.device = Device.objects.create(id=1, serial_number='SN1', hardware_key='DEVICE1', model=model)

    def test_anonymous(self):
        c = Client()
        response = c.get('/hardware/model/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_post(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/hardware/model/', {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_get(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.get('/hardware/model/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()[0]['key'], 'M1')
        self.assertEqual(response.json()[0]['name'], 'MOHE 1')


class DeviceTestCase(AuthenticatedApiTestCase):
    def setUp(self):
        super(DeviceTestCase, self).setUp()
        # hardware
        model = Model.objects.create(id=1, name='MOHE 1', key='M1')
        self.device = Device.objects.create(id=1, serial_number='SN1', hardware_key='DEVICE1', model=model)

    def test_anonymous(self):
        c = Client()
        response = c.get('/hardware/device/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_post(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/hardware/device/', {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_get(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.get('/hardware/device/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()[0]['serial_number'], 'SN1')
        self.assertEqual(response.json()[0]['hardware_key'], 'DEVICE1')
