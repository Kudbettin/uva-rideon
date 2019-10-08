# drives/urls.py
from django.urls import path
from .views import RideList

urlpatterns = [
    path('', RideList.as_view(), name='list'),
]
