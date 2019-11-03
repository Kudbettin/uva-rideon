from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.views import generic
from django.views.generic.list import ListView

from django.urls import reverse
from django.utils import timezone

from drives.models import Drive, create_drive, Location
from drives.forms import DriveCreationForm
from drives.search_drives import search_drives
from users.models import CustomUser
from django.template.context import make_context

import json

'''
Called when a user clicks 'Join Ride'
Adds them to the list of requested passengers so the 
driver can decide to let them join or not
'''
def passenger_request(request, driveId):
    if request.method == "POST":
        # Make sure the user being added is the logged in user
        id = request.POST['userId']        
        logged_in_user = request.user.id
        if int(id) != int(logged_in_user):
            return HttpResponseRedirect(reverse('insuficient_permission'))
            
        # Make sure the user isn't already on the requestlist or the passenger list
        if Drive.objects.get(id=driveId).passengers.filter(id=id).count() != 0 or Drive.objects.get(id=driveId).requestList.filter(id=id).count() != 0:
            return HttpResponseRedirect(reverse('insuficient_permission'))

        Drive.objects.get(id=driveId).add_passenger_to_requestlist(CustomUser.objects.get(id=id))
        return HttpResponseRedirect(reverse('drives:post_details', args=(driveId,)))
        
'''
Called when a Passenger leaves a ride
'''
def leave_ride(request, driveId):
    if request.method == "POST":
        # Make sure the user leaving is the logged in user
        id = request.POST['passengerId']        
        logged_in_user = request.user.id
        if int(id) != int(logged_in_user):
            return HttpResponseRedirect(reverse('insuficient_permission'))
            
        # Make sure the user is actually on the passenger list
        if Drive.objects.get(id=driveId).passengers.filter(id=id).count() != 1:
            return HttpResponseRedirect(reverse('insuficient_permission'))
    
        Drive.objects.get(id=driveId).passengers.remove(CustomUser.objects.get(id=id))
        return HttpResponseRedirect(reverse('drives:post_details', args=(driveId,)))
        
'''
Called when a Driver removes a passenger
'''
def passenger_remove(request, driveId):
    if request.method == "POST":
        # Make sure the logged in user is the drive owner
        id = request.POST['passengerId']
        owner_id = Drive.objects.get(id=driveId).driver.id        
        logged_in_user = request.user.id
        if int(owner_id) != int(logged_in_user):
            return HttpResponseRedirect(reverse('insuficient_permission'))
            
        # Make sure the user is actually on the passenger list
        if Drive.objects.get(id=driveId).passengers.filter(id=id).count() != 1:
            return HttpResponseRedirect(reverse('insuficient_permission'))
    
        Drive.objects.get(id=driveId).passengers.remove(CustomUser.objects.get(id=id))
        return HttpResponseRedirect(reverse('drives:post_details', args=(driveId,)))
        
'''
Called when a Driver approves a passenger request
'''
def approve_request(request, driveId):
    if request.method == "POST":
        # Make sure the logged in user is the drive owner
        id = request.POST['passengerId']
        owner_id = Drive.objects.get(id=driveId).driver.id        
        logged_in_user = request.user.id
        if int(owner_id) != int(logged_in_user):
            return HttpResponseRedirect(reverse('insuficient_permission'))
            
        # Make sure the user is on the requestList and not on the passengerList
        if Drive.objects.get(id=driveId).passengers.filter(id=id).count() != 0 and Drive.objects.get(id=driveId).requestList.filter(id=id).count() != 1:
            return HttpResponseRedirect(reverse('insuficient_permission'))
            
        Drive.objects.get(id=driveId).passengers.add(CustomUser.objects.get(id=id))
        Drive.objects.get(id=driveId).requestList.remove(CustomUser.objects.get(id=id))
        return HttpResponseRedirect(reverse('drives:post_details', args=(driveId,)))
        
'''
Called when a Driver rejects a passenger request
'''
def reject_request(request, driveId):
    if request.method == "POST":
        # Make sure the logged in user is the drive owner
        id = request.POST['passengerId']
        owner_id = Drive.objects.get(id=driveId).driver.id        
        logged_in_user = request.user.id
        if int(owner_id) != int(logged_in_user):
            return HttpResponseRedirect(reverse('insuficient_permission'))
            
        # Make sure the user is on the requestList
        if not Drive.objects.get(id=driveId).requestList.get(id=id):
            return HttpResponseRedirect(reverse('insuficient_permission'))
            
        id = request.POST['passengerId']
        Drive.objects.get(id=driveId).requestList.remove(CustomUser.objects.get(id=id))
        return HttpResponseRedirect(reverse('drives:post_details', args=(driveId,)))

class DriveView(generic.DetailView):
    model = Drive
    template_name = "drives/posting.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Mark if there are open spaces in the car
        # so we can render a button to apply to the ride
        if kwargs['object'].max_passengers - kwargs['object'].passengers.count() > 0:
            context['empty_passenger_slots'] = True
        
        context['waitlistIds'] = []
        for passenger in kwargs['object'].requestList.all():
            context['waitlistIds'].append(passenger.id)
        context['passengerIds'] = []
        for passenger in kwargs['object'].passengers.all():
            context['passengerIds'].append(passenger.id)
        
        return context

''' 
Returns an HTML representation of a search over the ridelist.
Search parameters are passed as POST request parameters.
'''
def search_ridelist(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        return render(request, 'drives/drive_list_inner.html', {'drive_list': search_drives(json_data)})
    return render(request, 'drives/drive_list_inner.html')

'''
Renders the outer layers of the main drive list page,
which contain the checkboxes and the search bar.
'''
def render_ridelist(request):
    return render(request, 'drives/drive_list_outer.html')

def post_new(request):
    if request.method == "POST":
        # re-format time data to use 24 hour scale for Django
        if request.POST['time']:
            request.POST = request.POST.copy()
            if 'am' in request.POST['time']:
                request.POST['time'] = request.POST['time'].replace('am', '')
            elif 'pm' in request.POST['time']:
                request.POST['time'] = request.POST['time'].replace('pm', '')
                hours,minutes = request.POST['time'].split(":")
                request.POST['time'] = str(int(hours) + 12) + ":" + minutes
                
        

        form = DriveCreationForm(request.POST)
        print(request.POST)

        if form.is_valid():

            start_location = Location.objects.create(
                coordinates_x=request.POST["start_coordinates_x"],
                coordinates_y=request.POST["start_coordinates_y"])

            end_location = Location.objects.create(
                coordinates_x=request.POST["end_coordinates_x"],
                coordinates_y=request.POST["end_coordinates_y"])

            start_location.save()
            end_location.save()

            post = form.save(commit=False)
            post.start_location = start_location
            post.end_location = end_location
            post.save()
            return HttpResponseRedirect(reverse('drives:post_details', args=(post.pk,)))
        else:
            print(form.errors)
    else:
        form = DriveCreationForm()

    return render(request, 'drives/new_drive.html', {'form': form})
