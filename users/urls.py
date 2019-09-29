# users/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<pk>/', ProfileView.as_view()),
]
