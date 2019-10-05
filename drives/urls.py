# drives/urls.py
from django.urls import path
from .views import DriveView

urlpatterns = [
    path('<pk>/', DriveView.as_view())
]