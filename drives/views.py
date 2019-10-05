from django.shortcuts import render

from .models import Drive

class DriveView(generic.DetailView):
    model = Drive
    template_name = "drives/posting.html"