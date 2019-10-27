from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
import PIL #needed for ImageField



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id><filename>
    return 'user_media/{0}_{1}'.format(instance.username, filename)

class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, default = '')
    gender = models.CharField(max_length=10, default = '')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    about = models.TextField(max_length=1000, default = 'Write a bio to let people know about you!')
    profile_pic = models.ImageField(upload_to=user_directory_path, default='default/default_profile_pic.jpg')
    home_town = models.CharField(max_length=20, default = '')

    def __str__(self):
        return self.email
