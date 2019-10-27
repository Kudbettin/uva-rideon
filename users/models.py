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
    gender = models.CharField(max_length=15, default = '')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    about = models.TextField(max_length=1000, default = 'Write a bio to let people know about you!')
    profile_pic = models.ImageField(upload_to=user_directory_path, default='default/default_profile_pic.jpg')
    home_town = models.CharField(max_length=20, default = '')


    def __str__(self):
         #get_fields gets stuff from AbstractUser that we don't want
        local_fields = ['name', 'gender', 'phone', 'about', 'home_town']
        field_values = []
        for field in local_fields:
            field_values.append(getattr(self, field, ''))
        return ' '.join(field_values)
      
class UserFriends(models.Model):
    current_user = models.ForeignKey(CustomUser, related_name='owner', null=True, on_delete=models.CASCADE)
    users = models.ManyToManyField(CustomUser, blank=True)

    def add_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.add(new_friend)

    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.remove(new_friend)

    def __str__(self):
        return str(self.current_user)
