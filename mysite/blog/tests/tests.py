from django.test import TestCase

# Create your tests here.


class SampleTest(TestCase):

    def test_something(self):
        """This test should fail"""
        self.assertEqual(2 + 2, 51)
