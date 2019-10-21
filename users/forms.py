from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from drives.models import DriverReview, RiderReview

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class DriverReviewForm(forms.ModelForm):

    class Meta:
        model = DriverReview
        fields = ("by", "of", "title", "description", "rating", "drive")

class RiderReviewForm(forms.ModelForm):

    class Meta:
        model = RiderReview
        fields = ("by", "of", "title", "description", "rating", "drive")
