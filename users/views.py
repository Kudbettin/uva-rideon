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
    fields = [ 'name', 'gender', 'phone','home_town', 'about']
    template_name = 'users/editprofile.html'

def get_fields(request,pk):
    
    instance = CustomUser.objects.get(id=pk)
    form = CustomUserChangeForm(request.POST or None, instance=instance)
    form.profile_pic = request.FILES.get('profile_pic', None)
    if form.is_valid():
          form.save()
          return redirect('/users/'+ pk + '/edit')
    return render(request, '/users/'+ pk + '/edit', {'form': form})  

    '''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CustomUserChangeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(pk)
            form.save(commit=False).save()
            return HttpResponseRedirect('users/editprofile.html' )

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomUserChangeForm()
    print(form)
    return render(request, 'users/editprofile.html', {'form' : form})
    #render(request, , {'CustomUser': CustomUser})
    '''