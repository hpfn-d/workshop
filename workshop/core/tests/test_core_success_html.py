from django.test import TestCase
from django.shortcuts import resolve_url as r


class CoreSuccessTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('core:success'))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """ Must use index.html"""
        self.assertTemplateUsed(self.response, 'core/success.html')
