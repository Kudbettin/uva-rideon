from django import forms
from django.utils import timezone

from .models import *

# why does this inherit UserCreationForm?
# class DriveCreationForm(UserCreationForm):
class DriveCreationForm(forms.ModelForm):

    class Meta:
        model = Drive
        # fields = ("start_location", "start_id", "start_street", "start_city", "start_state", "start_zip", 
        #             "end_location", "end_id", "end_street", "end_city", "end_state", "end_zip",
        #             "title", "driver", "date_time", "description", "passengers", "min_cost",
        #             "max_cost", "payment_method", "max_passengers", "car_description",
        #             "luggage_description")
        fields = ("start_street_number", "start_route", "start_locality", "start_administrative_area_level_1", "start_country", "start_postal_code", 
                    "end_street_number", "end_route", "end_locality", "end_administrative_area_level_1", "end_country", "end_postal_code",
                    "title", "driver", "date_time", "description", "passengers", "min_cost",
                    "max_cost", "payment_method", "max_passengers", "car_description",
                    "luggage_description")
        date_time = forms.DateField(label='date_time', input_formats=['%Y-%m-%d'], initial=timezone.now())


# class DriveChangeForm():
#     pass