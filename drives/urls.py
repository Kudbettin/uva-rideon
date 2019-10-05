# drives/urls.py
from django.urls import path
from .views import *

urlpatterns = [
	path('', base, name="base"),
    path('<pk>/', DriveView.as_view())    
]