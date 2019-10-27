from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.views import generic
from django import template

from .models import CustomUser
from drives.models import Drive, DriverReview, RiderReview

from .forms import CustomUserCreationForm, DriverReviewForm, RiderReviewForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

class ProfileView(generic.DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['avg_rating'] = DriverReview.objects.filter(of=kwargs['object'].id).rating
        context['driver_avg_rating'] = 3
        context['rider_avg_rating'] = 4
        return context

class EditProfileView(generic.DetailView):
    model = CustomUser
    template_name = 'users/editprofile.html'

class MyRidesView(generic.DetailView):
    model = CustomUser
    template_name = 'users/myrides.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_rides'] = Drive.objects.filter(status="Listed")
        context['cancelled_rides'] = Drive.objects.filter(status="Cancelled")
        context['completed_rides'] = Drive.objects.filter(status="Completed")
        context['riders_to_review_per_drive'] = []
        for drive in context['completed_rides']:
            query = Drive.objects.filter(id=drive.id)[0].passengers.all()

            context['riders_to_review_per_drive'].append( {"id":drive.id, "query":query})
            print(context['riders_to_review_per_drive'])
        return context

def post_new_review(request, pk):
    if request.method == "POST":
        request.POST = request.POST.copy()

        request.POST["by"] = request.user.id
        request.POST["of"] = 2
        
        if(request.user.id == Drive.objects.filter(id=request.POST["drive"])[0].driver.id):
            # Driver is reviewing passanger
            
            form = RiderReviewForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return HttpResponseRedirect(reverse_lazy('myrides', args=(pk,)))
            else:
                print(form.errors)
                print("error adding review")
        else:
            # Rider reviewing driver

            form = DriverReviewForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return HttpResponseRedirect(reverse_lazy('myrides', args=(pk,)))
            else:
                print(form.errors)
                print("error adding review")
    else:
        form = RideReviewForm()
        
    return render(request, 'users/myrides.html')
