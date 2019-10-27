from django.contrib import admin

from .models import *

admin.site.register(Location)
admin.site.register(Drive)
admin.site.register(DriverReview)
admin.site.register(RiderReview)
