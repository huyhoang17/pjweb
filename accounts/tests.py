from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class UserProfileTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(
            'test_user',
            'testuser@gmail.com',
            'test_password'
        )
        self.client = Client()
        self.assertEqual(User.objects.count(), 1)

    def test_list_account_response(self):
        response = self.client.get(reverse('accounts'))
        # login required
        self.assertEqual(response.status_code, 302)
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('accounts'))
        self.assertEqual(response.status_code, 200)
