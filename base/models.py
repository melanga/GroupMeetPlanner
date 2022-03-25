from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    bio = models.TextField(null=True)
    # default_time = models.ForeignKey(
    #     'Time', on_delete=models.SET_NULL, null=True, blank=True, related_name='default_time'
    # )
    # profile_pic = models.ImageField(null=True, default="avatar.svg")
    REQUIRED_FIELDS = []


class Group(models.Model):
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Time(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    # availability = models.CharField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.start_time.isoformat(timespec='minutes')) \
               + " : " \
               + str(self.end_time.isoformat(timespec='minutes'))
