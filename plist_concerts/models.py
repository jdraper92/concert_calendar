from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=45)
    artists = models.TextField()
    email = models.CharField(max_length = 60, default = 'default@email.com')
    last_update = models.CharField(max_length=10, default = '10102017')

class Artists(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    date = models.CharField(max_length=10)

class TimeKeeper(models.Model):
    first_date = models.CharField(max_length=10)
    last_date  = models.CharField(max_length=10)
