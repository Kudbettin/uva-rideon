from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.email

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