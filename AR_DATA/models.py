from django.db import models

# Create your models here.
class User_data(models.Model):
    key = models.CharField(max_length=50)
    stamp_count = models.IntegerField()
    store_count = models.IntegerField()
    tour_count = models.IntegerField()
    secret_count = models.IntegerField()