from django.test import Client, TestCase
from django.contrib.auth import authenticate
from users.models import CustomUser


class UserTester(TestCase):
    """
    Social auth tests.
    """
    def setUp(self):
        pass

    def testCreateNewUser(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.user.set_password('12345')
        self.user.save()
        self.assertEqual(CustomUser.objects.all().count(), 1)
		
    def testUserLogin(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.user.set_password('12345')
        self.user.save()
		
        authenticated_user = authenticate(username='testuser', password='12345')
		
        self.assertEqual(self.user, authenticated_user)
		
