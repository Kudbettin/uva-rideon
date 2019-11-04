from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.views import generic
from django import template
from drives.models import Drive, DriverReview, RiderReview
from .models import CustomUser, UserFriends
from .forms import CustomUserCreationForm, CustomUserChangeForm, DriverReviewForm, RiderReviewForm

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

class EditProfileView(generic.UpdateView):
  
    model = CustomUser
    fields = [ 'username', 'gender', 'phone','home_town', 'about', 'profile_pic']
    template_name = 'users/editprofile.html'
    
    def get_friends(self, request):
        users = CustomUser.objects.exclude(id=request.user)
        friend = UserFriends.objects.get(current_user=request.user)
        friends = friend.users.all()

 
def get_fields(request,pk):
    
    instance = CustomUser.objects.get(id=pk)
    form = CustomUserChangeForm(request.POST or None, request.FILES, instance=instance)
    if form.is_valid():
        #form.profile_pic = request.FILES.get('profile_pic', None)
        form.save()
        return redirect('/users/'+ pk + '/edit') # should update these to use reverse
    else:
        return redirect('/users/'+ pk + '/edit')

    return render(request, '/users/'+ pk + '/edit', {'form': form})  

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
            ridersNeedReviews = []
            ridersWithReviewsIds = []
            ridersWithReviews = RiderReview.objects.filter(drive=drive.id, by=self.request.user.id).all()
            
            for item in ridersWithReviews:
                ridersWithReviewsIds.append(item.of)
            
            for person in query:
                if person not in ridersWithReviewsIds:
                    ridersNeedReviews.append(CustomUser.objects.get(id=person.id))

            context['riders_to_review_per_drive'].append( {"id":drive.id, "query":ridersNeedReviews})

        context['drivers_to_review_per_drive'] = []

        for drive in context['completed_rides']:
            query = Drive.objects.filter(id=drive.id)[0].driver
            context['drivers_to_review_per_drive'].append( {"id":drive.id, "query":[]})
            
            if DriverReview.objects.filter(drive=drive.id, by=self.request.user.id).count() == 0:
                context['drivers_to_review_per_drive'][0]['query'].append(query)
        
        return context

def post_new_review(request, pk):
    if request.method == "POST":
        request.POST = request.POST.copy()

        request.POST["by"] = request.user.id
        
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

def change_friends(request, operation, pk):
    new_friend = CustomUser.objects.get(pk=pk)
    if operation == 'add':
        UserFriends.add_friend(request.user, new_friend)
    elif operation == 'remove':
        UserFriends.remove_friend(request.user, new_friend)
    return redirect()
