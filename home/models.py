from django.db import models
from django.contrib.auth.models import User
from datetime import  date
# Create your models here.
class rfid(models.Model):
    uid = models.TextField(unique=True, null=True, blank=True)

class meds(models.Model):
    uid = models.ForeignKey(rfid, on_delete=models.CASCADE, null=True, blank=True)
    bfr = models.TextField(null=True, blank=True)
    afr = models.TextField(null=True, blank=True)


class Pvitals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    bp = models.IntegerField(null=True, blank=True)
    sugar = models.IntegerField(null=True, blank=True)
    spo2 = models.IntegerField(null=True, blank=True)
    body_temp = models.IntegerField(null=True, blank=True)
    pulse = models.IntegerField(null=True, blank=True)
    date = models.DateField(null = True, blank = True, default=date.today)