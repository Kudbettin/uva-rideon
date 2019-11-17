from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from .models import CustomUser
from drives.models import DriverReview, RiderReview
import re

class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ('username', 'email')

class CustomUserChangeForm(forms.ModelForm):

	class Meta:
		model = CustomUser
		fields = ('username', 'gender', 'phone', 'about', 'profile_pic')
		phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
		phone = forms.CharField(validators=[phone_validator], max_length=17, empty_value='999-999-999',) #enforces validation at DB level 

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		phone_regex = r'^\+?1?\d{9,15}$'
		if not re.match(phone_regex, phone) and phone != '':
			raise forms.ValidationError('Phone number must be entered in the format: +999999999')
		return phone

class DriverReviewForm(forms.ModelForm):

	class Meta:
		model = DriverReview
		fields = ("by", "of", "title", "description", "rating", "drive")

class RiderReviewForm(forms.ModelForm):

	class Meta:
		model = RiderReview
		fields = ("by", "of", "title", "description", "rating", "drive")
