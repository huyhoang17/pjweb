from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from .models import CompanyProfile, Membership
from accounts.models import UserProfile


class CompanyProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = "test_user"
        self.test_company = "test_company"

    def create_test_user(self):
        test_user = User(username=self.test_user)
        test_user.save()
        return test_user

    def test_list_companies_response(self):
        response = self.client.get(reverse('companies'))
        self.assertEqual(response.status_code, 200)

    def test_create_membership_complete(self):
        test_user = self.create_test_user()
        self.assertEqual(UserProfile.objects.count(), 1)
        company = CompanyProfile(name=self.test_company)
        company.save()
        self.assertEqual(CompanyProfile.objects.count(), 1)
        membership = Membership(company=company, account=test_user.userprofile)
        membership.save()
        self.assertEqual(Membership.objects.count(), 1)
        self.assertEqual(membership.account.user.username, self.test_user)
        self.assertEqual(membership.company.name, self.test_company)
