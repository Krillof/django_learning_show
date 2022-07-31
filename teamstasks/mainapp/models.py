from re import M
from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='Membership', through_fields=('team','user'))

class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Task(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=400)
    is_done = models.BooleanField(default=False)
