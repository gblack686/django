
import datetime

from django.db import models
from django.utils import timezone
# Create your models here.


class Comparable(models.Model):



    comparable_name = models.CharField(max_length=200)
    entry_date = models.DateTimeField('date published')

    def __str__(self):
        return self.comparable_name

    def was_published_recently(self):
        now = timezone.now()    
        return now - datetime.timedelta(days=1) <= self.entry_date <= now



class Choice(models.Model):


    question = models.ForeignKey(Comparable, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    neighborhood =  models.CharField(max_length=200)
    market =  models.CharField(max_length=200)
    builder = models.CharField(max_length=200)
    lot_size = models.PositiveIntegerField(default=0)
    total_homes = models.PositiveIntegerField(default=0)
    homes_sold = models.PositiveIntegerField(default=0)
    sales_start_date = models.DateTimeField()
    survey_date = models.DateField(auto_now_add=True)
    base_tax_rate = models.FloatField(default=0)
    total_tax_rate = models.FloatField('Total Tax Rate', default=0)
    monthly_hoa = models.IntegerField(default=0)
    incentives = models.PositiveIntegerField(default=0)
    website = models.URLField(max_length=200)

    

    
    def __str__(self):
        return self.choice_text