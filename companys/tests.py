from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from .models import CompanyProfile, Membership
from accounts.models import UserProfile


class CompanyProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_company = "test_company"
        User.objects.create_user(
            'test_user',
            'testuser@gmail.com',
            'test_password'
        )
        self.assertEqual(User.objects.count(), 1)

    def test_list_companies_response(self):
        response = self.client.get(reverse('companies'))
        # login required
        self.assertEqual(response.status_code, 302)
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('accounts'))
        self.assertEqual(response.status_code, 200)

    def test_create_membership_complete(self):
        company = CompanyProfile(name=self.test_company)
        company.save()
        self.assertEqual(CompanyProfile.objects.count(), 1)
        user_acc = UserProfile.objects.get(user__username="test_user")
        membership = Membership(company=company, account=user_acc)
        membership.save()
        self.assertEqual(Membership.objects.count(), 1)
        self.assertEqual(membership.account.user.username,
                         user_acc.user.username)
        self.assertEqual(membership.company.name, self.test_company)
