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
        fields = ('name', 'gender', 'phone', 'home_town', 'about')
    


    '''
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(UserChangeForm, self).__init__(*args, **kwargs)


    def save(self, *args, **kwargs):
        kwargs['commit']=False
        obj = super(UserChangeForm, self).save(*args, **kwargs)
        print(self.request)
        if self.request:
            obj.username = self.request.username
            obj.save()
        return obj
    '''