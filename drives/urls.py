# drives/urls.py
from django.urls import path
from .views import *

app_name = "drives"
urlpatterns = [
  path('<int:driveId>/passenger_request', passenger_request, name='passenger_request'),
  path('<int:driveId>/passenger_remove', passenger_remove, name='passenger_remove'),
  path('<int:driveId>/request_reject', reject_request, name='reject_request'),
  path('<int:driveId>/request_approve', approve_request, name='approve_request'),
  path('<int:driveId>/leave_ride', leave_ride, name='leave_ride'),
  path('<int:driveId>/submit_waypoint', submit_waypoint, name='submit_waypoint'),
  path('', RideList.as_view(), name='list'),
  path('', render_ridelist, name='list'),
  path('search', search_ridelist, name='search'),
  path('<pk>/', DriveView.as_view(), name='post_details'),
  path('new', post_new, name='post_new')  
]
