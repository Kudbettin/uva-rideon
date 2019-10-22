from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ('username', 'email')

class CustomUserChangeForm(forms.ModelForm):

	class Meta:
		model = CustomUser
		fields = ('name', 'gender', 'phone', 'home_town', 'about', 'profile_pic')
