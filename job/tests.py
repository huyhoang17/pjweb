from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class CompanyProfileTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_job = "test_job"

    def test_list_jobs_response(self):
        response = self.client.get(reverse('jobs'))
        self.assertEqual(response.status_code, 200)
