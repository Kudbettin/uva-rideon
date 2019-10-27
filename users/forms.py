from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ('username', 'email')

class CustomUserChangeForm(forms.ModelForm):

	class Meta:
		model = CustomUser
		fields = ('name', 'gender', 'phone', 'home_town', 'about', 'profile_pic')
		phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
		phone = forms.CharField(validators=[phone_regex], max_length=17)