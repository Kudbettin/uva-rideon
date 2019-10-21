from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'gender', 'phone', 'home_town')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(UserChangeForm, self).__init__(*args, **kwargs)

    def is_valid(self):
    	return True

    def save(self, *args, **kwargs):
        kwargs['commit']=False
        obj = super(UserChangeForm, self).save(*args, **kwargs)
        print(self.request)
        if self.request:
            obj.user = self.request.user
            obj.save()
        return obj