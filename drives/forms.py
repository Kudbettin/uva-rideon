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

        self.fields['title'].widget           = forms.TextInput(attrs={'placeholder': 'My Awesome Trip'})
        self.fields['payment_method'].widget  = forms.TextInput(attrs={'placeholder': 'Venmo, when trip ends'})
        self.fields['description'].widget     = forms.Textarea(attrs={'rows': 2})
        self.fields['car_description'].widget = forms.Textarea(attrs={'rows': 2})
        self.fields['luggage_description'].widget = forms.Textarea(attrs={'rows': 2, 'placeholder': 'Space for 1 small suitcase per person'})
        self.fields['date'].widget = forms.TextInput(attrs={'autocomplete': 'off'})
        self.fields['time'].widget = forms.TextInput(attrs={'autocomplete': 'off'})

    
    def clean(self):
        if self.data['start_coordinates_x'] == "":
            # raise forms.ValidationError("Start address bad format")
            self.add_error(None, forms.ValidationError("Start address bad format, make sure to pick a valid address from dropdown!"))

        if self.data['end_coordinates_x'] == "":
            # raise forms.ValidationError("End address bad format")
            self.add_error(None, forms.ValidationError("End address bad format, make sure to pick a valid address from dropdown!"))
        
        return self.cleaned_data
    
    def clean_min_cost(self):
        min_cost = float(self.data['min_cost'])
        max_cost = float(self.data['max_cost'])
        
        if min_cost > max_cost:
            raise forms.ValidationError("Min cost can't be greater than Max cost")

        return min_cost


class DriveChangeForm(forms.ModelForm):
    
    class Meta:
        model = Drive
        fields = ( "title", "driver", "description", "date", "time", "min_cost",
                "max_cost", "payment_method", "max_passengers", "car_description",
                "luggage_description")

    # def clean(self):
    #     if self.data['start_coordinates_x'] == "":
    #         # raise forms.ValidationError("Start address bad format")
    #         self.add_error(None, forms.ValidationError("Start address bad format, make sure to pick a valid address from dropdown!"))

    #     if self.data['end_coordinates_x'] == "":
    #         # raise forms.ValidationError("End address bad format")
    #         self.add_error(None, forms.ValidationError("End address bad format, make sure to pick a valid address from dropdown!"))
        
    #     return self.cleaned_data

    def clean_min_cost(self):
        min_cost = float(self.data['min_cost'])
        max_cost = float(self.data['max_cost'])
        
        if min_cost > max_cost:
            raise forms.ValidationError("Min cost can't be greater than Max cost")

        return min_cost