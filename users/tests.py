from django.test import Client, TestCase
from django.contrib.auth import authenticate
from users.models import CustomUser
from users.custom_social_auth_pipeline import allowed_email 

class UserTester(TestCase):
    """
    Social auth tests.
    """
    def setUp(self):
        pass

    def testCreateValidNewUser(self):
        self.user = CustomUser.objects.create_user(username='hacker@virginia.edu', email='hacker@virginia.edu', password='12345')
        self.user.set_password('12345')
        self.user.save()
        self.assertEqual(CustomUser.objects.all().count(), 1)
		
    def testCreateUserInvalidEmail(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.assertFalse(allowed_email(self.user.email))
    
    def testUserLogin(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.user.set_password('12345')
        self.user.save()
		
        authenticated_user = authenticate(username='testuser', password='12345')
		
        self.assertEqual(self.user, authenticated_user)
		
