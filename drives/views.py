from django.shortcuts import render
from django.views.generic.list import ListView
from drives.models import Drive, create_drive

'''
View function for the home page of the website
'''
class RideList(ListView):

	model = Drive