from django import forms
from django.utils import timezone

from .models import *

# why does this inherit UserCreationForm?
# class DriveCreationForm(UserCreationForm):
class DriveCreationForm(forms.ModelForm):

    class Meta:
        model = Drive
        fields = ("start_location", "end_location", "title", "driver",
                    "date", "time", "description", "passengers", "min_cost",
                    "max_cost", "payment_method", "max_passengers", "car_description",
                    "luggage_description")
        date_time = forms.DateField(label='date_time', input_formats=['%Y-%m-%d'], initial=timezone.now())


# class DriveChangeForm():
#     pass