from django.test import Client, TestCase
from django.contrib.auth import authenticate
from users.models import CustomUser
from users.forms import CustomUserChangeForm
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

class UserEditsTester(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='hacker@virginia.edu', email='hacker@virginia.edu', password='12345')

    def testFormEditAllFieldsValid(self):
        form = CustomUserChangeForm(data={'username':'John_Doe' , 'gender':'Male', 'phone':'+17037561234', 'about':'Some About'})
        self.assertTrue(form.is_valid())

    def testFormEditInvalidPhone(self):
        form = CustomUserChangeForm(data={'username':'John_Doe' , 'gender':'Male', 'phone':'+1703756123w', 'about':'Some About'})
        self.assertFalse(form.is_valid())

    def testProfileEditAllFieldsValid(self):
        local_fields = ['username', 'gender', 'phone', 'about']
        correct_data = {'username':'striker417' , 'gender':'Male', 'phone':'+17037561234', 'about':'I am a god at soccer'}
        self.form = CustomUserChangeForm(data={'username':'striker417' , 'gender':'Male', 'phone':'+17037561234', 'about':'I am a god at soccer'}, instance=self.user)
        if self.form.is_valid():
            self.form.save()

        for field in local_fields:
            self.assertTrue(getattr(self.user, field, '') == correct_data[field] )