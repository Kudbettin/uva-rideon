from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.views import generic
from django.views.generic.list import ListView

from django.urls import reverse
from django.utils import timezone

from drives.models import Drive, create_drive
from drives.forms import DriveCreationForm

class DriveView(generic.DetailView):
    model = Drive
    template_name = "drives/posting.html"

''' 
Base view to display ride posts. We can probably kill this after comfirming the other listing is compatible with the postings
'''    
def base(request):
    latest_drives_list = Drive.objects.order_by('date_time')
    context = {
        'latest_drives_list': latest_drives_list
    }
    return render(request, 'drives/base.html', context)
    # return render(request, "drives/base.html")

'''
View function for the home page of the website
'''
class RideList(ListView):

	model = Drive


def post_new(request):
    if request.method == "POST":
        form = DriveCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # post.date_time = timezone.now()
            post.save()
            return HttpResponseRedirect(reverse('drives:post_details', args=(post.pk,)))

    else:
        form = DriveCreationForm()
        
    return render(request, 'drives/new_drive.html', {'form': form})
