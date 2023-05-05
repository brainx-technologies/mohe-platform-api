from django.test import Client

from mohe.diagnostics.models import Category, Biomarker
from mohe.hardware.models import Model, Device
from mohe.kplex.models import Kplex, Batch, Parameter
from mohe_api.api_tests.tests.base import AuthenticatedApiTestCase


class MeasurementTestCase(AuthenticatedApiTestCase):
    def setUp(self):
        super(MeasurementTestCase, self).setUp()

        # diagnostics
        category = Category.objects.create(id=1, name='Drugs of abuse')
        marker = Biomarker.objects.create(id=1, category=category, name='Cocaine', acronym='COC')

        # kplex
        kplex = Kplex.objects.create(id=1, name='Drugs of abuse', acronym='DOA')
        batch = Batch.objects.create(id=1, kplex=kplex, barcode=1, batch_number=2, production_date='2017-11-01',
                                     expiry_date='2030-12-31')
        Parameter.objects.create(id=1, kplex=kplex, biomarker=marker, position=1)

        # hardware
        model = Model.objects.create(id=1, name='MOHE 1')
        self.device = Device.objects.create(id=1, serial_number='SN1', hardware_key='DEVICE1', model=model)

    def test_post_empty(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/measurement/measurement/')
        self.assertEqual(response.status_code, 400)

    def test_post_success(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/measurement/measurement/', {
            'title': 'Test',
            'date': '2020-11-01 07:12:23Z',
            'sync_date': '2020-11-01 08:12:23Z',
            'measurement_date': '2020-11-01 08:12:23Z',
            'result': 4369,
            'lat': 12,
            'lng': 13,
            'device': self.device.pk,
            'kplex': 1,
            'batch': 1,
        })
        self.assertEqual(response.status_code, 201)

        response = c.get('/measurement/measurement/')

        result = response.json()[0]
        self.assertEqual(result['result'], 4369)
        self.assertEqual(result['title'], 'Test')
        self.assertEqual(result['device'], self.device.pk)

    def test_post_invalid_batch(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/measurement/measurement/', {
            'title': 'Test',
            'date': '2020-11-01 07:12:23Z',
            'sync_date': '2020-11-01 08:12:23Z',
            'measurement_date': '2020-11-01 08:12:23Z',
            'result': 4369,
            'lat': 12,
            'lng': 13,
            'device': self.device.pk,
            'kplex': 1,
            'batch': 99999,
        })
        self.assertEqual(response.status_code, 400)
