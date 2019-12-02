# users/urls.py
from django.urls import path
from  django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, ProfileView, EditProfileView, MyRidesView, post_new_review, post_add_friend, post_remove_friend
from . import views
app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<pk>/', ProfileView.as_view(), name="profile"),
    path('<pk>/edit/', EditProfileView.as_view(), name = 'edit_profile'),
    path('<pk>/edit/redirect/', views.get_fields),
    path('<pk>/myrides/', MyRidesView.as_view(), name='myrides'),
    path('<pk>/myrides/review', post_new_review, name='post_new_review'), 
    path('<pk>/add_friend', post_add_friend, name='post_add_friend'), 
    path('<pk>/remove_friend', post_remove_friend, name='post_remove_friend'), 
]
