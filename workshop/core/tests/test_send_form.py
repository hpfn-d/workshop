from unittest.mock import patch
from django.test import TestCase
from django.shortcuts import resolve_url as r

from workshop.core.forms import SubscriptionForm


class SubscriptionsNewPostValid(TestCase):
    @patch('workshop.core.views.export_to_mailchimp', return_value=True)
    def setUp(self, export_email):
        data = dict(
            email='new@tube.com',
        )
        self.resp = self.client.post(r('core:index'), data)

    def test_post(self):
        """ Valid POST should redirect to success page"""
        self.assertRedirects(self.resp, r('core:success'))


class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('core:index'), {})

    def test_post(self):
        """ Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/index.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscriptionsNewPostSameEmail(TestCase):
    @patch('workshop.core.views.export_to_mailchimp', return_value=False)
    def setUp(self, export_email):
        """
         data to be returned
        """
        data = dict(
            email='new@tube.com',
        )
        self.resp = self.client.post(r('core:index'), data)

    def test_post(self):
        """ Same POST email should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/index.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        """
        The form was filled
        No erros
        """
        form = self.resp.context['form']
        self.assertFalse(form.errors)

    def test_message_in_template(self):
        """
        Part of the error message index.html shows
        """
        self.assertContains(self.resp, 'Important')

    def test_data_in_form(self):
        """
        The duplicate email should be returned
        to the index.html page
        """
        self.assertContains(self.resp, 'new@tube.com')
