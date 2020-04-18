
import datetime

from django.db import models
from django.utils import timezone
# Create your models here.


class Comparable(models.Model):



    comparable_name = models.CharField(max_length=200)
    entry_date = models.DateTimeField('date published')

    def __str__(self):
        return self.comparable_name

    def __str__(self):
        return self.entry_date


class Choice(models.Model):

    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Comparable, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)