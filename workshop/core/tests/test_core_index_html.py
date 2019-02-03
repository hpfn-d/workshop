from django.http import HttpResponse
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.test.utils import ContextList


class CoreIndexTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('core:index'))

    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """ Must use index.html"""
        self.assertTemplateUsed(self.response, 'core/index.html')

    def test_csrf(self):
        """ Html must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_subscription_form(self):
        expected = (
            '<form',
            '<label',
            'type="email"',
            'type="submit"',
        )
        with self.subTest():
            for e in expected:
                self.assertContains(self.response, e, 1)

    def test_resp_is_httpresponse_instance(self):
        """ resp_is_httpresponse_instance """
        self.assertTrue(isinstance(self.response, HttpResponse))

    def test_resp_instance_context(self):
        """ sefl.resp has context attr"""
        self.assertTrue(hasattr(self.response, 'context'))

    def test_context_type(self):
        """ context is ContextList instance """
        self.assertIsInstance(self.response.context, ContextList)

