# drives/urls.py
from django.urls import path
from .views import *

urlpatterns = [
  path('', RideList.as_view(), name='list'),
  path('<pk>/', DriveView.as_view())  
]
