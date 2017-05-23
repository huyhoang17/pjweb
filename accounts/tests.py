from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from .models import UserProfile


class UserProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = 'test_user'

    def test_list_account_response(self):
        response = self.client.get(reverse('accounts'))
        self.assertEqual(response.status_code, 200)

    def test_auth_user_create_complete(self):
        self.assertEqual(User.objects.count(), 0)
        new_user = User(username=self.test_user)
        new_user.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
