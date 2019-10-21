from django import forms
from django.utils import timezone

from .models import *

class DriveCreationForm(forms.ModelForm):

    class Meta:
        model = Drive
        error_css_class = 'error'
        fields = ( "title", "driver", "description", "date", "time", "min_cost",
                    "max_cost", "payment_method", "max_passengers", "car_description",
                    "luggage_description")
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        
		# Remove driver and time widgets
        self.fields['driver'].widget = forms.HiddenInput()
		
		# Modify widget types and HTML attributes where sufficient
        self.fields['title'].widget           = forms.TextInput(attrs={'placeholder': 'My Awesome Trip'})
        self.fields['payment_method'].widget  = forms.TextInput(attrs={'placeholder': 'Venmo, when trip ends'})
        self.fields['description'].widget     = forms.Textarea(attrs={'rows': 2})
        self.fields['car_description'].widget = forms.Textarea(attrs={'rows': 2})
        self.fields['luggage_description'].widget = forms.Textarea(attrs={'rows': 2, 'placeholder': 'Space for 1 small suitcase per person'})

# class DriveChangeForm():
#     pass