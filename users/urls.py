# users/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, ProfileView, EditProfileView, MyRidesView, post_new_review

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<pk>/', ProfileView.as_view(), name="profile"),
    path('<pk>/edit/', EditProfileView.as_view()),
    path('<pk>/myrides/', MyRidesView.as_view(), name='myrides'),
    path('<pk>/myrides/review', post_new_review, name='post_new_review')  
]
