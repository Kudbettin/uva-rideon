from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import generic

from .models import CustomUser
from drives.models import DriverReview, RiderReview

from .forms import CustomUserCreationForm, CustomUserChangeForm

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
    fields = [ 'name', 'gender', 'phone','home_town', 'about', 'profile_pic']
    template_name = 'users/editprofile.html'

def get_fields(request,pk):
    
    instance = CustomUser.objects.get(id=pk)
    form = CustomUserChangeForm(request.POST or None, request.FILES, instance=instance)
    if form.is_valid():
        #form.profile_pic = request.FILES.get('profile_pic', None)
        form.save()
        return redirect('/users/'+ pk + '/edit') # should update these to use reverse
    return render(request, '/users/'+ pk + '/edit', {'form': form})  
