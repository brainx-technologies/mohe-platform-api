from django.test import Client
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK, HTTP_401_UNAUTHORIZED

from mohe.diagnostics.models import Category, Biomarker
from mohe.kplex.models import Parameter, Batch, Kplex
from mohe_api.api_tests.tests.base import AuthenticatedApiTestCase


class MplexTestCase(AuthenticatedApiTestCase):
    def setUp(self):
        super(MplexTestCase, self).setUp()

        # diagnostics
        category = Category.objects.create(id=1, name='Drugs of abuse')
        marker = Biomarker.objects.create(id=1, category=category, name='Cocaine', acronym='COC')

        # kplex
        kplex = Kplex.objects.create(id=1, name='mPlex Drugs of abuse', acronym='DOA')
        batch = Batch.objects.create(id=1, kplex=kplex, barcode=1, batch_number=2, production_date='2017-11-01',
                                     expiry_date='2030-12-31')
        Parameter.objects.create(id=1, kplex=kplex, biomarker=marker, position=1)

    def test_anonymous(self):
        c = Client()
        response = c.get('/kplex/kplex/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_post(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/kplex/kplex/', {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_get(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.get('/kplex/kplex/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()[0]['name'], 'mPlex Drugs of abuse')


class ParameterTestCase(AuthenticatedApiTestCase):
    def setUp(self):
        super(ParameterTestCase, self).setUp()

        # diagnostics
        category = Category.objects.create(id=1, name='Drugs of abuse')
        marker = Biomarker.objects.create(id=1, category=category, name='Cocaine', acronym='COC')

        # kplex
        kplex = Kplex.objects.create(id=1, name='mPlex Drugs of abuse', acronym='DOA')
        batch = Batch.objects.create(id=1, kplex=kplex, barcode=1, batch_number=2, production_date='2017-11-01',
                                     expiry_date='2030-12-31')
        Parameter.objects.create(id=1, kplex=kplex, biomarker=marker, position=1)

    def test_anonymous(self):
        c = Client()
        response = c.get('/kplex/parameter/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_post(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/kplex/parameter/', {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_get(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.get('/kplex/parameter/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()[0]['kplex'], 1)
        self.assertEqual(response.json()[0]['biomarker'], 1)



class BatchTestCase(AuthenticatedApiTestCase):
    def setUp(self):
        super(BatchTestCase, self).setUp()

        # diagnostics
        category = Category.objects.create(id=1, name='Drugs of abuse')
        marker = Biomarker.objects.create(id=1, category=category, name='Cocaine', acronym='COC')

        # kplex
        kplex = Kplex.objects.create(id=1, name='mPlex Drugs of abuse', acronym='DOA')
        batch = Batch.objects.create(id=1, kplex=kplex, barcode=1, batch_number=2, production_date='2017-11-01',
                                     expiry_date='2030-12-31')
        Parameter.objects.create(id=1, kplex=kplex, biomarker=marker, position=1)

    def test_anonymous(self):
        c = Client()
        response = c.get('/kplex/batch/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_post(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/kplex/batch/', {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_get(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.get('/kplex/batch/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()[0]['kplex'], 1)
        self.assertEqual(response.json()[0]['barcode'], 1)
        self.assertEqual(response.json()[0]['batch_number'], 2)
