from django.test import TestCase
from users.models import *

"""
Example unit tests to base others off of
"""
class UserTester(TestCase):
	def setUp(self):
		CustomUser.objects.create(email="email@email.com", username="me")
		
	def test_email(self):
		users = CustomUser.objects.filter(email="email@email.com", username="me")
		self.assertEqual(users.count(), 1)
		
	def test_email_2(self):
		users = CustomUser.objects.filter(email="email@email.com", username="me")
		self.assertEqual(users.count(), 1)