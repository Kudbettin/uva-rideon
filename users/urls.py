# users/urls.py
from django.urls import path
from  django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, ProfileView, EditProfileView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<pk>/', ProfileView.as_view(), name="profile"),
    path('<pk>/edit/', EditProfileView.as_view()),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')
]
