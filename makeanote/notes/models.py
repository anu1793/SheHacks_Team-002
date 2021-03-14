
# Create your models here.
from django.db import models

class WordStreak(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    language = models.CharField(max_length=50)
    date = models.DateField()



class SentHighlight(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    sentence = models.CharField(max_length=5000)
    date = models.DateField()



