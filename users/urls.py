# users/urls.py
from django.urls import path
from  django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, ProfileView, EditProfileView, MyRidesView, post_new_review
from . import views
app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('<pk>/', ProfileView.as_view(), name="profile"),
    path('<pk>/edit/', EditProfileView.as_view()),
    path('<pk>/edit/redirect/', views.get_fields),
    path('<pk>/myrides/', MyRidesView.as_view(), name='myrides'),
    path('<pk>/myrides/review', post_new_review, name='post_new_review'), 
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')
]
