# drives/urls.py
from django.urls import path
from .views import *

app_name = "drives"
urlpatterns = [
  path('', RideList.as_view(), name='list'),
  path('<pk>/', DriveView.as_view(), name='post_details'),
  path('new', post_new, name='post_new')  
]
