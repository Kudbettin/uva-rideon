from django.shortcuts import render
from django.views import generic

from .models import Drive

class DriveView(generic.DetailView):
    model = Drive
    template_name = "drives/posting.html"

# class BaseDriveView(generic.DetailView):
#     model = Drive
#     template_name = "drivers/base.html"

def base(request):
    latest_drives_list = Drive.objects.order_by('date_time')
    context = {
        'latest_drives_list': latest_drives_list
    }
    return render(request, 'drives/base.html', context)
    # return render(request, "drives/base.html")
