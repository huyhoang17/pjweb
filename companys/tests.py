from django.test import TestCase


class TruthTests(TestCase):

    def test_a_truth(self):
        self.assertTrue(1 + 1 == 2)
