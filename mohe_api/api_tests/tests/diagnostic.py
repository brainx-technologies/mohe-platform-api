from django.test import Client
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_200_OK, HTTP_401_UNAUTHORIZED

from mohe.diagnostics.models import Category, Biomarker
from mohe_api.api_tests.tests.base import AuthenticatedApiTestCase


class CategoryTestCase(AuthenticatedApiTestCase):
    def setUp(self):
        super(CategoryTestCase, self).setUp()
        Category.objects.create(id=1, name='Drugs of abuse')
        Biomarker.objects.create(id=1, category_id=1, name='Cocaine', acronym='COC')

    def test_anonymous(self):
        c = Client()
        response = c.get('/diagnostics/category/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_get(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.get('/diagnostics/category/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()[0]['name'], 'Drugs of abuse')

    def test_post(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/diagnostics/category/', {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)


class BiomarkerTestCase(AuthenticatedApiTestCase):
    def setUp(self):
        super(BiomarkerTestCase, self).setUp()
        Category.objects.create(id=1, name='Drugs of abuse')
        Biomarker.objects.create(id=1, category_id=1, name='Cocaine', acronym='COC')

    def test_anonymous(self):
        c = Client()
        response = c.get('/diagnostics/biomarker/')
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_get(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.get('/diagnostics/biomarker/')
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()[0]['name'], 'Cocaine')

    def test_post(self):
        c = Client(**self.get_basic_auth_headers())
        response = c.post('/diagnostics/biomarker/', {})
        self.assertEqual(response.status_code, HTTP_405_METHOD_NOT_ALLOWED)
