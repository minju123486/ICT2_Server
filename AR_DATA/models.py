from django.db import models

# Create your models here.
class User_data(models.Model):
    key = models.CharField(max_length=50)
    stamp_count = models.IntegerField()
    store_count = models.IntegerField()
    tour_count = models.IntegerField()
    secret_count = models.IntegerField()
    
    
class Tour_place(models.Model):
    tour_id = models.IntegerField()
    place = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    
class Check(models.Model):
    key = models.IntegerField()
    tour_id = models.IntegerField()
    
class stamp_table(models.Model):
    key = models.IntegerField()
    tour_id = models.CharField(max_length=50)
    num = models.IntegerField()